#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jinja2基础用法示例

这个示例演示了Jinja2的基本使用流程：
1. 创建Jinja2环境
2. 加载模板
3. 准备上下文数据
4. 渲染模板
5. 输出结果
"""

from jinja2 import Environment, FileSystemLoader
import datetime

# 步骤1: 创建Jinja2环境
# 指定模板目录
env = Environment(
    loader=FileSystemLoader('../templates'),  # 设置模板加载器，从../templates目录加载模板
    autoescape=True  # 自动转义HTML内容，防止XSS攻击
)

# 步骤2: 加载模板
# 从模板目录加载名为'basic_example.html'的模板文件
template = env.get_template('basic_example.html')

# 步骤3: 准备上下文数据
# 创建一个字典，包含要传递给模板的变量
context = {
    'name': '张三',  # 字符串变量
    'age': 30,  # 整数变量
    'hobbies': ['读书', '旅行', '摄影'],  # 列表变量
    'user': {  # 字典变量
        'username': 'zhangsan',
        'email': 'zhangsan@example.com'
    },
    'html_content': '<strong>This is bold text</strong>',  # 包含HTML的内容
    'current_date': datetime.datetime.now(),  # 日期时间对象
    # 'optional_value': 'This is optional'  # 这个变量被注释掉了，将使用默认值
}

# 步骤4: 渲染模板
# 使用上下文数据渲染模板，生成最终的输出内容
output = template.render(**context)

# 步骤5: 输出结果
# 将渲染结果打印到控制台
print("=== 渲染结果开始 ===")
print(output)
print("=== 渲染结果结束 ===")

# 可选：将渲染结果保存到文件
with open('rendered_basic_example.html', 'w', encoding='utf-8') as f:
    f.write(output)

print("渲染结果已保存到 'rendered_basic_example.html' 文件")

# 其他基础用法演示
print("\n=== 其他基础用法演示 ===")

# 1. 直接渲染字符串模板
simple_template = env.from_string("Hello, {{ name }}! Welcome to Jinja2.")
simple_output = simple_template.render(name='李四')
print("字符串模板渲染结果:", simple_output)

# 2. 使用基本表达式
expr_template = env.from_string("2 + 3 = {{ 2 + 3 }}, Your age next year: {{ age + 1 }}")
expr_output = expr_template.render(age=25)
print("表达式模板渲染结果:", expr_output)

# 3. 访问列表和字典元素
access_template = env.from_string(
    "First hobby: {{ hobbies[0] }}, Email: {{ user.email }}"
)
access_output = access_template.render(
    hobbies=['编程', '音乐'],
    user={'email': 'example@test.com'}
)
print("访问数据结构模板渲染结果:", access_output)

print("\n基础用法示例演示完成！")