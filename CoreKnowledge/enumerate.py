# -*- coding:utf-8 -*-
# file:enumerate.py
"""
python enumerate 的用法
"""

items = ['a', 'b', 'c']
# enumerate可以在循环中获取索引和值
#%%
# 遍历列表items，同时获取元素的索引和值
for index, value in enumerate(items):
    print(index, value)

#%%
# enumerate 指定索引值
# 遍历列表items，从索引1开始，同时获取元素的索引和值
for index, value in enumerate(items, start=1):
    print(index, value)

#%%
# 遍历字典dict_items，enumerate默认对字典的键进行枚举
# 此时key为索引值，value为字典的键名
dict_items = {'a': 1, 'b': 2, 'c': 3}
for key, value in enumerate(dict_items):
    print(key, value)


