#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jinja2变量和过滤器示例

这个示例演示了Jinja2中各种变量类型的使用和过滤器的应用：
1. 不同类型变量的定义和访问
2. 字符串过滤器的使用
3. 数字过滤器的使用
4. 列表和字典过滤器的使用
5. 日期和时间过滤器的使用
6. 过滤器的链式调用
"""

from jinja2 import Environment, FileSystemLoader
import datetime

# 创建Jinja2环境
env = Environment(
    loader=FileSystemLoader('../templates'),  # 设置模板加载器
    autoescape=True  # 自动转义HTML内容
)

# 加载模板
template = env.get_template('filters_example.html')

# 准备上下文数据，包含各种类型的变量和值
context = {
    # 基本字符串变量
    'message': 'hello world',
    'spaced_message': '  hello world  ',
    'raw_string': '  hello world  ',
    'html_content': '<strong>This is bold and <em>emphasized</em> text</strong>',
    
    # 数字变量
    'negative_number': -42,
    'pi': 3.14159265359,
    'string_number': '123',
    'string_float': '3.14',
    
    # 列表变量
    'numbers': [1, 2, 3, 4, 5],
    'unsorted_numbers': [5, 2, 8, 1, 3],
    'hobbies': ['读书', '旅行', '摄影', '编程'],
    
    # 字典变量
    'user': {
        'username': 'zhangsan',
        'email': 'zhangsan@example.com',
        'age': 30,
        'is_admin': True
    },
    'unsorted_dict': {
        'c': 3,
        'a': 1,
        'b': 2
    },
    
    # 日期时间变量
    'now': datetime.datetime.now(),
    
    # 这个变量故意不定义，用于测试default过滤器
    # 'undefined_var': '这个变量不存在'
}

# 渲染模板
output = template.render(**context)

# 输出渲染结果到控制台
print("=== 渲染结果开始 ===")
print(output)
print("=== 渲染结果结束 ===")

# 将渲染结果保存到文件
with open('rendered_filters_example.html', 'w', encoding='utf-8') as f:
    f.write(output)

print("渲染结果已保存到 'rendered_filters_example.html' 文件")

# 其他过滤器用法演示
print("\n=== 其他过滤器用法演示 ===")

# 1. 字符串过滤器演示
simple_str = "  hello jinja2 world  "
print(f"原始字符串: '{simple_str}'")
print(f"upper: '{env.from_string("{{ s|upper }}").render(s=simple_str)}'")
print(f"lower: '{env.from_string("{{ s|lower }}").render(s=simple_str)}'")
print(f"capitalize: '{env.from_string("{{ s|capitalize }}").render(s=simple_str)}'")
print(f"title: '{env.from_string("{{ s|title }}").render(s=simple_str)}'")
print(f"trim: '{env.from_string("{{ s|trim }}").render(s=simple_str)}'")
print(f"length: {env.from_string("{{ s|length }}").render(s=simple_str)}")
print(f"replace: '{env.from_string("{{ s|replace('world', 'everyone') }}").render(s=simple_str)}'")

# 2. 列表过滤器演示
sample_list = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"\n原始列表: {sample_list}")
print(f"first: {env.from_string("{{ l|first }}").render(l=sample_list)}")
print(f"last: {env.from_string("{{ l|last }}").render(l=sample_list)}")
print(f"length: {env.from_string("{{ l|length }}").render(l=sample_list)}")
print(f"sort: {env.from_string("{{ l|sort }}").render(l=sample_list)}")
print(f"join: '{env.from_string("{{ l|join(', ') }}").render(l=sample_list)}'")

# 3. 过滤器链式调用演示
print(f"\n链式调用示例:")
print(f"原始字符串: '{simple_str}'")
print(f"trim|title|replace: '{env.from_string("{{ s|trim|title|replace('World', 'Everyone') }}").render(s=simple_str)}'")

print("\n变量和过滤器示例演示完成！")