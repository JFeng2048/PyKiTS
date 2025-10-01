#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Jinja2宏和包含功能示例

这个脚本演示了Jinja2模板引擎中宏(macros)和包含(includes)功能的使用方法，
包括如何定义、导入、使用宏，以及如何包含其他模板文件。
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from datetime import datetime


def setup_jinja_environment(templates_dir='../templates'):
    """设置Jinja2环境
    
    Args:
        templates_dir: 模板文件所在目录
        
    Returns:
        Jinja2环境对象
    """
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建模板目录的绝对路径
    templates_path = os.path.join(current_dir, templates_dir)
    
    # 创建Jinja2环境
    env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    return env


def render_macros_example():
    """演示宏的基本使用方法"""
    print("=" * 80)
    print("演示宏的基本使用方法")
    print("=" * 80)
    
    # 设置Jinja2环境
    env = setup_jinja_environment()
    
    # 准备渲染上下文
    context = {
        'title': '宏功能演示',
        'current_time': datetime.now(),
        'users': [
            {'id': 1, 'name': '张三', 'age': 28, 'position': '软件工程师'},
            {'id': 2, 'name': '李四', 'age': 32, 'position': '产品经理'},
            {'id': 3, 'name': '王五', 'age': 45, 'position': '项目经理'}
        ],
        'hobbies': ['阅读', '运动', '音乐', '旅行', '摄影'],
        'progress': 65
    }
    
    # 加载并渲染模板
    template = env.get_template('macros_includes_example.html')
    rendered_content = template.render(**context)
    
    # 保存渲染结果到文件
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_macros_example.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
    
    print(f"宏示例已渲染并保存到: {output_file}")
    print("请在浏览器中打开该文件查看效果。")
    print()


def demonstrate_macro_definition_usage():
    """演示宏的定义和使用"""
    print("=" * 80)
    print("演示宏的定义和使用")
    print("=" * 80)
    
    # 设置Jinja2环境
    env = setup_jinja_environment()
    
    # 定义一个简单的内联宏示例
    inline_macro_template = '''
    {% macro greeting(name, title='先生/女士') %}
        <p>你好，{{ title }} {{ name }}！欢迎访问我们的网站。</p>
    {% endmacro %}
    
    {% macro render_user_card(user) %}
        <div class="user-card">
            <h3>{{ user.name }}</h3>
            <p>年龄: {{ user.age }}</p>
            <p>职位: {{ user.position }}</p>
        </div>
    {% endmacro %}
    
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>内联宏示例</title>
        <style>
            .user-card {
                border: 1px solid #ddd;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h1>内联宏示例</h1>
        
        {{ greeting('张三') }}
        {{ greeting('李四', '工程师') }}
        
        <h2>用户列表</h2>
        {% for user in users %}
            {{ render_user_card(user) }}
        {% endfor %}
    </body>
    </html>
    '''
    
    # 创建模板对象
    template = env.from_string(inline_macro_template)
    
    # 准备渲染上下文
    context = {
        'users': [
            {'id': 1, 'name': '张三', 'age': 28, 'position': '软件工程师'},
            {'id': 2, 'name': '李四', 'age': 32, 'position': '产品经理'}
        ]
    }
    
    # 渲染模板
    rendered_content = template.render(**context)
    
    # 保存渲染结果到文件
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_inline_macros.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
    
    print(f"内联宏示例已渲染并保存到: {output_file}")
    print("这个示例展示了如何在模板中直接定义和使用宏。")
    print()


def demonstrate_macro_imports():
    """演示宏的导入和复用"""
    print("=" * 80)
    print("演示宏的导入和复用")
    print("=" * 80)
    
    # 设置Jinja2环境
    env = setup_jinja_environment()
    
    # 示例模板，导入外部宏文件
    import_macro_template = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>宏导入示例</title>
        <!-- 导入宏文件中的样式 -->
        {% include 'macros/components.html' %}
    </head>
    <body>
        <h1>宏导入示例</h1>
        
        <!-- 从宏文件导入需要的宏 -->
        {% from 'macros/components.html' import button, card, alert, render_table %}
        
        <div style="margin-bottom: 20px;">
            <h2>按钮宏</h2>
            {{ button('默认按钮') }}
            {{ button('主要按钮', type='primary') }}
            {{ button('成功按钮', type='success') }}
        </div>
        
        <div style="margin-bottom: 20px;">
            <h2>卡片宏</h2>
            {{ card(
                title='产品信息',
                content='这是一个使用导入宏创建的卡片组件，展示了产品详细信息。',
                footer='发布日期: 2023-07-15'
            ) }}
        </div>
        
        <div style="margin-bottom: 20px;">
            <h2>警告框宏</h2>
            {{ alert('这是一条提示信息', type='info') }}
            {{ alert('操作成功完成', type='success') }}
        </div>
        
        <div>
            <h2>表格宏</h2>
            {% set headers = ['ID', '产品名称', '价格', '库存'] %}
            {% set rows = [
                ['1', '笔记本电脑', '¥5999', '120'],
                ['2', '智能手机', '¥3999', '200'],
                ['3', '平板电脑', '¥2499', '80']
            ] %}
            {{ render_table(headers, rows) }}
        </div>
    </body>
    </html>
    '''
    
    # 创建模板对象
    template = env.from_string(import_macro_template)
    
    # 渲染模板（此示例不需要额外上下文）
    rendered_content = template.render()
    
    # 保存渲染结果到文件
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_imported_macros.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
    
    print(f"宏导入示例已渲染并保存到: {output_file}")
    print("这个示例展示了如何从外部文件导入宏并在不同模板中复用。")
    print()


def demonstrate_includes():
    """演示包含功能的使用"""
    print("=" * 80)
    print("演示包含功能的使用")
    print("=" * 80)
    
    # 设置Jinja2环境
    env = setup_jinja_environment()
    
    # 示例模板，使用包含功能
    includes_template = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>包含功能示例</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            main {
                min-height: 400px;
                padding: 20px 0;
            }
        </style>
    </head>
    <body>
        <!-- 包含导航栏 -->
        {% include 'includes/navbar.html' %}
        
        <div class="container">
            <main>
                <h1>包含功能示例</h1>
                <p>本页面展示了Jinja2中的包含功能，通过包含可以将页面拆分为多个可复用的部分。</p>
                
                <!-- 条件包含示例 -->
                {% set show_sidebar = true %}
                {% if show_sidebar %}
                    <div style="float: right; width: 300px; margin-left: 20px;">
                        {% include 'includes/sidebar.html' ignore missing %}
                        {% if not env.is_available('includes/sidebar.html') %}
                            <div style="border: 1px dashed #ccc; padding: 15px;">
                                <p>侧边栏内容（模拟数据）</p>
                                <ul>
                                    <li><a href="#">最新文章</a></li>
                                    <li><a href="#">热门话题</a></li>
                                    <li><a href="#">关于我们</a></li>
                                </ul>
                            </div>
                        {% endif %}
                    </div>
                {% endif %}
                
                <div>
                    <h2>主要内容区域</h2>
                    <p>这是页面的主要内容区域。在实际应用中，这里会展示页面的核心信息。</p>
                    <p>通过使用包含功能，我们可以将页面的不同部分（如导航栏、页脚、侧边栏等）拆分成独立的模板文件，使代码更加模块化和可维护。</p>
                </div>
            </main>
        </div>
        
        <!-- 包含页脚 -->
        {% include 'includes/footer.html' %}
    </body>
    </html>
    '''
    
    # 添加一个is_available方法到环境对象，用于检测模板是否存在
    def is_available(template_name):
        try:
            env.get_template(template_name)
            return True
        except:
            return False
    
    env.globals['env'] = type('obj', (object,), {'is_available': is_available})
    
    # 创建模板对象
    template = env.from_string(includes_template)
    
    # 渲染模板
    rendered_content = template.render()
    
    # 保存渲染结果到文件
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_includes_example.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
    
    print(f"包含功能示例已渲染并保存到: {output_file}")
    print("这个示例展示了如何使用包含功能将页面拆分为多个可复用的部分。")
    print()


def demonstrate_advanced_usage():
    """演示宏和包含的高级用法"""
    print("=" * 80)
    print("演示宏和包含的高级用法")
    print("=" * 80)
    
    # 设置Jinja2环境
    env = setup_jinja_environment()
    
    # 添加一些全局函数到环境中
    env.globals['now'] = datetime.now
    env.globals['format_currency'] = lambda x: f"¥{x:.2f}"
    
    # 高级用法模板
    advanced_template = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>宏和包含的高级用法</title>
        {% include 'macros/components.html' %}
        <style>
            .order-summary {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 20px;
                margin: 20px 0;
                background-color: #f9f9f9;
            }
            .product-item {
                border-bottom: 1px solid #eee;
                padding: 10px 0;
            }
            .product-item:last-child {
                border-bottom: none;
            }
        </style>
    </head>
    <body>
        <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
            <h1>宏和包含的高级用法</h1>
            
            <!-- 1. 宏的嵌套使用 -->
            <h2>1. 宏的嵌套使用</h2>
            {% from 'macros/components.html' import card, button, render_table %}
            
            {{ card(
                title='订单摘要',
                content='''
                    <div class="order-summary">
                        <p><strong>订单编号:</strong> {{ order.id }}</p>
                        <p><strong>下单时间:</strong> {{ order.date }}</p>
                        
                        <h3>商品列表</h3>
                        {% set headers = ['商品名称', '单价', '数量', '小计'] %}
                        {% set rows = [] %}
                        {% for item in order.items %}
                            {% set _ = rows.append([item.name, item.price, item.quantity, item.subtotal]) %}
                        {% endfor %}
                        {{ render_table(headers, rows) }}
                        
                        <p style="text-align: right; font-size: 18px;"><strong>总计: {{ order.total }}</strong></p>
                    </div>
                ''',
                footer=button('查看详情', type='primary') ~ ' ' ~ button('打印订单')
            ) }}
            
            <!-- 2. 变量模板名 -->
            <h2>2. 变量模板名</h2>
            {% set template_type = 'welcome' %}
            {% set dynamic_template = 'includes/' ~ template_type ~ '_message.html' %}
            {% include dynamic_template ignore missing %}
            
            {% if not env.is_available(dynamic_template) %}
                <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px;">
                    <p>这是一个动态包含的欢迎消息（模拟数据）</p>
                </div>
            {% endif %}
            
            <!-- 3. 宏与过滤器的结合 -->
            <h2>3. 宏与过滤器的结合</h2>
            {% set products = [
                {'name': '笔记本电脑', 'price': 5999, 'stock': 50},
                {'name': '平板电脑', 'price': 2499, 'stock': 100},
                {'name': '智能手机', 'price': 3999, 'stock': 150}
            ] %}
            
            <p>价格从高到低排序的产品列表：</p>
            {% set sorted_products = products | sort(reverse=true, attribute='price') %}
            {% set headers = ['产品名称', '价格', '库存'] %}
            {% set rows = [] %}
            {% for p in sorted_products %}
                {% set _ = rows.append([p.name, format_currency(p.price), p.stock]) %}
            {% endfor %}
            {{ render_table(headers, rows) }}
            
            <!-- 4. 包含文件中的宏 -->
            <h2>4. 包含文件中的宏</h2>
            {% include 'macros/components.html' %}
            {% from 'macros/components.html' import badge %}
            
            <div style="margin-top: 10px;">
                {{ badge('新品', 'primary') }} {{ badge('热卖', 'success') }} {{ badge('限时折扣', 'warning') }}
            </div>
        </div>
    </body>
    </html>
    '''
    
    # 添加is_available方法到环境对象
    def is_available(template_name):
        try:
            env.get_template(template_name)
            return True
        except:
            return False
    
    env.globals['env'] = type('obj', (object,), {'is_available': is_available})
    
    # 创建模板对象
    template = env.from_string(advanced_template)
    
    # 准备渲染上下文
    context = {
        'order': {
            'id': 'ORD-20230715-001',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'items': [
                {'name': '笔记本电脑', 'price': '¥5999.00', 'quantity': 1, 'subtotal': '¥5999.00'},
                {'name': '无线鼠标', 'price': '¥99.00', 'quantity': 2, 'subtotal': '¥198.00'},
                {'name': '键盘保护膜', 'price': '¥59.00', 'quantity': 1, 'subtotal': '¥59.00'}
            ],
            'total': '¥6256.00'
        }
    }
    
    # 渲染模板
    rendered_content = template.render(**context)
    
    # 保存渲染结果到文件
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output_advanced_usage.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_content)
    
    print(f"高级用法示例已渲染并保存到: {output_file}")
    print("这个示例展示了宏的嵌套使用、变量模板名、宏与过滤器结合等高级用法。")
    print()


def main():
    """主函数，运行所有示例"""
    print("Jinja2宏和包含功能示例")
    print("=" * 80)
    
    # 运行各个示例
    render_macros_example()
    demonstrate_macro_definition_usage()
    demonstrate_macro_imports()
    demonstrate_includes()
    demonstrate_advanced_usage()
    
    print("=" * 80)
    print("所有示例已运行完成！")
    print("请查看examples目录下的output_*.html文件来查看渲染结果。")


if __name__ == "__main__":
    main()