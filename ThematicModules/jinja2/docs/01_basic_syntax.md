# Jinja2基础语法

## 什么是Jinja2？
Jinja2是一个现代的、设计良好的Python模板引擎，它提供了灵活的模板语法和强大的功能，被广泛应用于Web开发、代码生成等场景。

## 基本概念

### 模板
模板是包含变量和控制结构的文本文件，用于生成最终的输出内容。Jinja2模板可以是HTML、XML、JSON、纯文本等任何格式。

### 渲染
渲染是将模板中的变量替换为实际值，并执行控制结构的过程，最终生成最终的输出内容。

## 基础语法

### 1. 变量
变量是模板中最基本的元素，用于显示动态内容。在Jinja2中，变量使用双大括号`{{ }}`包围。

```html
<p>Hello, {{ name }}!</p>
```

当渲染模板时，`{{ name }}`会被替换为实际的name值。

### 2. 表达式
Jinja2支持在模板中使用表达式，可以是变量、算术运算、比较运算、逻辑运算等。

```html
<p>2 + 3 = {{ 2 + 3 }}</p>
<p>Is 5 greater than 3? {{ 5 > 3 }}</p>
<p>Your age next year: {{ age + 1 }}</p>
```

### 3. 注释
Jinja2中的注释使用`{# #}`包围，注释内容不会在渲染后的输出中显示。

```html
<p>Visible content</p>
{# This is a comment and won't be visible #}
```

### 4. 转义与安全
默认情况下，Jinja2会自动转义变量内容，以防止XSS攻击。如果需要输出原始HTML内容，可以使用`safe`过滤器。

```html
<p>转义后: {{ user_input }}</p>
<p>原始输出: {{ user_input|safe }}</p>
```

### 5. 行语句
Jinja2支持使用行语句，以`{% %}`开头并以`%}`结尾的代码行。

```html
{% if user.logged_in %}
  Welcome back, {{ user.name }}!
{% endif %}
```

## 基本数据类型

### 字符串
字符串可以使用单引号或双引号包围。

```html
<p>Name: {{ "John Doe" }}</p>
<p>Greeting: {{ 'Hello, world!' }}</p>
```

### 数字
支持整数和浮点数。

```html
<p>Count: {{ 42 }}</p>
<p>Price: {{ 9.99 }}</p>
```

### 列表
可以通过索引访问列表元素。

```html
<p>First item: {{ items[0] }}</p>
<p>Second item: {{ items[1] }}</p>
```

### 字典
可以通过键访问字典值。

```html
<p>Username: {{ user['username'] }}</p>
<p>Email: {{ user.email }}</p>  {# 点表示法也可以 #}
```

### 布尔值
可以用于条件判断。

```html
{% if is_admin %}
  <p>You are an admin.</p>
{% endif %}
```

## Jinja2的基本使用流程

1. 创建Jinja2环境
2. 加载模板
3. 准备上下文数据
4. 渲染模板
5. 获取渲染结果

## 动手实践
请参考`examples/basic_usage.py`文件，运行示例代码，观察Jinja2的基本用法。

## 练习
1. 创建一个简单的模板，显示用户信息（姓名、年龄、邮箱）
2. 在模板中使用算术表达式和比较表达式
3. 尝试使用注释和行语句

## 下一步
完成本章节后，您可以继续学习[变量和过滤器](02_variables_and_filters.md)章节，了解更多关于Jinja2变量操作和过滤器的知识。