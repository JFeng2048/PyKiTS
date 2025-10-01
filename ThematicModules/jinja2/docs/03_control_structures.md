# Jinja2控制结构

控制结构是Jinja2模板中用于控制程序流程的元素，包括条件判断、循环等，可以根据不同的条件生成不同的输出内容。

## 条件语句
条件语句用于根据条件决定是否输出某些内容。Jinja2中的条件语句使用`{% if %}`、`{% elif %}`和`{% else %}`标签。

### 基本if语句
```html
{% if user.is_logged_in %}
  <p>Welcome back, {{ user.username }}!</p>
{% endif %}
```

### if-else语句
```html
{% if user.is_admin %}
  <p>You are an administrator.</p>
{% else %}
  <p>You are a regular user.</p>
{% endif %}
```

### if-elif-else语句
```html
{% if score >= 90 %}
  <p>优秀</p>
{% elif score >= 80 %}
  <p>良好</p>
{% elif score >= 60 %}
  <p>及格</p>
{% else %}
  <p>不及格</p>
{% endif %}
```

### 条件运算符
在条件语句中，可以使用以下运算符：

- **比较运算符**：`==`, `!=`, `<`, `>`, `<=`, `>=`
- **逻辑运算符**：`and`, `or`, `not`
- **成员运算符**：`in`, `not in`
- **测试运算符**：`is`, `is not`

```html
{% if user.age >= 18 and user.country == 'China' %}
  <p>You are eligible.</p>
{% endif %}

{% if 'admin' in user.roles %}
  <p>You have admin privileges.</p>
{% endif %}

{% if variable is defined %}
  <p>The variable exists.</p>
{% endif %}
```

## 循环语句
循环语句用于遍历集合（如列表、字典等）中的元素，并为每个元素生成输出内容。Jinja2中的循环语句使用`{% for %}`和`{% endfor %}`标签。

### 基本for循环
```html
<ul>
{% for item in items %}
  <li>{{ item }}</li>
{% endfor %}
</ul>
```

### 遍历字典
```html
<ul>
{% for key, value in user.items() %}
  <li>{{ key }}: {{ value }}</li>
{% endfor %}
</ul>
```

### 循环索引
在循环中，可以使用`loop`变量获取循环的相关信息，如索引、长度等。

```html
<ul>
{% for item in items %}
  <li>{{ loop.index }}. {{ item }}</li>  {# loop.index从1开始 #}
{% endfor %}
</ul>
```

### loop变量的常用属性

- `loop.index`：当前循环的索引（从1开始）
- `loop.index0`：当前循环的索引（从0开始）
- `loop.revindex`：当前循环的反向索引（从长度开始，到1结束）
- `loop.revindex0`：当前循环的反向索引（从长度-1开始，到0结束）
- `loop.first`：如果是第一次循环，返回True
- `loop.last`：如果是最后一次循环，返回True
- `loop.length`：循环对象的长度

```html
<ul>
{% for item in items %}
  <li>
    {{ loop.index }}/{{ loop.length }}: {{ item }}
    {% if loop.first %} (First item){% endif %}
    {% if loop.last %} (Last item){% endif %}
  </li>
{% endfor %}
</ul>
```

### 循环控制

#### else子句
当循环的对象为空时，执行else子句中的内容。

```html
<ul>
{% for item in items %}
  <li>{{ item }}</li>
{% else %}
  <li>No items found.</li>
{% endfor %}
</ul>
```

#### break和continue
在较新版本的Jinja2中，支持`break`和`continue`语句来控制循环流程。

```html
<ul>
{% for item in items %}
  {% if item == 'stop' %}
    {% break %}
  {% endif %}
  {% if item == 'skip' %}
    {% continue %}
  {% endif %}
  <li>{{ item }}</li>
{% endfor %}
</ul>
```

### 嵌套循环
循环可以嵌套使用。

```html
<table>
{% for row in table_data %}
  <tr>
  {% for cell in row %}
    <td>{{ cell }}</td>
  {% endfor %}
  </tr>
{% endfor %}
</table>
```

## 循环和条件结合使用
循环和条件语句可以结合使用，实现更复杂的逻辑。

```html
<ul>
{% for user in users %}
  {% if user.is_active %}
    <li>{{ user.username }} (Active)</li>
  {% else %}
    <li>{{ user.username }} (Inactive)</li>
  {% endif %}
{% endfor %}
</ul>
```

## 宏中的控制结构
控制结构也可以在宏中使用，使宏更加灵活。

```html
{% macro render_list(items, show_index=false) %}
  <ul>
  {% for item in items %}
    <li>
      {% if show_index %}{{ loop.index }}. {% endif %}
      {{ item }}
    </li>
  {% endfor %}
  </ul>
{% endmacro %}
```

## 动手实践
请参考`examples/control_structures.py`文件，运行示例代码，观察Jinja2控制结构的使用方法。

## 练习
1. 创建一个包含条件语句的模板，根据用户角色显示不同内容
2. 创建一个循环模板，显示用户列表
3. 结合循环和条件，只显示满足特定条件的项目
4. 使用loop变量显示循环信息

## 下一步
完成本章节后，您可以继续学习[模板继承](04_template_inheritance.md)章节，了解Jinja2中的模板继承和布局复用功能。