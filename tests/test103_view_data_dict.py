# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 09:47:44 2024

@author: lunel
"""

import unittest
from SCANDATA.common_class import DataKeySet, ViewDataDict

class Test(unittest.TestCase):
    def test(self):
        key_set = DataKeySet()
        data = ViewDataDict()
        key_set.set_data_key("CONTROLLER", "ROI1")
        print(key_set.key_dict)
        key_set.set_data_key("CONTROLLER", "ROI2")
        print(key_set.key_dict)
        key_set.add_observer(data)
        
        
        key_set.set_data_key("CONTROLLER", "ROI1")
        print(key_set.key_dict)
        
        
        
        """
        view_data.set_view_data("CONTROLLER", "ROI1")
        print(view_data.view_dict)
        view_data.set_view_data_val("ROI1", False)  
        print(view_data.view_dict["CONTROLLER"])
        view_data.set_view_data_val("ROI1")  
        print(view_data.view_dict["CONTROLLER"])
        view_data.set_view_data("CONTROLLER", "ROI1")
        print(view_data.view_dict)
        """

if __name__ == '__main__':
    unittest.main()
    
"""
# キーセットにオブザーバーとして辞書を追加
key_set.add_observer(dict1)
key_set.add_observer(dict2)

# キーセットにキーを追加して、辞書に異なる値を設定
key_set.add_key("key1")
dict1["key1"] = "value1"
dict2["key1"] = "different value1"

# キーセットからキーを削除
key_set.remove_key("key1")

# 辞書の状態を確認
print(dict1)  # {}
print(dict2)  # {}
"""