# -*- coding: utf-8 -*-

"""
Jinja2控制结构练习

这个练习将帮助你熟悉Jinja2的控制结构，包括条件语句和循环。
请完成以下任务：

1. 创建Jinja2环境
2. 加载模板文件'control_structures_exercise.html'
3. 准备上下文数据，包含以下变量：
   - users: 一个包含多个用户信息的列表
   - products: 一个包含产品信息的列表
   - categories: 一个包含类别的字典
4. 渲染模板并打印结果
5. 使用不同的循环控制技术（break、continue）处理数据
6. 实现嵌套循环来展示复杂数据结构

完成后运行这个脚本，确保一切正常工作。
"""

from jinja2 import Environment, FileSystemLoader

# TODO: 创建Jinja2环境
env = None

# TODO: 准备上下文数据
users = [
    {'name': '张三', 'age': 28, 'is_active': True, 'role': 'admin'},
    {'name': '李四', 'age': 32, 'is_active': True, 'role': 'user'},
    {'name': '王五', 'age': 25, 'is_active': False, 'role': 'user'},
    {'name': '赵六', 'age': 40, 'is_active': True, 'role': 'manager'},
    # TODO: 添加更多用户数据
]

products = [
    {'name': '笔记本电脑', 'price': 6999, 'stock': 50, 'category': '电子设备'},
    {'name': '智能手机', 'price': 3999, 'stock': 100, 'category': '电子设备'},
    {'name': '办公桌', 'price': 1299, 'stock': 20, 'category': '家具'},
    {'name': '办公椅', 'price': 899, 'stock': 30, 'category': '家具'},
    {'name': 'Python编程书', 'price': 89, 'stock': 150, 'category': '图书'},
    # TODO: 添加更多产品数据
]

categories = {
    '电子设备': ['笔记本电脑', '智能手机', '平板电脑'],
    '家具': ['办公桌', '办公椅', '书架'],
    '图书': ['Python编程书', '数据分析书', '设计书']
}

context = {
    'users': users,
    'products': products,
    'categories': categories,
    # TODO: 添加更多需要的上下文数据
}

# TODO: 加载模板文件'control_structures_exercise.html'
template = None

# TODO: 渲染模板
output = None

# TODO: 打印渲染结果
print("=== 控制结构练习渲染结果开始 ===")
# 在这里打印输出
print("=== 控制结构练习渲染结果结束 ===")

# TODO: 使用from_string方法演示break和continue的使用

print("控制结构练习完成！")