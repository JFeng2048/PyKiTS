# Jinja2宏和包含教程

## 1. 宏概述

宏是Jinja2中的一个强大功能，它允许你定义可重用的模板片段，类似于编程语言中的函数。宏可以接受参数，处理逻辑，并生成输出内容。通过使用宏，你可以将重复使用的代码片段封装起来，提高模板的可维护性和复用性。

### 宏的基本概念

- **宏定义**：使用`{% macro 名称(参数1, 参数2, ...) %}...{% endmacro %}`定义一个宏
- **宏调用**：使用`{{ 宏名称(参数1, 参数2, ...) }}`调用一个宏
- **参数传递**：可以向宏传递位置参数和关键字参数
- **默认参数**：可以为宏参数设置默认值

## 2. 宏的定义与使用

### 基本语法

```html
{# 定义一个简单的宏 #}
{% macro render_button(text, url, class='btn') %}
<a href="{{ url }}" class="{{ class }}">
    {{ text }}
</a>
{% endmacro %}

{# 调用宏 #}
{{ render_button('点击这里', '/home', 'btn btn-primary') }}
```

### 带参数的宏

宏可以接受任意数量的参数，包括位置参数和关键字参数：

```html
{% macro input_field(name, type='text', label='', value='', placeholder='') %}
<div class="form-group">
    {% if label %}
        <label for="{{ name }}">{{ label }}</label>
    {% endif %}
    <input type="{{ type }}" 
           id="{{ name }}" 
           name="{{ name }}" 
           value="{{ value }}" 
           placeholder="{{ placeholder }}">
</div>
{% endmacro %}

{# 使用这个宏创建表单字段 #}
{{ input_field('username', label='用户名', placeholder='请输入用户名') }}
{{ input_field('password', type='password', label='密码', placeholder='请输入密码') }}
```

### 宏的高级用法

#### 默认参数

你可以为宏参数设置默认值，这样在调用宏时如果不提供该参数，就会使用默认值：

```html
{% macro alert(message, type='info') %}
<div class="alert alert-{{ type }}">
    {{ message }}
</div>
{% endmacro %}

{# 使用默认参数 #}
{{ alert('这是一条提示信息') }}

{# 覆盖默认参数 #}
{{ alert('这是一条错误信息', 'danger') }}
```

#### 变长参数

使用`**kwargs`可以接收任意数量的额外关键字参数：

```html
{% macro div_with_classes(content, **classes) %}
<div class="{{ classes|join(' ') }}">
    {{ content }}
</div>
{% endmacro %}

{# 使用变长参数 #}
{{ div_with_classes('这是一个带有多个类的div', 'container', 'mt-4', 'p-2') }}
```

#### 宏中的逻辑

宏内部可以包含控制结构和其他Jinja2语法：

```html
{% macro render_list(items, ordered=false) %}
{% if ordered %}
    <ol>
{% else %}
    <ul>
{% endif %}
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
{% if ordered %}
    </ol>
{% else %}
    </ul>
{% endif %}
{% endmacro %}

{# 使用带逻辑的宏 #}
{{ render_list(['苹果', '香蕉', '橙子']) }}
{{ render_list(['第一步', '第二步', '第三步'], ordered=true) }}
```

## 3. 宏的组织与导入

对于较大的项目，将宏组织在单独的文件中是一种良好的实践。你可以在专门的宏文件中定义所有需要的宏，然后在其他模板中导入和使用它们。

### 创建宏文件

通常将宏文件放在`templates/macros/`目录下：

**templates/macros/forms.html:**
```html
{% macro input(name, type='text', value='', placeholder='', required=false) %}
<input type="{{ type }}" 
       name="{{ name }}" 
       value="{{ value }}" 
       placeholder="{{ placeholder }}" 
       {% if required %}required{% endif %}>
{% endmacro %}

{% macro textarea(name, value='', rows=4, cols=50) %}
<textarea name="{{ name }}" rows="{{ rows }}" cols="{{ cols }}">
    {{ value }}
</textarea>
{% endmacro %}

{% macro select(name, options, selected='') %}
<select name="{{ name }}">
    {% for value, label in options.items() %}
        <option value="{{ value }}" {% if value == selected %}selected{% endif %}>
            {{ label }}
        </option>
    {% endfor %}
</select>
{% endmacro %}
```

### 导入宏

在其他模板中，你可以使用`{% import %}`指令来导入宏：

```html
{# 导入特定宏文件中的所有宏 #}
{% import "macros/forms.html" as forms %}

{# 使用导入的宏 #}
<form>
    {{ forms.input('username', placeholder='用户名') }}
    {{ forms.input('password', type='password', placeholder='密码') }}
    {{ forms.textarea('description', rows=5) }}
    
    {% set options = {'male': '男', 'female': '女', 'other': '其他'} %}
    {{ forms.select('gender', options, 'male') }}
</form>
```

### 从宏文件中导入特定宏

你也可以只导入宏文件中的特定宏：

```html
{# 只导入特定的宏 #}
{% from "macros/forms.html" import input, submit %}

{# 直接使用导入的宏，不需要前缀 #}
<input type="email" name="email" placeholder="邮箱">
{{ submit('提交') }}
```

### 全局宏

如果你希望在所有模板中都能使用某些宏，可以在Jinja2环境中注册它们：

```python
from jinja2 import Environment, FileSystemLoader

# 创建环境
env = Environment(loader=FileSystemLoader('templates'))

# 定义全局宏
def format_currency(value):
    return f"¥{value:,.2f}"

# 注册全局宏
env.globals['format_currency'] = format_currency
```

## 4. 包含指令

`{% include %}`指令允许你在一个模板中包含另一个模板的内容。这是一种简单的代码复用机制，适用于不需要参数的固定内容块。

### 基本用法

```html
{# 包含导航栏模板 #}
<header>
    {% include "includes/navbar.html" %}
</header>

{# 包含页脚模板 #}
<footer>
    {% include "includes/footer.html" %}
</footer>
```

### 条件包含

你可以使用条件语句来决定是否包含某个模板：

```html
{% if user.is_authenticated %}
    {% include "includes/user_menu.html" %}
{% else %}
    {% include "includes/login_prompt.html" %}
{% endif %}
```

### 包含变量名的模板

你也可以使用变量来指定要包含的模板名称：

```html
{% set sidebar_template = user.is_admin ? 'admin_sidebar.html' : 'user_sidebar.html' %}
{% include sidebar_template %}
```

### 忽略缺失的模板

如果包含的模板可能不存在，你可以使用`ignore missing`选项来避免错误：

```html
{% include "includes/custom_sidebar.html" ignore missing %}
```

## 5. 宏与包含的对比

宏和包含都是Jinja2中代码复用的机制，但它们有不同的使用场景和特点：

| 特性 | 宏 | 包含 |
|------|------|------|
| 参数支持 | 支持 | 不直接支持，需要在上下文中传递变量 |
| 返回值 | 返回渲染后的内容 | 直接插入模板内容 |
| 复杂度 | 可以包含复杂逻辑 | 通常用于静态内容 |
| 组织方式 | 通常放在专门的宏文件中 | 可以放在任何位置 |
| 导入方式 | 使用`import`或`from...import` | 使用`include` |

### 适用场景

- **宏**：适用于需要参数化、有逻辑处理的可重用组件，如表单字段、按钮、卡片等。
- **包含**：适用于固定的、不需要参数的内容块，如导航栏、页脚、侧边栏等。

## 6. 最佳实践

### 宏的最佳实践

1. **命名规范**：为宏使用清晰、描述性的名称，如`render_button`、`input_field`等。
2. **参数设计**：为常用参数提供默认值，使宏更灵活。
3. **宏文件组织**：将相关的宏组织在同一个文件中，如`forms.html`、`components.html`等。
4. **宏的粒度**：保持宏的简洁和专注，每个宏只负责一个功能。
5. **文档注释**：为复杂的宏添加注释，说明其用途和参数。

### 包含的最佳实践

1. **模板结构**：将可重用的模板片段放在`includes`目录下。
2. **内容独立性**：确保包含的模板可以独立工作，不依赖于特定的上下文。
3. **避免过度包含**：过多的包含会增加模板的复杂性，影响性能。
4. **条件包含**：合理使用条件包含来根据不同情况显示不同内容。

## 7. 高级技巧

### 宏中的宏

你可以在一个宏中调用另一个宏，这对于构建复杂组件非常有用：

```html
{% macro form_field(label, field) %}
<div class="form-group">
    <label>{{ label }}</label>
    {{ field }}
</div>
{% endmacro %}

{% macro input_field(name, type='text', value='') %}
<input type="{{ type }}" name="{{ name }}" value="{{ value }}">
{% endmacro %}

{# 在宏中调用另一个宏 #}
{{ form_field('用户名', input_field('username')) }}
{{ form_field('密码', input_field('password', type='password')) }}
```

### 包含与继承结合

你可以将包含指令与模板继承结合使用，创建更加灵活和可维护的模板系统：

```html
{# base.html #}
<!DOCTYPE html>
<html>
<head>{% block head %}{% endblock %}</head>
<body>
    {% include "includes/header.html" %}
    
    <main>{% block content %}{% endblock %}</main>
    
    {% include "includes/footer.html" %}
</body>
</html>
```

### 动态包含路径

你可以使用变量来动态构建包含路径：

```html
{% set section = 'blog' %}
{% set template_path = 'includes/' ~ section ~ '_sidebar.html' %}
{% include template_path %}
```

## 8. 练习

### 基础练习

1. 创建一个宏文件`templates/macros/components.html`，定义几个常用的UI组件宏，如按钮、卡片、警告框等。
2. 在另一个模板中导入并使用这些宏。
3. 创建几个简单的包含文件，如导航栏、页脚，并在主模板中包含它们。

### 进阶练习

1. 创建一个复杂的表单宏，包含多种输入类型和验证逻辑。
2. 创建一个分页宏，可以处理不同的分页参数和样式。
3. 结合宏和包含，创建一个具有一致风格的完整页面模板。

## 9. 总结

宏和包含是Jinja2中实现代码复用的两种重要机制。宏提供了参数化和逻辑处理能力，适用于构建可配置的组件；包含则提供了简单直接的内容插入方式，适用于复用固定内容块。通过合理使用这两种机制，你可以创建更加模块化、可维护和可扩展的模板系统。