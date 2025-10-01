#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jinja2扩展功能演示

本示例展示了如何在Jinja2中开发和使用自定义扩展，包括：
1. 文本处理扩展：提供文本截断、高亮、slugify等功能
2. 重复标签扩展：提供{% repeat %}标签用于循环执行代码块
3. 缓存块扩展：提供{% cache %}标签用于缓存模板块
4. 调试扩展：提供调试工具和信息显示功能

使用方法：
    python extensions_demo.py
"""

import os
import sys
import time
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

# 确保可以导入自定义扩展
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入我们创建的扩展
from examples.jinja2_extensions import (
    TextProcessingExtension,
    RepeatExtension,
    CacheBlockExtension,
    DebugExtension
)


def setup_environment(debug=False):
    """
    设置Jinja2环境并加载所有扩展
    
    参数:
        debug: 是否启用调试模式
        
    返回:
        配置好的Jinja2环境实例
    """
    # 获取模板目录路径
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
    
    # 创建Jinja2环境
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True,
        debug=debug  # 设置调试模式
    )
    
    # 注册扩展
    env.add_extension(TextProcessingExtension)
    env.add_extension(RepeatExtension)
    env.add_extension(CacheBlockExtension)
    env.add_extension(DebugExtension)
    
    # 配置缓存块扩展
    if hasattr(env, 'cache'):
        env.cache = {}
    else:
        # 如果环境没有cache属性，创建一个
        setattr(env, 'cache', {})
    
    # 配置缓存过期时间（秒）
    env.cache_timeout = 300  # 默认5分钟
    
    return env


def get_template_variables():
    """
    获取模板渲染所需的变量
    
    返回:
        包含所有模板变量的字典
    """
    # 示例产品数据
    products = [
        {'id': 1, 'name': 'Jinja2入门指南', 'description': '全面介绍Jinja2模板引擎的基础知识和使用方法', 'price': '¥59.90', 'stock': 10},
        {'id': 2, 'name': '高级模板设计模式', 'description': '探索现代Web应用中的高级模板设计和最佳实践', 'price': '¥89.90', 'stock': 5},
        {'id': 3, 'name': '模板性能优化', 'description': '学习如何优化模板渲染性能，提升Web应用响应速度', 'price': '¥79.90', 'stock': 0},
        {'id': 4, 'name': '模板安全与防御', 'description': '了解模板安全问题和防御措施，避免常见的安全漏洞', 'price': '¥69.90', 'stock': 8}
    ]
    
    # 其他模板变量
    context = {
        'long_text': 'Jinja2是一个功能强大的Python模板引擎，它允许开发者在HTML、XML或其他标记语言中嵌入Python代码。'\
                   'Jinja2的模板系统支持变量替换、条件判断、循环、过滤器、宏等多种功能，'\
                   '使得前端页面的开发更加灵活和高效。在现代Web应用开发中，Jinja2被广泛应用于各种Python Web框架。',
        'page_title': 'Jinja2扩展功能 - 模板引擎的高级特性',
        'item_count': 3,
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': 'user_12345',
        'products': products,
        'page_num': 1,
        'total_pages': 3
    }
    
    return context


def basic_extensions_demo():
    """
    基础扩展示演示
    展示如何使用文本处理扩展和重复标签扩展
    """
    print("=" * 80)
    print("基础扩展示演示")
    print("=" * 80)
    
    # 设置环境
    env = setup_environment()
    
    # 测试文本处理扩展
    print("\n1. 文本处理扩展测试:")
    template = env.from_string('''
    原始文本: {{ text }}
    截断到10个词: {{ text | truncate_words(10) }}
    高亮关键词: {{ text | highlight(['Jinja2', '模板']) }}
    生成Slug: {{ title | slugify }}
    ''')
    
    result = template.render(
        text="Jinja2是一个功能强大的Python模板引擎，可以创建动态内容的HTML页面。",
        title="Jinja2扩展功能 - 高级教程"
    )
    print(result)
    
    # 测试重复标签扩展
    print("\n2. 重复标签扩展测试:")
    template = env.from_string('''
    {% repeat 3 %}
        迭代 {{ loop.index }}: {{ loop.first ? '第一个' : loop.last ? '最后一个' : '中间的' }}\n    {% endrepeat %}
    ''')
    
    result = template.render()
    print(result)
    
    print("\n基础扩展示演示完成！")
    print("=" * 80)


def cache_block_demo():
    """
    缓存块扩展示演示
    展示缓存块的使用和效果
    """
    print("=" * 80)
    print("缓存块扩展示演示")
    print("=" * 80)
    
    # 设置环境
    env = setup_environment()
    
    # 创建一个简单的模板
    template = env.from_string('''
    {% cache 'demo_block' %}
        缓存生成时间: {{ time }}
    {% endcache %}
    ''')
    
    # 第一次渲染，应该生成新缓存
    print("\n第一次渲染（生成缓存）:")
    result1 = template.render(time=datetime.now().strftime('%H:%M:%S.%f'))
    print(result1)
    
    # 等待一段时间，但不超过缓存过期时间
    time.sleep(1)
    
    # 第二次渲染，应该使用缓存
    print("\n第二次渲染（使用缓存）:")
    result2 = template.render(time=datetime.now().strftime('%H:%M:%S.%f'))
    print(result2)
    
    # 清除特定缓存
    print("\n清除特定缓存后:")
    if hasattr(env, 'cache') and 'demo_block' in env.cache:
        del env.cache['demo_block']
    
    # 第三次渲染，应该重新生成缓存
    result3 = template.render(time=datetime.now().strftime('%H:%M:%S.%f'))
    print(result3)
    
    print("\n缓存块扩展示演示完成！")
    print("=" * 80)


def debug_extension_demo():
    """
    调试扩展示演示
    展示调试扩展的各种功能
    """
    print("=" * 80)
    print("调试扩展示演示")
    print("=" * 80)
    
    # 设置环境，启用调试模式
    env = setup_environment(debug=True)
    
    # 创建一个包含调试功能的模板
    template = env.from_string('''
    {% debug 'test_section' %}
        这是一个调试区块
        {{ complex_data | debug_print('复杂数据') }}
        类型: {{ complex_data | type_of }}
        {{ dump_data | dump }}
    {% enddebug %}
    
    {% timeit 'loop_operation' %}
        {% for i in range(1000) %}
            {% if i % 100 == 0 %}
                计数: {{ i }}\n            {% endif %}
        {% endfor %}
    {% endtimeit %}
    
    环境配置: {{ get_env_config() | json_debug }}
    ''')
    
    # 渲染模板
    print("\n渲染包含调试功能的模板:")
    result = template.render(
        complex_data={'name': '测试对象', 'items': [1, 2, 3], 'nested': {'a': 1, 'b': 2}},
        dump_data="这是要转储的数据"
    )
    
    # 在实际应用中，调试信息通常会添加到渲染结果的HTML注释中
    # 这里我们直接打印部分调试输出
    print("调试信息已添加到渲染结果中")
    
    print("\n调试扩展示演示完成！")
    print("=" * 80)


def comprehensive_demo():
    """
    综合演示
    渲染完整的扩展示例模板
    """
    print("=" * 80)
    print("综合演示")
    print("=" * 80)
    
    # 设置环境
    env = setup_environment(debug=True)
    
    # 获取模板
    template = env.get_template('extensions_example.html')
    
    # 获取模板变量
    context = get_template_variables()
    
    # 记录开始时间
    start_time = time.time()
    
    # 渲染模板
    print("\n渲染扩展示例模板...")
    result = template.render(**context)
    
    # 计算渲染时间
    render_time = time.time() - start_time
    
    # 将结果保存到文件，便于查看
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extensions_example_output.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"\n渲染完成！耗时: {render_time:.4f}秒")
    print(f"渲染结果已保存到: {output_file}")
    print("请在浏览器中打开该文件查看效果")
    
    print("\n综合演示完成！")
    print("=" * 80)


def main():
    """
    主函数，运行所有演示
    """
    print("Jinja2扩展功能演示程序")
    print("=" * 80)
    
    try:
        # 运行各个演示
        basic_extensions_demo()
        cache_block_demo()
        debug_extension_demo()
        comprehensive_demo()
        
        print("\n所有演示运行完成！")
        print("请查看生成的HTML文件以获得完整的扩展功能展示。")
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()