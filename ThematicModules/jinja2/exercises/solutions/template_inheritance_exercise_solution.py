# -*- coding: utf-8 -*-

"""
Jinja2模板继承练习解决方案

这是模板继承练习的参考解决方案。
"""

from jinja2 import Environment, FileSystemLoader

# 创建Jinja2环境
env = Environment(
    loader=FileSystemLoader('../../templates'),
    autoescape=True
)

# 准备上下文数据
context = {
    'page_title': 'Jinja2模板继承练习',
    'site_name': 'Jinja2学习中心',
    'navigation': [
        {'name': '首页', 'url': '/'},
        {'name': '教程', 'url': '/tutorials'},
        {'name': '练习', 'url': '/exercises'},
        {'name': '资源', 'url': '/resources'}
    ],
    'content': '这是页面的主要内容，在子模板中定义。通过模板继承，我们可以复用基础模板的结构，同时定制特定部分的内容。',
    'footer_text': '© 2025 Jinja2学习中心 - 版权所有'
}

# 加载子模板文件'child_exercise.html'
template = env.get_template('child_exercise.html')

# 渲染模板
output = template.render(**context)

# 打印渲染结果
print("=== 模板继承练习渲染结果开始 ===")
print(output)
print("=== 模板继承练习渲染结果结束 ===")

# 将渲染结果保存到文件
with open('../rendered_child_exercise.html', 'w', encoding='utf-8') as f:
    f.write(output)

print("渲染结果已保存到 '../rendered_child_exercise.html' 文件")

# 创建并渲染另一个子模板 - 我们可以直接在代码中定义
print("\n=== 创建并渲染另一个子模板 ===")

# 定义一个新的子模板内容
another_child_template = env.from_string("""
{% extends "base_exercise.html" %}

{% block title %}高级模板继承示例{% endblock %}

{% block header_subtitle %}高级功能演示{% endblock %}

{% block navigation %}
{{ super() }}
<li><a href="/advanced">高级功能</a></li>
{% endblock %}

{% block styles %}
{{ super() }}
<style>
    .advanced-feature {
        background-color: #e3f2fd;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .feature-title {
        color: #1976d2;
        font-weight: bold;
    }
</style>
{% endblock %}

{% block content %}
<div class="content-box">
    <h2>高级模板继承功能</h2>
    
    <div class="advanced-feature">
        <div class="feature-title">嵌套块</div>
        <p>Jinja2支持嵌套块，允许更精细地控制模板的各个部分。</p>
    </div>
    
    <div class="advanced-feature">
        <div class="feature-title">条件继承</div>
        <p>你可以根据条件选择不同的基础模板：</p>
        <pre>{% raw %}{% extends request.is_logged_in ? "user.html" : "guest.html" %}{% endraw %}</pre>
    </div>
    
    <div class="advanced-feature">
        <div class="feature-title">包含文件</div>
        <p>除了继承，还可以使用include来包含其他模板片段：</p>
        <pre>{% raw %}{% include "sidebar.html" %}{% endraw %}</pre>
    </div>
</div>
{% endblock %}

{% block footer %}
{{ super() }}
<p>高级模板功能演示 - 版权所有</p>
{% endblock %}
""")

# 渲染第二个子模板
another_output = another_child_template.render(**context)
print("第二个子模板渲染结果:")
print(another_output)

# 保存第二个渲染结果
with open('../rendered_advanced_exercise.html', 'w', encoding='utf-8') as f:
    f.write(another_output)

print("第二个渲染结果已保存到 '../rendered_advanced_exercise.html' 文件")

print("模板继承练习完成！")