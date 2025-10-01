"""
Jinja2上下文和环境配置示例

本示例演示了Jinja2模板引擎中上下文数据和环境配置的使用方法，包括：
- 基本上下文变量的传递和使用
- 全局上下文变量的定义和使用
- 自定义过滤器的创建和应用
- 自定义测试的实现和使用
- 全局函数的添加和调用
- 环境配置选项的设置
- 缓存策略的配置
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import datetime
import re
import random
import json
import hashlib
import markdown

# 确保中文正常显示
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class CustomJinja2Environment(Environment):
    """自定义Jinja2环境类，扩展默认功能"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 添加自定义功能
        self.add_custom_features()
    
    def add_custom_features(self):
        """添加自定义过滤器、测试和全局函数"""
        # 添加自定义过滤器
        self.filters['uppercase'] = lambda s: s.upper() if isinstance(s, str) else s
        self.filters['reverse_string'] = lambda s: s[::-1] if isinstance(s, str) else s
        self.filters['currency'] = format_currency
        self.filters['percentage'] = format_percentage
        self.filters['capitalize_list'] = capitalize_list
        self.filters['format_date'] = format_date
        self.filters['relative_time'] = relative_time
        self.filters['render_markdown'] = render_markdown
        self.filters['to_json'] = to_json
        self.filters['encrypt'] = simple_encrypt
        self.filters['url_encode'] = url_encode
        
        # 添加自定义测试
        self.tests['even'] = is_even
        self.tests['prime'] = is_prime
        self.tests['list'] = lambda x: isinstance(x, list)
        self.tests['dict'] = lambda x: isinstance(x, dict)
        self.tests['string'] = lambda x: isinstance(x, str)
        self.tests['contains'] = contains
        self.tests['in_range'] = in_range
        
        # 添加全局函数
        self.globals['now'] = get_current_time
        self.globals['random'] = generate_random

# 自定义过滤器函数
def format_currency(value, symbol='¥'):
    """格式化货币显示"""
    try:
        return f"{symbol}{float(value):.2f}"
    except (ValueError, TypeError):
        return value

def format_percentage(value, decimals=2):
    """格式化百分比显示"""
    try:
        return f"{(float(value) * 100):.{decimals}f}%"
    except (ValueError, TypeError):
        return value

def capitalize_list(lst):
    """将列表中的字符串首字母大写"""
    if not isinstance(lst, list):
        return lst
    return [item.capitalize() if isinstance(item, str) else item for item in lst]

def format_date(date_obj, format_str='%Y-%m-%d %H:%M:%S'):
    """格式化日期时间"""
    if isinstance(date_obj, datetime.datetime):
        return date_obj.strftime(format_str)
    return date_obj

def relative_time(date_obj):
    """计算相对时间"""
    if not isinstance(date_obj, datetime.datetime):
        return date_obj
    now = datetime.datetime.now()
    diff = now - date_obj
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)}秒前"
    elif seconds < 3600:
        return f"{int(seconds/60)}分钟前"
    elif seconds < 86400:
        return f"{int(seconds/3600)}小时前"
    else:
        return f"{int(seconds/86400)}天前"

def render_markdown(text):
    """渲染Markdown文本为HTML"""
    if not isinstance(text, str):
        return text
    return markdown.markdown(text)

def to_json(data):
    """将Python对象转换为JSON字符串"""
    try:
        return json.dumps(data, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(data)

def simple_encrypt(text):
    """简单的字符串加密"""
    if not isinstance(text, str):
        return text
    # 注意：这只是示例，实际应用中应使用更安全的加密方法
    return hashlib.md5(text.encode()).hexdigest()[:16]

def url_encode(url):
    """简单的URL编码"""
    if not isinstance(url, str):
        return url
    import urllib.parse
    return urllib.parse.quote(url, safe=':/?&=')

# 自定义测试函数
def is_even(value):
    """检查数字是否为偶数"""
    try:
        return int(value) % 2 == 0
    except (ValueError, TypeError):
        return False

def is_prime(value):
    """检查数字是否为素数"""
    try:
        n = int(value)
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True
    except (ValueError, TypeError):
        return False

def contains(container, item):
    """检查容器是否包含指定项目"""
    if isinstance(container, (list, tuple, str, set)):
        return item in container
    elif isinstance(container, dict):
        return item in container.values()
    return False

def in_range(value, min_val, max_val):
    """检查值是否在指定范围内"""
    try:
        return min_val <= float(value) <= max_val
    except (ValueError, TypeError):
        return False

# 全局函数
def get_current_time(format_str='%Y-%m-%d %H:%M:%S'):
    """获取当前时间"""
    now = datetime.datetime.now()
    if format_str:
        return now.strftime(format_str)
    return now

def generate_random(min_val=0, max_val=100):
    """生成随机数"""
    return random.randint(min_val, max_val)

# 基础环境配置函数
def create_basic_environment():
    """创建基础Jinja2环境"""
    # 确定模板目录路径
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    
    # 创建基础环境
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    print("基础环境配置完成")
    return env

# 高级环境配置函数
def create_advanced_environment():
    """创建高级Jinja2环境"""
    # 确定模板目录路径
    template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    
    # 创建高级环境
    env = CustomJinja2Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,               # 移除块周围的空行
        lstrip_blocks=True,             # 移除块开头的空白
        newline_sequence='\n',          # 定义换行符序列
        extensions=[                    # 启用扩展
            'jinja2.ext.loopcontrols',  # 提供break和continue控制
            'jinja2.ext.do'             # 提供do语句支持
        ]
    )
    
    # 添加全局变量
    env.globals.update({
        'global_site_name': 'Jinja2学习平台',
        'current_year': datetime.datetime.now().year,
        'app_version': '1.0.0',
        'debug_mode': True,
        'server_info': 'Development Server'
    })
    
    print("高级环境配置完成")
    return env

# 缓存配置函数
def configure_cache(env, cache_type='memory', cache_size=50, cache_timeout=3600):
    """配置Jinja2模板缓存"""
    if cache_type == 'memory':
        # 使用内存缓存
        env.cache_size = cache_size
        print(f"已配置内存缓存，大小: {cache_size}")
    elif cache_type == 'filesystem':
        # 注意：Jinja2默认不支持文件系统缓存，需要扩展
        print("文件系统缓存需要额外扩展，此处仅作示例")
    else:
        # 禁用缓存
        env.cache = None
        print("缓存已禁用")
    
    return env

# 准备上下文数据函数
def prepare_context_data():
    """准备上下文数据"""
    context = {
        # 基本类型
        'name': '张三',
        'site_name': 'Python教程网站',
        'age': 28,
        'price': 99.99,
        'is_admin': True,
        
        # 复合类型
        'skills': ['Python', 'JavaScript', 'Java', 'C++', 'SQL'],
        'user_profile': {
            'username': 'zhangsan',
            'email': 'zhangsan@example.com',
            'level': 5,
            'join_date': '2023-01-15',
            'preferences': {
                'theme': 'dark',
                'notifications': True
            }
        },
        'current_time': datetime.datetime.now(),
        
        # 用于演示的数据
        'message': 'Hello, Jinja2模板引擎！',
        'discount': 0.2,
        'number1': 10,
        'number2': 15,
        'number3': 17,
        'variable1': [1, 2, 3],
        'variable2': {'key': 'value'},
        'variable3': '这是一个字符串',
        'unsafe_html': '<script>alert("XSS攻击")</script><p>这是一段HTML内容</p>',
        'markdown_content': '''# Markdown示例
## 二级标题

这是**粗体文本**和*斜体文本*。

- 列表项1
- 列表项2

[链接示例](https://www.example.com)'''
    }
    
    return context

# 渲染模板函数
def render_template(env, template_name, context):
    """渲染指定的模板"""
    try:
        # 获取模板
        template = env.get_template(template_name)
        
        # 渲染模板
        output = template.render(**context)
        
        # 保存渲染结果到文件
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, f"{template_name.replace('.html', '')}_output.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"模板渲染成功，输出文件: {output_file}")
        return output
    except Exception as e:
        print(f"模板渲染失败: {e}")
        return None

# 演示函数
def demo_basic_context():
    """演示基本上下文变量"""
    print("\n=== 演示基本上下文变量 ===")
    env = create_basic_environment()
    context = {
        'name': '李四',
        'age': 30,
        'languages': ['Python', 'JavaScript', 'Java']
    }
    
    # 渲染简单模板
    template = env.from_string('''
    <h1>基本上下文演示</h1>
    <p>姓名: {{ name }}</p>
    <p>年龄: {{ age }}</p>
    <p>编程语言:</p>
    <ul>
        {% for lang in languages %}
        <li>{{ lang }}</li>
        {% endfor %}
    </ul>
    ''')
    
    output = template.render(**context)
    print(output)


def demo_environment_config():
    """演示环境配置功能"""
    print("\n=== 演示环境配置功能 ===")
    
    # 创建高级环境
    env = create_advanced_environment()
    
    # 配置缓存
    env = configure_cache(env, cache_type='memory', cache_size=100)
    
    # 准备上下文数据
    context = prepare_context_data()
    
    # 渲染环境示例模板
    render_template(env, 'environment_example.html', context)


def demo_custom_extensions():
    """演示自定义扩展功能"""
    print("\n=== 演示自定义扩展功能 ===")
    
    # 创建高级环境
    env = create_advanced_environment()
    
    # 测试自定义过滤器
    template = env.from_string('''
    <p>原始字符串: {{ message }}</p>
    <p>大写: {{ message|uppercase }}</p>
    <p>反转: {{ message|reverse_string }}</p>
    <p>价格: {{ price|currency }}</p>
    <p>日期: {{ current_time|format_date('%Y-%m-%d') }}</p>
    ''')
    
    # 测试自定义测试
    template2 = env.from_string('''
    <p>{{ number1 }} 是偶数? {{ number1 is even }}</p>
    <p>{{ number3 }} 是素数? {{ number3 is prime }}</p>
    <p>技能包含Python? {{ skills is contains('Python') }}</p>
    ''')
    
    # 测试全局函数
    template3 = env.from_string('''
    <p>当前时间: {{ now() }}</p>
    <p>随机数: {{ random(1, 100) }}</p>
    <p>网站名称: {{ global_site_name }}</p>
    ''')
    
    # 准备上下文数据
    context = prepare_context_data()
    
    # 渲染并显示结果
    print("\n自定义过滤器测试:")
    print(template.render(**context))
    
    print("\n自定义测试测试:")
    print(template2.render(**context))
    
    print("\n全局函数测试:")
    print(template3.render(**context))


def demo_cache_strategies():
    """演示缓存策略"""
    print("\n=== 演示缓存策略 ===")
    
    # 测试启用缓存的性能
    env = create_advanced_environment()
    env = configure_cache(env, cache_type='memory')
    context = prepare_context_data()
    
    print("\n测试启用缓存的渲染时间:")
    import time
    start_time = time.time()
    for _ in range(5):
        render_template(env, 'environment_example.html', context)
    end_time = time.time()
    print(f"启用缓存渲染5次耗时: {end_time - start_time:.4f}秒")
    
    # 测试禁用缓存的性能
    env_no_cache = create_advanced_environment()
    env_no_cache = configure_cache(env_no_cache, cache_type='none')
    
    print("\n测试禁用缓存的渲染时间:")
    start_time = time.time()
    for _ in range(5):
        # 为了公平比较，使用相同的模板和上下文
        env_no_cache.get_template('environment_example.html').render(**context)
    end_time = time.time()
    print(f"禁用缓存渲染5次耗时: {end_time - start_time:.4f}秒")
    
    print("\n注意: 在实际应用中，缓存的效果会因模板复杂度和系统环境而有所不同")


def main():
    """主函数，运行所有演示"""
    print("Jinja2上下文和环境配置示例")
    print("=" * 50)
    
    # 运行各个演示
    demo_basic_context()
    demo_environment_config()
    demo_custom_extensions()
    demo_cache_strategies()
    
    print("\n" + "=" * 50)
    print("所有演示运行完成")

if __name__ == "__main__":
    main()