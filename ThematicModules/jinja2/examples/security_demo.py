#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jinja2 安全性演示

本示例展示了如何在Jinja2中实现和使用各种安全功能，包括：
1. 自动转义与XSS防护
2. 沙箱模式使用
3. 安全过滤器开发
4. 用户输入验证和清理
5. 敏感数据保护
6. 模板文件安全

使用方法：
    python security_demo.py
"""

import os
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2.sandbox import SandboxedEnvironment


def setup_basic_environment(template_dir):
    """
    设置基本的Jinja2环境（包含最小安全配置）
    
    参数:
        template_dir: 模板目录路径
        
    返回:
        Jinja2环境实例
    """
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    return env


def setup_secure_environment(template_dir, debug=False):
    """
    设置安全的Jinja2环境（包含完整安全配置）
    
    参数:
        template_dir: 模板目录路径
        debug: 是否启用调试模式
        
    返回:
        安全配置的Jinja2环境实例
    """
    # 使用沙箱环境
    env = SandboxedEnvironment(
        # 启用自动转义
        autoescape=select_autoescape(['html', 'xml', 'htm']),
        # 设置模板加载器，限制搜索路径
        loader=FileSystemLoader(template_dir, followlinks=False),
        # 配置其他安全选项
        trim_blocks=True,
        lstrip_blocks=True,
        # 调试模式设置
        debug=debug,
        # 限制循环迭代次数
        max_list_iterations=100,
        # 限制递归深度
        recursion_limit=10
    )
    
    # 添加安全的自定义过滤器
    env.filters['safe_truncate'] = safe_truncate_filter
    env.filters['mask_credit_card'] = mask_credit_card_filter
    env.filters['mask_email'] = mask_email_filter
    env.filters['safe_url'] = safe_url_filter
    env.filters['sanitize_html'] = sanitize_html_filter
    
    # 添加安全的全局函数
    env.globals['get_current_time'] = lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    env.globals['is_production'] = not debug
    env.globals['environment_type'] = 'production' if not debug else 'development'
    
    # 限制危险的全局变量访问
    # 这里可以移除或替换任何可能有安全风险的全局变量
    
    return env


def safe_truncate_filter(text, length=100, suffix='...'):
    """
    安全的文本截断过滤器
    先截断文本，然后进行HTML转义
    
    参数:
        text: 要截断的文本
        length: 截断长度
        suffix: 截断后的后缀
        
    返回:
        安全截断后的文本
    """
    from html import escape
    
    if not text:
        return ''
    
    # 转换为字符串
    text_str = str(text)
    
    # 先截断
    if len(text_str) > length:
        truncated = text_str[:length] + suffix
    else:
        truncated = text_str
    
    # 再转义
    return escape(truncated)


def mask_credit_card_filter(card_number):
    """
    信用卡号掩码过滤器
    只显示前4位和后4位，中间用*代替
    
    参数:
        card_number: 信用卡号
        
    返回:
        掩码后的信用卡号
    """
    if not card_number:
        return ''
    
    # 提取所有数字
    import re
    digits = re.sub(r'\D', '', str(card_number))
    
    if len(digits) < 8:
        return '****'
    
    # 只显示前4位和后4位
    masked = digits[:4] + '*' * (len(digits) - 8) + digits[-4:]
    
    # 格式化显示（每4位一组）
    return ' '.join([masked[i:i+4] for i in range(0, len(masked), 4)])


def mask_email_filter(email):
    """
    邮箱地址掩码过滤器
    隐藏部分用户名
    
    参数:
        email: 邮箱地址
        
    返回:
        掩码后的邮箱地址
    """
    if not email:
        return ''
    
    email_str = str(email)
    
    # 检查邮箱格式
    if '@' not in email_str:
        return email_str
    
    username, domain = email_str.split('@', 1)
    
    # 根据用户名长度决定掩码策略
    if len(username) <= 2:
        # 用户名太短，全部掩码
        masked_username = '*' * len(username)
    else:
        # 显示第一个字符，然后掩码中间部分，最后显示最后一个字符
        masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
    
    return masked_username + '@' + domain


def safe_url_filter(url):
    """
    安全的URL过滤器
    移除危险的URL协议
    
    参数:
        url: 要过滤的URL
        
    返回:
        安全的URL或#
    """
    if not url:
        return '#'
    
    url_str = str(url).strip()
    
    # 检查是否有协议
    if ':' in url_str:
        protocol, rest = url_str.split(':', 1)
        protocol = protocol.lower()
        
        # 只允许安全的协议
        allowed_protocols = ['http', 'https', 'ftp', 'ftps', 'mailto', 'tel']
        if protocol not in allowed_protocols:
            return '#"
        
    return url_str


def sanitize_html_filter(html):
    """
    HTML清理过滤器
    移除危险的HTML标签和属性
    
    参数:
        html: 要清理的HTML内容
        
    返回:
        清理后的HTML内容
    """
    if not html:
        return ''
    
    from html import escape
    
    # 简单的HTML清理（实际应用中应使用专门的HTML清理库如bleach）
    # 这里只是一个基础实现，仅用于演示
    
    # 允许的标签白名单
    allowed_tags = {'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                   'b', 'i', 'u', 'strong', 'em', 'br', 'hr', 'ul', 'ol', 'li'}
    
    # 允许的属性白名单
    allowed_attributes = {'href', 'src', 'alt', 'title', 'class', 'id'}
    
    # 转换为字符串
    html_str = str(html)
    
    try:
        # 简单的标签过滤（实际应用中应使用HTML解析库）
        import re
        
        # 转义所有内容
        clean_html = escape(html_str)
        
        # 对于允许的标签，将转义后的标签转回原始标签
        for tag in allowed_tags:
            clean_html = clean_html.replace(f'&lt;{tag}&gt;', f'<{tag}>')
            clean_html = clean_html.replace(f'&lt;/{tag}&gt;', f'</{tag}>')
            
        return clean_html
    except Exception:
        # 出错时返回完全转义的内容
        return escape(html_str)


def sanitize_user_input(input_data, max_length=1000):
    """
    安全处理用户输入
    
    参数:
        input_data: 用户输入的数据
        max_length: 最大允许长度
        
    返回:
        清理后的安全数据
    """
    if input_data is None:
        return ''
    
    # 转换为字符串
    input_str = str(input_data)
    
    # 移除控制字符
    input_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_str)
    
    # 限制长度
    if len(input_str) > max_length:
        input_str = input_str[:max_length] + '...'
    
    return input_str


def validate_template_path(template_name):
    """
    验证模板路径安全性
    防止目录遍历攻击
    
    参数:
        template_name: 模板名称
        
    返回:
        布尔值，表示路径是否安全
    """
    if not template_name:
        return False
    
    # 检查是否包含危险的路径组件
    dangerous_patterns = ['..', '\\', '//', '/.', './']
    for pattern in dangerous_patterns:
        if pattern in template_name:
            return False
    
    # 检查是否以斜杠开头（绝对路径）
    if template_name.startswith('/') or template_name.startswith('\\'):
        return False
    
    # 检查文件扩展名
    allowed_extensions = ['.html', '.htm', '.xml', '.txt']
    _, ext = os.path.splitext(template_name)
    if ext and ext.lower() not in allowed_extensions:
        return False
    
    return True


def get_template_variables():
    """
    获取模板渲染所需的变量
    
    返回:
        包含所有模板变量的字典
    """
    # 示例用户数据（注意：敏感字段已被掩码）
    user = {
        'username': 'demo_user',
        'email': 'user@example.com',
        'registered_at': '2023-01-15',
        # 敏感字段不应传递给模板
        # 'password_hash': '...',  # 不应该出现在模板上下文中
        # 'api_key': '...',        # 不应该出现在模板上下文中
    }
    
    # 恶意输入示例
    malicious_inputs = {
        'user_input': '<script>alert("XSS Attack!");</script>',
        'malicious_url': 'javascript:alert("XSS")',
        'malicious_template_path': '../config/database.yml',
        'restricted_value': {'_hidden': 'secret', 'visible': 'public data'}
    }
    
    # 其他测试数据
    test_data = {
        'credit_card': '1234 5678 9012 3456',
        'email': 'sensitive.user@example.com',
        'long_comment': '这是一个很长的评论，可能包含一些不安全的内容，如 <script>alert(\'XSS\');</script> 标签，我们需要安全地处理它。',
        'user_url': 'https://example.com/user/profile',
        'cache_status': '缓存启用，限制大小: 50 个模板',
        'debug_mode': False,
        'environment_type': 'production',
        'debug_error': '详细的错误信息，包含堆栈跟踪和变量内容（仅开发环境显示）',
        'production_error': '抱歉，处理您的请求时发生错误。请稍后再试。'
    }
    
    # 合并所有变量
    context = {**user, **malicious_inputs, **test_data}
    
    return context


def xss_protection_demo():
    """
    XSS防护演示
    展示自动转义功能和安全过滤器
    """
    print("=" * 80)
    print("XSS防护演示")
    print("=" * 80)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(os.path.dirname(current_dir), 'templates')
    
    # 设置环境
    env = setup_secure_environment(template_dir)
    
    # 测试自动转义
    print("\n1. 自动转义测试:")
    template = env.from_string('''
    原始输入: {{ user_input }}
    使用safe过滤器: {{ user_input|safe }}
    安全截断: {{ user_input|safe_truncate(20) }}
    ''')
    
    result = template.render(
        user_input='<script>alert("XSS Attack!");</script>'
    )
    print(result)
    
    # 测试HTML清理
    print("\n2. HTML清理测试:")
    template = env.from_string('''
    原始HTML: {{ html_content }}
    清理后HTML: {{ html_content|sanitize_html }}
    ''')
    
    result = template.render(
        html_content='<div>安全内容<script>alert("危险脚本");</script></div>'
    )
    print(result)
    
    print("\nXSS防护演示完成！")
    print("=" * 80)


def sandbox_mode_demo():
    """
    沙箱模式演示
    展示沙箱环境的安全限制
    """
    print("=" * 80)
    print("沙箱模式演示")
    print("=" * 80)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(os.path.dirname(current_dir), 'templates')
    
    # 设置沙箱环境
    sandbox_env = SandboxedEnvironment(
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # 设置普通环境用于对比
    normal_env = Environment(
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # 测试危险属性访问
    print("\n1. 危险属性访问测试:")
    test_obj = {'_private': 'secret data', 'public': 'public data'}
    
    # 在普通环境中
    template = normal_env.from_string('普通环境: {{ obj._private }}')
    normal_result = template.render(obj=test_obj)
    print(normal_result)
    
    # 在沙箱环境中
    template = sandbox_env.from_string('沙箱环境: {{ obj._private }}')
    sandbox_result = template.render(obj=test_obj)
    print(sandbox_result)
    
    # 测试限制循环迭代
    print("\n2. 循环迭代限制测试:")
    template = sandbox_env.from_string('''
    {% for i in range(1000) %}
        {% if i % 100 == 0 %}{{ i }}{% endif %}
    {% endfor %}
    ''')
    
    try:
        result = template.render()
        print(f"渲染结果长度: {len(result)} 字符")
    except Exception as e:
        print(f"渲染异常: {e}")
    
    print("\n沙箱模式演示完成！")
    print("=" * 80)


def sensitive_data_protection_demo():
    """
    敏感数据保护演示
    展示敏感数据的掩码和保护
    """
    print("=" * 80)
    print("敏感数据保护演示")
    print("=" * 80)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(os.path.dirname(current_dir), 'templates')
    
    # 设置环境
    env = setup_secure_environment(template_dir)
    
    # 测试敏感数据掩码
    print("\n1. 信用卡号掩码测试:")
    template = env.from_string('''
    原始卡号: {{ credit_card }}
    掩码后: {{ credit_card|mask_credit_card }}
    ''')
    
    result = template.render(
        credit_card='1234 5678 9012 3456'
    )
    print(result)
    
    # 测试邮箱掩码
    print("\n2. 邮箱地址掩码测试:")
    template = env.from_string('''
    原始邮箱: {{ email }}
    掩码后: {{ email|mask_email }}
    ''')
    
    result = template.render(
        email='sensitive.user@example.com'
    )
    print(result)
    
    # 测试URL安全过滤
    print("\n3. URL安全过滤测试:")
    template = env.from_string('''
    安全URL: {{ safe_url|safe_url }}
    危险URL: {{ dangerous_url|safe_url }}
    ''')
    
    result = template.render(
        safe_url='https://example.com',
        dangerous_url='javascript:alert("XSS")'
    )
    print(result)
    
    print("\n敏感数据保护演示完成！")
    print("=" * 80)


def template_file_security_demo():
    """
    模板文件安全演示
    展示模板文件访问控制
    """
    print("=" * 80)
    print("模板文件安全演示")
    print("=" * 80)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(os.path.dirname(current_dir), 'templates')
    
    # 设置环境
    env = setup_secure_environment(template_dir)
    
    # 测试安全的模板路径
    print("\n1. 安全的模板路径测试:")
    safe_template = 'security_example.html'
    if validate_template_path(safe_template):
        try:
            template = env.get_template(safe_template)
            print(f"成功加载模板: {safe_template}")
        except Exception as e:
            print(f"加载模板失败: {e}")
    else:
        print(f"模板路径不安全: {safe_template}")
    
    # 测试不安全的模板路径
    print("\n2. 不安全的模板路径测试:")
    unsafe_template = '../config/database.yml'
    if validate_template_path(unsafe_template):
        try:
            template = env.get_template(unsafe_template)
            print(f"成功加载模板: {unsafe_template}")
        except Exception as e:
            print(f"加载模板失败: {e}")
    else:
        print(f"模板路径不安全: {unsafe_template}")
    
    print("\n模板文件安全演示完成！")
    print("=" * 80)


def comprehensive_demo():
    """
    综合演示
    渲染完整的安全示例模板
    """
    print("=" * 80)
    print("综合安全演示")
    print("=" * 80)
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(os.path.dirname(current_dir), 'templates')
    
    # 设置环境
    env = setup_secure_environment(template_dir, debug=False)  # 生产环境模式
    
    # 获取模板
    try:
        template = env.get_template('security_example.html')
    except Exception as e:
        print(f"加载模板失败: {e}")
        return
    
    # 获取模板变量
    context = get_template_variables()
    
    # 清理所有用户输入
    for key, value in context.items():
        # 假设所有用户提供的值都是字符串类型的输入
        if key not in ['user', 'cache_status', 'debug_mode', 'environment_type']:
            context[key] = sanitize_user_input(value)
    
    # 记录开始时间
    import time
    start_time = time.time()
    
    # 渲染模板
    print("\n渲染安全示例模板...")
    try:
        result = template.render(**context)
    except Exception as e:
        print(f"渲染模板失败: {e}")
        return
    
    # 计算渲染时间
    render_time = time.time() - start_time
    
    # 将结果保存到文件，便于查看
    output_file = os.path.join(current_dir, 'security_example_output.html')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
    except Exception as e:
        print(f"保存输出文件失败: {e}")
        return
    
    print(f"\n渲染完成！耗时: {render_time:.4f}秒")
    print(f"渲染结果已保存到: {output_file}")
    print("请在浏览器中打开该文件查看安全功能效果")
    
    print("\n综合安全演示完成！")
    print("=" * 80)


def main():
    """
    主函数，运行所有安全演示
    """
    print("Jinja2 安全性演示程序")
    print("=" * 80)
    print("本程序展示了Jinja2模板引擎中的各种安全功能和最佳实践")
    print("=" * 80)
    
    try:
        # 运行各个演示
        xss_protection_demo()
        sandbox_mode_demo()
        sensitive_data_protection_demo()
        template_file_security_demo()
        comprehensive_demo()
        
        print("\n所有安全演示运行完成！")
        print("请查看生成的HTML文件以获得完整的安全功能展示。")
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()