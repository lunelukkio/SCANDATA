"""
Heka Patchmaster .dat file reader 

Structure definitions adapted from StimFit hekalib.cpp

Brief example::

    # Load a .dat file
    bundle = Bundle(file_name)
    
    # Select a trace
    trace = bundle.pul[group_ind][series_ind][sweep_ind][trace_ind]
    
    # Print meta-data for this trace
    print(trace)
    
    # Load data for this trace
    data = bundle.data[group_id, series_id, sweep_ind, trace_ind]

"""

import numpy as np
import re, struct, collections


class Struct(object):
    """High-level wrapper around struct.Struct that makes it a bit easier to 
    unpack large, nested structures.
    
    * Unpacks to dictionary allowing fields to be retrieved by name
    * Optionally massages field data on read
    * Handles arrays and nested structures
    
    *fields* must be a list of tuples like (name, format) or (name, format, function)
    where *format* must be a simple struct format string like 'i', 'd', 
    '32s', or '4d'; or another Struct instance.
    
    *function* may be either a function that filters the data for that field
    or None to exclude the field altogether.
    
    If *size* is given, then an exception will be raised if the final struct size
    does not match the given size.

    
    Example::
        
        class MyStruct(Struct):
            field_info = [
                ('char_field', 'c'),                # single char 
                ('char_array', '8c'),               # list of 8 chars
                ('str_field',  '8s', cstr),         # C string of len 8
                ('sub_struct', MyOtherStruct),      # dict generated by s2.unpack 
                ('filler', '32s', None),            # ignored field
            ]
            size_check = 300
            
        fh = open(fname, 'rb')
        data = MyStruct(fh)
    
    """
    field_info = None
    size_check = None
    _fields_parsed = None
    
    
    
    def __init__(self, data, endian='<'):
        """Read the structure from *data* and return an ordered dictionary of 
        fields.
        
        *data* may be a string or file.
        *endian* may be '<' or '>'
        """
        field_info = self._field_info()
        if not isinstance(data, (str, bytes)):
            data = data.read(self._le_struct.size)
        if endian == '<':
            items = self._le_struct.unpack(data)
        elif endian == '>':
            items = self._be_struct.unpack(data)
        else:
            raise ValueError('Invalid endian: %s' % endian)
        
        fields = collections.OrderedDict()
        
        i = 0
        for name, fmt, func in field_info:
            # pull item(s) out of the list based on format string
            if len(fmt) == 1 or fmt[-1] == 's':
                item = items[i]
                i += 1
            else:
                n = int(fmt[:-1])
                item = items[i:i+n]
                i += n
            
            # try unpacking sub-structure
            if isinstance(func, tuple):
                substr, func = func
                item = substr(item, endian)
            
            # None here means the field should be omitted
            if func is None:
                continue
            # handle custom massaging function
            if func is not True:
                item = func(item)
            fields[name] = item
            setattr(self, name, item)
            
        self.fields = fields
        
    @classmethod
    def _field_info(cls):
        if cls._fields_parsed is not None:
            return cls._fields_parsed
        
        fmt = ''
        fields = []
        for items in cls.field_info:
            if len(items) == 3:
                name, ifmt, func = items
            else:
                name, ifmt = items
                func = True
                
            if isinstance(ifmt, type) and issubclass(ifmt, Struct):
                func = (ifmt, func) # instructs to unpack with sub-struct before calling function
                ifmt = '%ds' % ifmt.size()
            elif len(ifmt) > 1 and re.match(r'\d*[xcbB?hHiIlLqQfdspP]', ifmt) is None:
                raise TypeError('Unsupported format string "%s"' % ifmt)
            
            fields.append((name, ifmt, func))
            fmt += ifmt
        cls._le_struct = struct.Struct('<' + fmt)
        cls._be_struct = struct.Struct('>' + fmt)
        cls._fields_parsed = fields
        if cls.size_check is not None:
            assert cls._le_struct.size == cls.size_check
        return fields

    @classmethod
    def size(cls):
        cls._field_info()
        return cls._le_struct.size
    
    @classmethod
    def array(cls, x):
        """Return a new StructArray class of length *x* and using this struct 
        as the array item type.
        """
        return type(cls.__name__+'[%d]'%x, (StructArray,), 
                    {'item_struct': cls, 'array_size': x})
        
    def __repr__(self, indent=0):
        indent_str = '    '*indent
        r = indent_str + '%s(\n'%self.__class__.__name__
        if not hasattr(self, 'fields'):
            r = r[:-1] + '<initializing>)'
            return r
        for k,v in self.fields.items():
            if isinstance(v, Struct):
                r += indent_str + '    %s = %s\n' % (k, v.__repr__(indent=indent+1).lstrip())
            else:
                r += indent_str + '    %s = %r\n' % (k, v)
        r += indent_str + ')'
        return r

    def get_fields(self):
        """Recursively convert struct fields+values to nested dictionaries.
        """
        fields = self.fields.copy()
        for k,v in fields.items():
            if isinstance(v, StructArray):
                fields[k] = [x.get_fields() for x in v.array]
            elif isinstance(v, Struct):
                fields[k] = v.get_fields()
        return fields

    
class StructArray(Struct):
    item_struct = None
    array_size = None
    
    def __init__(self, data, endian='<'):
        if not isinstance(data, (str, bytes)):
            data = data.read(self.size())
        items = []
        isize = self.item_struct.size()
        for i in range(self.array_size):
            d = data[:isize]
            data = data[isize:]
            items.append(self.item_struct(d, endian))
        self.array = items

    def __getitem__(self, i):
        return self.array[i]
        
    @classmethod
    def size(self):
        return self.item_struct.size() * self.array_size

    def __repr__(self, indent=0):
        r = '    '*indent + '%s(\n' % self.__class__.__name__
        for item in self.array:
            r += item.__repr__(indent=indent+1) + ',\n'
        r += '    '*indent + ')'
        return r


def cstr(byt):
    """Convert C string bytes to python string.
    """
    try:
        ind = byt.index(b'\0')
    except ValueError:
        return byt
    return byt[:ind].decode('utf-8', errors='ignore')


class BundleItem(Struct):
    field_info = [
        ('Start', 'i'),
        ('Length', 'i'),
        ('Extension', '8s', cstr),
    ]
    size_check = 16


class BundleHeader(Struct):
    field_info = [
        ('Signature', '8s', cstr),
        ('Version', '32s', cstr),
        ('Time', 'd'),
        ('Items', 'i'),
        ('IsLittleEndian', '12s'),
        ('BundleItems', BundleItem.array(12)),
    ]
    size_check = 256



class TreeNode(Struct):
    """Struct that also represents a node in a Pulse file tree.
    """
    def __init__(self, fh, pul, level=0):
        self.level = level
        self.children = []
        endian = pul.endian
        
        # The record structure in the file may differ from our expected structure
        # due to version differences, so we read the required number of bytes, and
        # then pad or truncate before unpacking the record. This will probably
        # result in corrupt data in some situations..
        realsize = pul.level_sizes[level]
        structsize = self.size()
        data = fh.read(realsize)
        diff = structsize - realsize
        if diff > 0:
            data = data + b'\0'*diff
        else:
            data = data[:structsize]
        
        # initialize struct data
        Struct.__init__(self, data, endian)
        
        # Next read the number of children
        nchild = struct.unpack(endian + 'i', fh.read(4))[0]
            
        level += 1
        if level >= len(pul.rectypes):
            return
        child_rectype = pul.rectypes[level]
        for i in range(nchild):
            self.children.append(child_rectype(fh, pul, level))

    def __getitem__(self, i):
        return self.children[i]
    
    def __len__(self):
        return len(self.children)
    
    def __iter__(self):
        return self.children.__iter__()
    
    def __repr__(self, indent=0):
        # Return a string describing this structure
        ind = '    '*indent
        srep = Struct.__repr__(self, indent)[:-1]  # exclude final parenthese
        srep += ind + '    children = %d,\n' % len(self)
        #srep += ind + 'children = [\n'
        #for ch in self:
            #srep += ch.__repr__(indent=indent+1) + ',\n'
        srep += ind + ')'
        return srep




class TraceRecord(TreeNode):
    field_info = [
        ('Mark', 'i'),
        ('Label', '32s', cstr),
        ('TraceCount', 'i'),
        ('Data', 'i'),
        ('DataPoints', 'i'),
        ('InternalSolution', 'i'),
        ('AverageCount', 'i'),
        ('LeakCount', 'i'),
        ('LeakTraces', 'i'),
        ('DataKind', 'h'),
        ('Filler1', 'h', None),
        ('RecordingMode', 'c'),
        ('AmplIndex', 'c'),
        ('DataFormat', 'c'),
        ('DataAbscissa', 'c'),
        ('DataScaler', 'd'),
        ('TimeOffset', 'd'),
        ('ZeroData', 'd'),
        ('YUnit', '8s', cstr),
        ('XInterval', 'd'),
        ('XStart', 'd'),
        ('XUnit', '8s', cstr),
        ('YRange', 'd'),
        ('YOffset', 'd'),
        ('Bandwidth', 'd'),
        ('PipetteResistance', 'd'),
        ('CellPotential', 'd'),
        ('SealResistance', 'd'),
        ('CSlow', 'd'),
        ('GSeries', 'd'),
        ('RsValue', 'd'),
        ('GLeak', 'd'),
        ('MConductance', 'd'),
        ('LinkDAChannel', 'i'),
        ('ValidYrange', 'c'),
        ('AdcMode', 'c'),
        ('AdcChannel', 'h'),
        ('Ymin', 'd'),
        ('Ymax', 'd'),
        ('SourceChannel', 'i'),
        ('ExternalSolution', 'i'),
        ('CM', 'd'),
        ('GM', 'd'),
        ('Phase', 'd'),
        ('DataCRC', 'i'),
        ('CRC', 'i'),
        ('GS', 'd'),
        ('SelfChannel', 'i'),
        ('Filler2', 'i', None),
    ]
    size_check = 296


class SweepRecord(TreeNode):
    field_info = [
        ('Mark', 'i'),
        ('Label', '32s', cstr),
        ('AuxDataFileOffset', 'i'),
        ('StimCount', 'i'),
        ('SweepCount', 'i'),
        ('Time', 'd'),
        ('Timer', 'd'),
        ('SwUserParams', '4d'),
        ('Temperature', 'd'),
        ('OldIntSol', 'i'),
        ('OldExtSol', 'i'),
        ('DigitalIn', 'h'),
        ('SweepKind', 'h'),
        ('Filler1', 'i', None),
        ('Markers', '4d'),
        ('Filler2', 'i', None),
        ('CRC', 'i'),
    ]
    size_check = 160


class UserParamDescrType(Struct):
    field_info = [
        ('Name', '32s', cstr),
        ('Unit', '8s', cstr),
    ]
    size_check = 40


class AmplifierState(Struct):
    field_info = [
        ('StateVersion', '8s', cstr),
        ('RealCurrentGain', 'd'),
        ('RealF2Bandwidth', 'd'),
        ('F2Frequency', 'd'),
        ('RsValue', 'd'),
        ('RsFraction', 'd'),
        ('GLeak', 'd'),
        ('CFastAmp1', 'd'),
        ('CFastAmp2', 'd'),
        ('CFastTau', 'd'),
        ('CSlow', 'd'),
        ('GSeries', 'd'),
        ('StimDacScale', 'd'),
        ('CCStimScale', 'd'),
        ('VHold', 'd'),
        ('LastVHold', 'd'),
        ('VpOffset', 'd'),
        ('VLiquidJunction', 'd'),
        ('CCIHold', 'd'),
        ('CSlowStimVolts', 'd'),
        ('CCTrackVHold', 'd'),
        ('TimeoutLength', 'd'),
        ('SearchDelay', 'd'),
        ('MConductance', 'd'),
        ('MCapacitance', 'd'),
        ('SerialNumber', '8s', cstr),
        ('E9Boards', 'h'),
        ('CSlowCycles', 'h'),
        ('IMonAdc', 'h'),
        ('VMonAdc', 'h'),
        ('MuxAdc', 'h'),
        ('TstDac', 'h'),
        ('StimDac', 'h'),
        ('StimDacOffset', 'h'),
        ('MaxDigitalBit', 'h'),
        ('SpareInt1', 'h', None),
        ('SpareInt2', 'h', None),
        ('SpareInt3', 'h', None),

        ('AmplKind', 'c'),
        ('IsEpc9N', 'c'),
        ('ADBoard', 'c'),
        ('BoardVersion', 'c'),
        ('ActiveE9Board', 'c'),
        ('Mode', 'c'),
        ('Range', 'c'),
        ('F2Response', 'c'),

        ('RsOn', 'c'),
        ('CSlowRange', 'c'),
        ('CCRange', 'c'),
        ('CCGain', 'c'),
        ('CSlowToTstDac', 'c'),
        ('StimPath', 'c'),
        ('CCTrackTau', 'c'),
        ('WasClipping', 'c'),

        ('RepetitiveCSlow', 'c'),
        ('LastCSlowRange', 'c'),
        ('Locked', 'c'),
        ('CanCCFast', 'c'),
        ('CanLowCCRange', 'c'),
        ('CanHighCCRange', 'c'),
        ('CanCCTracking', 'c'),
        ('HasVmonPath', 'c'),

        ('HasNewCCMode', 'c'),
        ('Selector', 'c'),
        ('HoldInverted', 'c'),
        ('AutoCFast', 'c'),
        ('AutoCSlow', 'c'),
        ('HasVmonX100', 'c'),
        ('TestDacOn', 'c'),
        ('QMuxAdcOn', 'c'),

        ('RealImon1Bandwidth', 'd'),
        ('StimScale', 'd'),

        ('Gain', 'c'),
        ('Filter1', 'c'),
        ('StimFilterOn', 'c'),
        ('RsSlow', 'c'),
        ('Old1', 'c'),
        ('CCCFastOn', 'c'),
        ('CCFastSpeed', 'c'),
        ('F2Source', 'c'),

        ('TestRange', 'c'),
        ('TestDacPath', 'c'),
        ('MuxChannel', 'c'),
        ('MuxGain64', 'c'),
        ('VmonX100', 'c'),
        ('IsQuadro', 'c'),
        ('SpareBool4', 'c', None),
        ('SpareBool5', 'c', None),

        ('StimFilterHz', 'd'),
        ('RsTau', 'd'),
        ('FilterOffsetDac', 'h'),
        ('ReferenceDac', 'h'),
        ('SpareInt6', 'h', None),
        ('SpareInt7', 'h', None),
        ('Spares1', '24s', None),
        
        ('CalibDate', '16s'),
        ('SelHold', 'd'),
        ('Spares2', '32s', None),
    ]
    size_check = 400
    
    
class LockInParams(Struct):
    field_info = [
        ('ExtCalPhase', 'd'),
        ('ExtCalAtten', 'd'),
        ('PLPhase', 'd'),
        ('PLPhaseY1', 'd'),
        ('PLPhaseY2', 'd'),
        ('UsedPhaseShift', 'd'),
        ('UsedAttenuation', 'd'),
        ('Spares2', '8s', None),
        ('ExtCalValid', '?'),
        ('PLPhaseValid', '?'),
        ('LockInMode', 'c'),
        ('CalMode', 'c'),
        ('Spares', '28s', None),
    ]
    size_check = 96


class SeriesRecord(TreeNode):
    field_info = [
        ('Mark', 'i'),
        ('Label', '32s', cstr),
        ('Comment', '80s', cstr),
        ('SeriesCount', 'i'),
        ('NumberSweeps', 'i'),
        ('AmplStateOffset', 'i'),
        ('AmplStateSeries', 'i'),
        ('riesType', 'c'),
        ('Filler1', 'c', None),
        ('Filler2', 'c', None),
        ('Filler3', 'c', None),
        ('Time', 'd'),
        ('PageWidth', 'd'),
        ('SwUserParamDescr', UserParamDescrType.array(4)),
        ('Filler4', '32s', None),
        ('SeUserParams', '4d'),
        ('LockInParams', LockInParams),
        ('AmplifierState', AmplifierState),
        ('Username', '80s', cstr),
        ('UserParamDescr', UserParamDescrType.array(4)),
        ('Filler5', 'i', None),
        ('CRC', 'i'),
    ]
    size_check = 1120


class GroupRecord(TreeNode):
    field_info = [
        ('Mark', 'i'),
        ('Label', '32s', cstr),
        ('Text', '80s', cstr),
        ('ExperimentNumber', 'i'),
        ('GroupCount', 'i'),
        ('CRC', 'i'),
    ]
    size_check = 128


class Pulsed(TreeNode):
    field_info = [
        ('Version', 'i'),
        ('Mark', 'i'),
        ('VersionName', '32s', cstr),
        ('AuxFileName', '80s', cstr),
        ('RootText', '400s', cstr),
        ('StartTime', 'd'),
        ('MaxSamples', 'i'),
        ('CRC', 'i'),
        ('Features', 'h'),
        ('Filler1', 'h', None),
        ('Filler2', 'i', None),
    ]
    size_check = 544
    
    rectypes = [
        None,
        GroupRecord,
        SeriesRecord,
        SweepRecord,
        TraceRecord
    ]
    
    def __init__(self, bundle, offset=0, size=None):
        fh = open(bundle.file_name, 'rb')
        fh.seek(offset)
        
        # read .pul header
        magic = fh.read(4) 
        if magic == b'eerT':
            self.endian = '<'
        elif magic == b'Tree':
            self.endian = '>'
        else:
            raise RuntimeError('Bad file magic: %s' % magic)
        
        levels = struct.unpack(self.endian + 'i', fh.read(4))[0]

        # read size of each level (one int per level)
        self.level_sizes = []
        for i in range(levels):
            size = struct.unpack(self.endian + 'i', fh.read(4))[0]
            self.level_sizes.append(size)
            
        TreeNode.__init__(self, fh, self)


class Data(object):
    def __init__(self, bundle, offset=0, size=None):
        self.bundle = bundle
        self.offset = offset
        
    def __getitem__(self, *args):
        index = args[0]
        assert len(index) == 4
        pul = self.bundle.pul
        trace = pul[index[0]][index[1]][index[2]][index[3]]
        fh = open(self.bundle.file_name, 'rb')
        fh.seek(trace.Data)
        fmt = bytearray(trace.DataFormat)[0]
        dtype = [np.int16, np.int32, np.float16, np.float32][fmt]
        data = np.fromfile(fh, count=trace.DataPoints, dtype=dtype)
        return data * trace.DataScaler + trace.ZeroData


class Bundle(object):
    
    item_classes = {
        '.pul': Pulsed,
        '.dat': Data,
    }
    
    def __init__(self, file_name):
        self.file_name = file_name
        fh = open(file_name, 'rb')
        # Read header assuming little endiam
        endian = '<'
        self.header = BundleHeader(fh, endian)

        # If the header is bad, re-read using big endian
        if self.header.IsLittleEndian[0] == b'\0':
            endian = '>'
            fh.seek(0)
            self.header = BundleHeader(fh, endian)
            
        # Read bundle items
        #self.bundle_items = [Struct(fh, endian + bundle_item[0], bundle_item[1]) for i in range(12)]

        # catalog extensions of bundled items
        self.catalog = {}
        for item in self.header.BundleItems:
            item.instance = None
            ext = item.Extension
            self.catalog[ext] = item
        print(self.catalog)
        fh.close()

    @property
    def pul(self):
        """The Pulsed object from this bundle.
        """
        return self._get_item_instance('.pul')
    
    @property
    def data(self):
        """The Data object from this bundle.
        """
        return self._get_item_instance('.dat')
        
    def _get_item_instance(self, ext):
        if ext not in self.catalog:
            return None
        item = self.catalog[ext]
        if item.instance is None:
            cls = self.item_classes[ext]
            item.instance = cls(self, item.Start, item.Length)
        return item.instance
        
    def __repr__(self):
        return "Bundle(%r)" % list(self.catalog.keys())
