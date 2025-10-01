from jinja2 import Environment, FileSystemLoader
import datetime
import os

# 配置Jinja2环境
def setup_environment(templates_dir='../templates'):
    """设置Jinja2环境，加载指定目录下的模板"""
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True
    )
    return env

# 准备示例数据
def prepare_context_data():
    """准备用于模板渲染的上下文数据"""
    # 基本用户信息
    user = {
        'username': '张三',
        'is_authenticated': True,
        'is_admin': False
    }
    
    # 消息提示
    messages = [
        {'type': 'success', 'text': '欢迎来到Jinja2学习中心！'},
        {'type': 'info', 'text': '今天学习了模板继承，收获很大！'}
    ]
    
    # 完整上下文数据
    context = {
        'user': user,
        'messages': messages,
        'current_time': datetime.datetime.now(),
        'year': datetime.datetime.now().year,
        'page_title': 'Jinja2模板继承示例'
    }
    
    return context

# 渲染并保存模板
def render_and_save_template(env, template_name, context, output_filename):
    """渲染指定的模板并保存到文件"""
    # 确保输出目录存在
    os.makedirs('../output', exist_ok=True)
    
    # 渲染模板
    template = env.get_template(template_name)
    rendered_content = template.render(**context)
    
    # 保存到文件
    output_path = os.path.join('../output', output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
    
    print(f"模板 '{template_name}' 已成功渲染并保存到 '{output_path}'")
    
    return rendered_content

# 演示基本的模板继承
def demonstrate_basic_inheritance(env, context):
    """演示基本的模板继承概念"""
    print("=== 基本模板继承演示 ===")
    print("1. 渲染基础模板 base.html")
    base_output = render_and_save_template(env, 'base.html', context, 'base_output.html')
    
    print("\n2. 渲染首页模板 home.html (继承自 base.html)")
    home_output = render_and_save_template(env, 'home.html', context, 'home_output.html')
    
    print("\n3. 渲染关于页面模板 about.html (继承自 base.html)")
    about_output = render_and_save_template(env, 'about.html', context, 'about_output.html')
    
    print("\n模板继承关系：")
    print("- home.html -> base.html")
    print("- about.html -> base.html")
    print()

# 演示块的覆盖和继承
def demonstrate_block_usage(env, context):
    """演示模板中块的覆盖和继承"""
    print("=== 块的覆盖和继承演示 ===")
    
    # 创建一个简单的子模板字符串
    simple_child_template = """
{% extends "base.html" %}

{% block title %}简单子模板{% endblock %}

{% block content %}
<div class="card">
    <h2>这是一个简单的子模板</h2>
    <p>它继承了基础模板的结构，但覆盖了content块。</p>
    <p>当前时间: {{ current_time.strftime('%Y-%m-%d %H:%M:%S') }}</p>
</div>
{% endblock %}
"""
    
    # 渲染并保存这个简单的子模板
    simple_template = env.from_string(simple_child_template)
    simple_output = simple_template.render(**context)
    
    # 保存到文件
    output_path = os.path.join('../output', 'simple_child_output.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(simple_output)
    
    print("1. 创建了一个简单的子模板，仅覆盖了title和content块")
    print(f"   已保存到 '{output_path}'")
    
    # 创建一个使用super()的子模板
    super_child_template = """
{% extends "base.html" %}

{% block title %}使用super()的子模板{% endblock %}

{% block css %}
    {{ super() }}
    <style>
        .highlight { background-color: #ffeb3b; padding: 2px 5px; }
    </style>
{% endblock %}

{% block content %}
    {{ super() }}
    <div class="card highlight">
        <h2>这是使用super()的子模板</h2>
        <p>它保留了基础模板的content内容，并添加了新的内容。</p>
        <p>使用<code>{{ super() }}</code>可以继承父模板中块的内容。</p>
    </div>
{% endblock %}
"""
    
    # 渲染并保存这个使用super()的子模板
    super_template = env.from_string(super_child_template)
    super_output = super_template.render(**context)
    
    # 保存到文件
    output_path = os.path.join('../output', 'super_child_output.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(super_output)
    
    print("2. 创建了一个使用super()的子模板，保留了父模板的内容")
    print(f"   已保存到 '{output_path}'")
    print()

# 演示包含指令的使用
def demonstrate_include_usage(env, context):
    """演示include指令的使用"""
    print("=== include指令演示 ===")
    
    # 创建一个使用include的模板
    include_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Include指令演示</title>
</head>
<body>
    <h1>Include指令演示</h1>
    
    <div class="container">
        <p>下面包含了导航栏组件：</p>
        {% include "includes/navbar.html" %}
        
        <p>下面包含了页脚组件：</p>
        {% include "includes/footer.html" %}
    </div>
</body>
</html>
"""
    
    # 渲染并保存这个使用include的模板
    include_template_obj = env.from_string(include_template)
    include_output = include_template_obj.render(**context)
    
    # 保存到文件
    output_path = os.path.join('../output', 'include_demo.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(include_output)
    
    print("创建了一个使用include指令的模板")
    print("include指令允许在模板中包含其他模板片段，提高代码复用性")
    print(f"已保存到 '{output_path}'")
    print()

# 主函数
def main():
    """主函数，运行所有模板继承示例"""
    print("===== Jinja2模板继承演示 =====")
    
    # 设置环境
    env = setup_environment()
    
    # 准备上下文数据
    context = prepare_context_data()
    
    # 运行各种示例
    demonstrate_basic_inheritance(env, context)
    demonstrate_block_usage(env, context)
    demonstrate_include_usage(env, context)
    
    print("\n===== 演示完成 =====")
    print("所有渲染的HTML文件都保存在 ../output 目录中")
    print("你可以在浏览器中打开这些文件查看渲染结果")

if __name__ == '__main__':
    main()