# -*- coding: utf-8 -*-

"""
Jinja2基础语法练习解决方案

这是基础语法练习的参考解决方案。
"""

from jinja2 import Environment, FileSystemLoader
import datetime

# 创建Jinja2环境，设置模板加载器和自动转义
env = Environment(
    loader=FileSystemLoader('../../templates'),  # 设置模板加载器，从../../templates目录加载模板
    autoescape=True  # 自动转义HTML内容，防止XSS攻击
)

# 加载模板文件'basic_exercise.html'
template = env.get_template('basic_exercise.html')

# 准备上下文数据
context = {
    'name': '张三',
    'age': 28,
    'skills': ['Python', 'JavaScript', 'HTML/CSS', '数据分析'],
    'contact': {
        'email': 'zhangsan@example.com',
        'phone': '13812345678'
    },
    'current_time': datetime.datetime.now()
}

# 渲染模板
output = template.render(**context)

# 打印渲染结果
print("=== 渲染结果开始 ===")
print(output)
print("=== 渲染结果结束 ===")

# 将渲染结果保存到文件
with open('../rendered_basic_exercise.html', 'w', encoding='utf-8') as f:
    f.write(output)

print("渲染结果已保存到 '../rendered_basic_exercise.html' 文件")

# 使用from_string方法直接渲染一个简单的字符串模板
simple_template = env.from_string("你好, {{ name }}! 你有 {{ skills|length }} 项技能。")
simple_output = simple_template.render(**context)
print("字符串模板渲染结果:", simple_output)

print("基础语法练习完成！")