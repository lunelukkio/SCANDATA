"""
Provides a View tkinter GUI suitable for plotting functions that use two 
numerical user inputs.

Contains:
* MPLgraph    A matplotlib backend tkinter widget used by View
* View    A tkinter GUI with two numerical entry boxes and a matplotlib canvas. 
"""

import matplotlib as mpl
import tkinter as tk

mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)  # NavigationToolbar2TkAgg was deprecated
from tkinter import ttk


class MPLgraph(FigureCanvasTkAgg):
    """The canvas-like matplotlib object used by View.

    """
    def __init__(self, figure, parent=None, **options):
        """
        argument:
            figure: a matplotlib.figure.Figure object
        """
        FigureCanvasTkAgg.__init__(self, figure, parent, **options)
        self.figure = figure
        self.add = figure.add_subplot(111)
        # .show() was deprecated and changed to .draw(). See:
        # https://github.com/matplotlib/matplotlib/pull/9275
        self.draw()
        self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self, parent)
        self.toolbar.update()

    def plot(self, x, y):
        """Take two arrays for x and y coordinates and plot the data."""
        self.add.plot(x, y)
        self.figure.canvas.draw()  # DRAW IS CRITICAL TO REFRESH

    def clear(self):
        """Erase the plot."""
        self.add.clear()
        self.figure.canvas.draw()


class View(ttk.Frame):
    """A tkinter GUI with two numerical entry boxes (labeled "base" and 
    "exponent"), and a matplotlib canvas. 
    
    View assumes the controller has an update_view method, that accepts 
    variables in the format:
    
        values = {'base': b, 'exponent': e}

    where b and e are floats, and returns an (x, y) tuple of numpy arrays.
    
    View provides the following methods for external use by the controller: 
    
    * set_values    used to initialize the view
    * clear    clears the MPLgraph plot
    * plot    plots data provided as x, y tuple of numpy arrays
    
    TODO: The view currently allows the controller to be called when widgets are 
    left empty, which results in a ValueError when the model is called. A 
    workaround such as filling empty entry widgets with 0. is required.
    """

    def __init__(self, parent, controller, **options):
        """Create the necessary widgets, and a dict self.values for 
        storing the state of the entry widgets in the format:
            {'base': b, 'exponent': e}
        where b and e are floats.
        
        Requires arguments:
            parent: parent widget
            controller: the object that provides the update_view method
        """
        ttk.Frame.__init__(self, parent, **options)
        self.pack()

        self.parent = parent
        self.controller = controller
        self.values = {}

        self.create_entries()
        self.create_bindings()
        self.create_canvas()

    def create_entries(self):
        """Add entry widgets and associated labels to View, and assign 
        StringVar objects to the entry widgets."""
        self.base_entry = self.add_entry('base')
        self.base = tk.StringVar()
        self.base_entry.config(textvariable=self.base)
        self.base_entry.focus_set()

        self.exponent_entry = self.add_entry('exponent')
        self.exponent = tk.StringVar()
        self.exponent_entry.config(textvariable=self.exponent)

    def add_entry(self, text):
        """Create a label with text=text, and an entry with numerical entry 
        validation; pack them; and return the entry object for future 
        reference.
        
        Argument:
            text:    string that is both the label text and the key for the 
                     self.values dict.
        Returns:
            entry:    The created ttk.Entry object
        """
        ttk.Label(self, text=text).pack(side=tk.LEFT)

        # check on each keypress for numerical entry
        entry = ttk.Entry(self, validate='key')
        entry['validatecommand'] = (self.register(self.is_number_or_empty),
                                    '%P')
        entry['invalidcommand'] = 'bell'  # beep if invalid keypress
        entry.pack(side=tk.LEFT)
        return entry

    def is_number_or_empty(self, entry):
        """Test (e.g. on keypress) to see if entry status is acceptable (either 
        empty, or able to be converted to a float.)
        
        Argument:
            entry: string
        Returns:
            boolean
        """
        return self.is_number(entry) or self.is_empty(entry)

    @staticmethod
    def is_number(entry):
        """Test to see if entry value is a number.
        
         Argument:
            entry: string
        Returns:
            boolean
        """
        try:
            float(entry)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_empty(entry):
        if not entry:
            return True
        return False

    def create_bindings(self):
        """Bind events across all entry widgets"""
        self.bind_class('TEntry', '<FocusIn>',
                        lambda event: self.on_focus_in(event))
        self.bind_class('TEntry', '<Return>',
                        lambda event: self.on_value_entry(event))
        self.bind_class('TEntry', '<Tab>', lambda event: self.on_tab(event))
        self.bind_class('TEntry', '<FocusOut>',
                        lambda event: self.refresh())

    @staticmethod
    def on_focus_in(event):
        """Select the entire contents of entry widget upon focus, for easy 
        editing.
        """
        event.widget.selection_range(0, tk.END)

    def on_value_entry(self, event):
        """When a valid change to the entry is committed, request a view 
        refresh, and set focus on next entry widget."""
        self.refresh()
        self.set_next_focus(event.widget.tk_focusNext())

    def refresh(self):
        """Overwrite self.values and request a plot refresh, but only if an 
        entry's value is changed.
        """
        if self.entry_is_changed():
            self.update_values()
            self.controller.update_view(self.values)

    def entry_is_changed(self):
        """Compare current widget entries to the dictionary of previously 
        stored values.
        
        Returns: Boolean
        """
        if self.current_values() != self.values:
            return True
        return False

    def current_values(self):
        """Get current widget values and store them in a dictionary.
        
        Returns: a dict in self.values format
        """
        return {'base': float(self.base.get()),
                'exponent': float(self.exponent.get())}

    def update_values(self):
        """Overwrite the dictionary of previous entry values with that for 
        the current values."""
        self.values = self.current_values()

    def set_next_focus(self, NextWidget):
        """Starting with NextWidget, traverse the order of widgets until the 
        next Entry widget is found, then set focus to it. Used to ignore all 
        the matplotlib widgets.
        
        Argument:
            NextWidget: a tkinter widget
        """
        if type(NextWidget) is not ttk.Entry:
            self.set_next_focus(NextWidget.tk_focusNext())
        else:
            NextWidget.focus()

    def on_tab(self, event):
        """Wrapper of on_value_entry; required to override the Tab key's 
        default behavior."""
        self.on_value_entry(event)
        return 'break'

    def create_canvas(self):
        """Adds a MPLgraph widget to the bottom of View's parent."""
        self.figure = mpl.figure.Figure(figsize=(5, 4), dpi=100)
        self.canvas = MPLgraph(self.figure, self.parent)
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH)

    # The three methods below provide the interface to the controller
    def set_values(self, values):
        """Used by the controller to initialize the view's entry values and 
        data.
        
        Argument:
            values: a dict in self.values format
        """
        self.base.set(values['base'])
        self.exponent.set(values['exponent'])
        self.values = values

    def clear(self):
        """ Erase the matplotlib canvas."""
        self.canvas.clear()

    def plot(self, x, y):
        """Plot the model's results to the matplotlib canvas.
        
        Arguments:
            x, y: numpy arrays of x and y coordinates
        """
        self.canvas.plot(x, y)


if __name__ == '__main__':
    root = tk.Tk()
    app = View(root, controller=None)
    root.mainloop()
