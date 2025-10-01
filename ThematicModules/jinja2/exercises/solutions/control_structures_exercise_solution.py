# -*- coding: utf-8 -*-

"""
Jinja2控制结构练习解决方案

这是控制结构练习的参考解决方案。
"""

from jinja2 import Environment, FileSystemLoader

# 创建Jinja2环境
env = Environment(
    loader=FileSystemLoader('../../templates'),
    autoescape=True
)

# 准备上下文数据
users = [
    {'name': '张三', 'age': 28, 'is_active': True, 'role': 'admin'},
    {'name': '李四', 'age': 32, 'is_active': True, 'role': 'user'},
    {'name': '王五', 'age': 25, 'is_active': False, 'role': 'user'},
    {'name': '赵六', 'age': 40, 'is_active': True, 'role': 'manager'},
    {'name': '孙七', 'age': 35, 'is_active': True, 'role': 'user'},
    {'name': '周八', 'age': 22, 'is_active': False, 'role': 'user'}
]

products = [
    {'name': '笔记本电脑', 'price': 6999, 'stock': 50, 'category': '电子设备'},
    {'name': '智能手机', 'price': 3999, 'stock': 100, 'category': '电子设备'},
    {'name': '办公桌', 'price': 1299, 'stock': 20, 'category': '家具'},
    {'name': '办公椅', 'price': 899, 'stock': 30, 'category': '家具'},
    {'name': 'Python编程书', 'price': 89, 'stock': 150, 'category': '图书'},
    {'name': '平板电脑', 'price': 2499, 'stock': 15, 'category': '电子设备'},
    {'name': '书架', 'price': 599, 'stock': 8, 'category': '家具'},
    {'name': '数据分析书', 'price': 129, 'stock': 45, 'category': '图书'}
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
    'page_title': '控制结构练习',
    'current_year': 2025
}

# 加载模板文件'control_structures_exercise.html'
template = env.get_template('control_structures_exercise.html')

# 渲染模板
output = template.render(**context)

# 打印渲染结果
print("=== 控制结构练习渲染结果开始 ===")
print(output)
print("=== 控制结构练习渲染结果结束 ===")

# 将渲染结果保存到文件
with open('../rendered_control_structures_exercise.html', 'w', encoding='utf-8') as f:
    f.write(output)

# 使用from_string方法演示break和continue的使用
print("\n=== break和continue示例 ===")

# break示例
break_template = env.from_string("""
查找第一个价格超过5000的产品:
{% for product in products %}
  {% if product.price > 5000 %}
    找到了: {{ product.name }} - ¥{{ product.price }}
    {% break %}
  {% endif %}
  跳过: {{ product.name }}
{% endfor %}
""")

# continue示例
continue_template = env.from_string("""
列出所有有库存的电子设备产品:
{% for product in products %}
  {% if product.stock == 0 %}
    {% continue %}
  {% endif %}
  {% if product.category == '电子设备' %}
    {{ product.name }} - ¥{{ product.price }} (库存: {{ product.stock }})
  {% endif %}
{% endfor %}
""")

# 渲染并打印结果
print(break_template.render(products=products))
print(continue_template.render(products=products))

print("控制结构练习完成！")