# Jinja2模板继承教程

## 1. 模板继承概述

模板继承是Jinja2中最强大的特性之一，它允许你创建一个基础"骨架"模板，定义网站的通用结构和元素，然后在子模板中扩展和重写这些结构。这有助于保持代码的DRY（Don't Repeat Yourself）原则，使模板管理更加高效和可维护。

### 核心概念

- **基础模板**：定义页面的基本结构，包含通用部分和可被覆盖的"块"。
- **子模板**：继承自基础模板，填充或重写基础模板中定义的块。
- **块**：基础模板中定义的可被覆盖的区域。

## 2. 基础模板设计

基础模板通常包含网站的通用元素，如HTML结构、CSS样式、JavaScript脚本、导航栏、页脚等。在这些模板中，你可以定义可被后续子模板覆盖的"块"。

### 基本语法

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
    {% block css %}
    <!-- 这里是默认CSS -->
    <link rel="stylesheet" href="/static/style.css">
    {% endblock %}
</head>
<body>
    <header>
        <nav>导航栏内容</nav>
    </header>
    
    <main>
        {% block content %}
        <!-- 子模板将填充这里的内容 -->
        {% endblock %}
    </main>
    
    <footer>
        页脚内容
    </footer>
    
    {% block js %}
    <!-- 这里是默认JavaScript -->
    <script src="/static/main.js"></script>
    {% endblock %}
</body>
</html>
```

### 关键特性

- 使用`{% block 名称 %}...{% endblock %}`定义可被覆盖的块。
- 每个块都有一个默认内容，当子模板未覆盖该块时显示。
- 块可以嵌套，但建议保持简洁以提高可维护性。

## 3. 子模板实现

子模板通过`{% extends "基础模板路径" %}`指令来继承基础模板，然后通过重新定义块来填充或覆盖基础模板的内容。

### 基本语法

```html
{% extends "base.html" %}

{% block title %}首页 - 我的网站{% endblock %}

{% block css %}
    {{ super() }}  <!-- 继承基础模板中的CSS -->
    <link rel="stylesheet" href="/static/index.css">  <!-- 添加额外的CSS -->
{% endblock %}

{% block content %}
    <h1>欢迎来到我的网站</h1>
    <p>这是首页内容。</p>
{% endblock %}

{% block js %}
    {{ super() }}  <!-- 继承基础模板中的JavaScript -->
    <script src="/static/index.js"></script>  <!-- 添加额外的JavaScript -->
{% endblock %}
```

### 重要指令

- **extends**：指定要继承的基础模板路径。
- **super()**：在子模板中调用父模板中相同块的内容。
- **block**：在子模板中重定义父模板中的块。

## 4. 嵌套块与包含

模板继承支持块的嵌套和包含，可以创建复杂的模板结构。

### 嵌套块

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    {% block head %}
        <title>{% block title %}默认标题{% endblock %}</title>
        {% block meta %}
            <meta charset="UTF-8">
        {% endblock %}
    {% endblock %}
</head>
<body>
    {% block content %}
        <div class="container">
            {% block main %}
            <!-- 主要内容 -->
            {% endblock %}
        </div>
    {% endblock %}
</body>
</html>
```

子模板可以选择性地覆盖任意层级的块，而不必覆盖所有块：

```html
{% extends "base.html" %}

{% block title %}特定页面标题{% endblock %}

{% block main %}
    <h1>特定页面的主要内容</h1>
{% endblock %}
```

### 包含（Include）指令

除了继承外，Jinja2还提供了`{% include %}`指令，用于在模板中包含其他模板片段：

```html
<!-- 基础模板中的导航栏 -->
<header>
    {% include "includes/navbar.html" %}
</header>

<!-- 基础模板中的页脚 -->
<footer>
    {% include "includes/footer.html" %}
</footer>
```

## 5. 模板继承最佳实践

### 5.1 合理规划基础模板结构

- 创建一个清晰的基础模板层次结构
- 定义合理的块结构，避免过多过细的块
- 将通用逻辑放在基础模板中

### 5.2 子模板的最佳实践

- 只覆盖必要的块
- 合理使用`super()`来重用父模板内容
- 保持子模板的简洁性

### 5.3 性能考量

- 避免过深的继承层次
- 避免在块中使用复杂的逻辑
- 合理使用缓存机制

## 6. 高级模板继承技巧

### 6.1 宏与继承结合

可以在基础模板中定义宏，然后在子模板中使用：

```html
<!-- base.html -->
{% macro render_flash_messages() %}
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
{% endmacro %}

<!-- 在子模板中使用 -->
{% extends "base.html" %}

{% block content %}
    {{ render_flash_messages() }}
    <!-- 其他内容 -->
{% endblock %}
```

### 6.2 条件继承

可以根据条件动态选择要继承的模板：

```html
{% if condition %}
    {% extends "base1.html" %}
{% else %}
    {% extends "base2.html" %}
{% endif %}
```

### 6.3 多继承模式

虽然Jinja2本身不支持多继承，但可以通过组合使用`include`和`extends`来实现类似效果：

```html
{% extends "base.html" %}

{% block sidebar %}
    {% include "sidebar.html" %}
{% endblock %}
```

## 7. 模板继承实践指导

### 7.1 项目结构建议

- 创建专门的`layouts`目录存放基础模板
- 创建`includes`目录存放可重用的模板片段
- 按照功能模块组织子模板

### 7.2 常见用例

- 创建网站通用布局
- 构建具有一致外观的管理后台
- 开发多语言支持的模板系统

## 8. 练习

### 基础练习

1. 创建一个基础模板`base.html`，包含标题、导航栏、内容区和页脚。
2. 创建两个子模板，`home.html`和`about.html`，分别继承自`base.html`并填充各自的内容。
3. 在子模板中覆盖标题和内容块，并尝试使用`super()`函数。

### 进阶练习

1. 创建一个三层模板继承结构：基础模板 → 特定类型页面模板 → 具体页面模板。
2. 在基础模板中定义可重用的宏，并在子模板中使用。
3. 使用`include`指令将通用组件（如侧边栏、导航栏）引入到基础模板中。

## 9. 总结

模板继承是Jinja2中强大且灵活的特性，通过创建可重用的基础模板和可扩展的子模板，可以显著提高模板代码的复用性和可维护性。合理规划模板结构、遵循最佳实践，可以使你的模板系统更加高效和健壮。