# Jinja2上下文和环境配置

Jinja2的上下文和环境配置是控制模板渲染过程和行为的关键部分。本章将详细介绍如何管理模板上下文数据、配置Jinja2环境以及如何扩展和定制Jinja2的功能。

## 1. 模板上下文

模板上下文是模板渲染过程中可以访问的变量和对象的集合。它为模板提供了动态数据。

### 1.1 基本上下文数据

上下文数据可以是基本数据类型、复杂数据结构或自定义对象：

```python
# 基本上下文数据示例
context = {
    'name': '张三',
    'age': 30,
    'is_admin': True,
    'tags': ['python', 'jinja2', 'web'],
    'profile': {
        'bio': 'Python开发者',
        'website': 'https://example.com'
    },
    'registration_date': datetime.now()
}

# 使用上下文渲染模板
template.render(**context)
```

### 1.2 上下文变量的作用域

- **全局上下文**：在整个渲染过程中可访问的数据
- **局部上下文**：在特定模板块或宏中可访问的数据
- **运行时上下文**：在渲染过程中动态生成的数据

```python
# 添加全局上下文变量
env.globals['current_year'] = datetime.now().year
env.globals['site_name'] = '我的网站'

# 添加测试函数
def is_even(n):
    return n % 2 == 0

env.tests['even'] = is_even
```

### 1.3 上下文处理器

上下文处理器是一种可以在每次渲染模板时自动注入上下文数据的机制：

```python
# 定义上下文处理器
def inject_user():
    # 这里可以是从数据库或会话中获取用户信息的逻辑
    user = {
        'name': '访客',
        'authenticated': False
    }
    return {'user': user}

# 创建一个带有上下文处理器的环境
class CustomEnvironment(Environment):
    def render_template(self, template_name, **context):
        # 添加上下文处理器的数据
        context.update(inject_user())
        template = self.get_template(template_name)
        return template.render(**context)
```

## 2. 环境配置

Jinja2环境对象(`Environment`)是模板渲染的核心，它包含了模板加载器、过滤器、测试、全局变量等配置。

### 2.1 基本环境配置

创建和配置Jinja2环境的基本方法：

```python
from jinja2 import Environment, FileSystemLoader, select_autoescape

# 创建基本环境
env = Environment(
    loader=FileSystemLoader('templates'),  # 设置模板加载器
    autoescape=select_autoescape(['html', 'xml']),  # 设置自动转义
    trim_blocks=True,  # 自动删除块末尾的换行符
    lstrip_blocks=True,  # 自动删除块起始的空白字符
    undefined=StrictUndefined,  # 使用严格未定义，访问不存在的变量会抛出异常
    extensions=['jinja2.ext.loopcontrols', 'jinja2.ext.do']  # 启用扩展
)
```

### 2.2 模板加载器

Jinja2支持多种模板加载方式，适应不同的应用场景：

#### 2.2.1 FileSystemLoader

从文件系统加载模板：

```python
from jinja2 import FileSystemLoader

# 从单个目录加载模板
loader = FileSystemLoader('templates')

# 从多个目录加载模板，按顺序查找
loader = FileSystemLoader(['templates', 'shared_templates'])

env = Environment(loader=loader)
```

#### 2.2.2 PackageLoader

从Python包中加载模板：

```python
from jinja2 import PackageLoader

# 从指定包的templates目录加载模板
loader = PackageLoader('my_package', 'templates')

env = Environment(loader=loader)
```

#### 2.2.3 DictLoader

从Python字典中加载模板字符串：

```python
from jinja2 import DictLoader

# 模板字典
template_dict = {
    'index.html': '<h1>{{ title }}</h1>',
    'about.html': '<h1>关于我们</h1><p>{{ content }}</p>'
}

loader = DictLoader(template_dict)

env = Environment(loader=loader)
```

#### 2.2.4 ChoiceLoader

尝试从多个加载器中加载模板：

```python
from jinja2 import ChoiceLoader, FileSystemLoader, PackageLoader

# 创建选择加载器
loader = ChoiceLoader([
    FileSystemLoader('custom_templates'),
    PackageLoader('my_package', 'templates')
])

env = Environment(loader=loader)
```

### 2.3 自动转义配置

自动转义是防止XSS攻击的重要机制：

```python
from jinja2 import select_autoescape

# 自动转义HTML和XML文件
env = Environment(
    autoescape=select_autoescape(['html', 'xml'])
)

# 完全启用自动转义
env = Environment(
    autoescape=True
)

# 完全禁用自动转义（不推荐，除非你知道风险）
env = Environment(
    autoescape=False
)
```

### 2.4 空白控制

控制模板中空白字符的处理方式：

```python
# 配置空白控制
env = Environment(
    trim_blocks=True,  # 删除块末尾的换行符
    lstrip_blocks=True,  # 删除块起始的空白字符
    keep_trailing_newline=True  # 保留模板末尾的换行符
)
```

## 3. 扩展环境功能

Jinja2允许通过添加自定义过滤器、测试、全局函数等来扩展环境功能。

### 3.1 添加自定义过滤器

过滤器用于在模板中转换数据：

```python
# 定义自定义过滤器
def to_uppercase(value):
    return value.upper()

def format_currency(value, currency='¥'):
    return f"{currency}{value:.2f}"

# 添加到环境
env.filters['uppercase'] = to_uppercase
env.filters['currency'] = format_currency

# 在模板中使用
# {{ name|uppercase }}
# {{ price|currency }}
# {{ price|currency('$') }}
```

### 3.2 添加自定义测试

测试用于在条件语句中评估表达式：

```python
# 定义自定义测试
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_list(value):
    return isinstance(value, list)

# 添加到环境
env.tests['prime'] = is_prime
env.tests['list'] = is_list

# 在模板中使用
# {% if number is prime %}
# {% if items is list %}
```

### 3.3 添加全局变量和函数

全局变量和函数在所有模板中都可访问：

```python
# 添加全局变量
env.globals['site_name'] = '我的Jinja2网站'
env.globals['current_year'] = datetime.now().year

# 添加全局函数
def now(format='%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(format)

def markdown(text):
    # 假设使用markdown库将Markdown转换为HTML
    import markdown as md
    return md.markdown(text)

env.globals['now'] = now
env.globals['markdown'] = markdown

# 在模板中使用
# {{ site_name }}
# {{ now() }}
# {{ now('%Y-%m-%d') }}
# {{ content|markdown }}
```

## 4. 环境缓存配置

Jinja2会缓存已编译的模板以提高性能，你可以根据需要配置缓存行为：

```python
# 配置模板缓存
env = Environment(
    loader=FileSystemLoader('templates'),
    auto_reload=True,  # 开发模式下自动重新加载模板
    cache_size=50,  # 缓存的模板数量
)

# 禁用缓存（开发模式使用）
env.cache = None

# 使用自定义缓存
env.cache = {}  # 简单的内存缓存
```

## 5. 自定义环境类

对于复杂的应用场景，你可以继承`Environment`类来自定义行为：

```python
from jinja2 import Environment, FileSystemLoader

class CustomEnvironment(Environment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 添加默认配置
        self.loader = FileSystemLoader('templates')
        self.trim_blocks = True
        self.lstrip_blocks = True
        
        # 添加自定义功能
        self._setup_custom_features()
        
    def _setup_custom_features(self):
        # 添加自定义过滤器
        self.filters['custom_filter'] = lambda x: f"自定义处理: {x}"
        
        # 添加全局变量
        self.globals['app_version'] = '1.0.0'
        
    def render_with_defaults(self, template_name, **context):
        # 添加默认上下文数据
        default_context = {
            'render_time': datetime.now(),
            'debug_mode': False
        }
        default_context.update(context)
        
        template = self.get_template(template_name)
        return template.render(**default_context)

# 使用自定义环境
custom_env = CustomEnvironment()
result = custom_env.render_with_defaults('index.html', title='首页')
```

## 6. 上下文和环境的最佳实践

### 6.1 组织上下文数据

- 将相关的数据组织成逻辑组（如使用字典）
- 使用一致的命名约定
- 限制全局上下文的大小，只包含真正全局的数据
- 对敏感数据进行适当的处理或屏蔽

### 6.2 环境配置建议

- 在开发环境中启用`auto_reload`和禁用缓存
- 在生产环境中优化缓存配置
- 为不同类型的模板创建专用的环境
- 使用`StrictUndefined`来捕获未定义的变量

### 6.3 性能优化

- 预编译常用模板
- 合理设置缓存大小
- 使用适当的加载器（如生产环境使用`FileSystemLoader`）
- 避免在模板中执行复杂的计算，将计算逻辑移到上下文准备阶段

## 7. 高级环境配置示例

### 7.1 多环境配置

为不同环境（开发、测试、生产）创建不同的配置：

```python
def create_environment(env_type='development'):
    """根据环境类型创建适当的Jinja2环境"""
    if env_type == 'development':
        return Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
            auto_reload=True,
            cache_size=0  # 禁用缓存
        )
    elif env_type == 'testing':
        return Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
            auto_reload=False,
            cache_size=20
        )
    else:  # production
        return Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
            auto_reload=False,
            cache_size=100
        )

# 使用
prod_env = create_environment('production')
dev_env = create_environment('development')
```

### 7.2 集成到Web框架

将Jinja2集成到Web框架（如Flask）中：

```python
from flask import Flask

app = Flask(__name__)

# 配置Flask使用的Jinja2环境
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.auto_reload = app.debug  # 开发模式下自动重载

# 添加自定义过滤器
@app.template_filter('currency')
def currency_filter(value):
    return f"¥{value:.2f}"

# 添加全局函数
@app.context_processor
def inject_global_vars():
    return {
        'site_name': app.config.get('SITE_NAME', '我的网站'),
        'current_time': datetime.now()
    }

# 使用Jinja2渲染模板
@app.route('/')
def index():
    return render_template('index.html', title='首页')
```

## 8. 练习

### 8.1 基础练习

1. 创建一个Jinja2环境，配置文件系统加载器和自动转义
2. 向环境中添加2个自定义过滤器和2个自定义测试
3. 创建一个包含全局变量的上下文，并渲染一个使用这些变量的模板

### 8.2 进阶练习

1. 创建一个自定义环境类，继承自`Environment`
2. 在自定义类中实现自动注入常用上下文数据的功能
3. 添加一个方法来预编译和缓存常用模板
4. 实现根据环境类型（开发/生产）自动切换配置的功能

### 8.3 挑战练习

1. 创建一个模板加载器，从远程服务器加载模板
2. 实现一个模板缓存系统，可以将编译后的模板保存到磁盘
3. 开发一个完整的上下文处理器系统，支持多个处理器和优先级
4. 实现一个可以在运行时动态添加和删除过滤器、测试和全局函数的机制