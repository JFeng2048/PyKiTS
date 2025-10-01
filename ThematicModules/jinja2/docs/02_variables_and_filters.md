# Jinja2变量和过滤器

## 变量
变量是Jinja2模板中用于存储和显示动态数据的元素。在Jinja2中，变量可以是各种Python数据类型，如字符串、数字、列表、字典、对象等。

### 变量的定义和使用
变量通常在渲染模板时通过上下文传递给模板。在模板中，使用双大括号`{{ 变量名 }}`来显示变量的值。

```html
<p>Hello, {{ name }}!</p>
<p>Your age is {{ age }}.</p>
```

### 变量的访问方式

#### 点表示法
对于字典和对象，可以使用点表示法访问其属性或值。

```html
<p>Username: {{ user.username }}</p>
<p>Email: {{ user.email }}</p>
```

#### 下标表示法
对于列表和字典，可以使用下标表示法访问其元素。

```html
<p>First item: {{ items[0] }}</p>
<p>User role: {{ user['role'] }}</p>
```

### 变量的作用域
在Jinja2中，变量有以下几种作用域：

1. **全局变量**：在整个模板中都可以访问的变量，通常通过上下文传递
2. **局部变量**：在特定代码块（如循环）中定义的变量
3. **块变量**：在模板继承中，通过`block`定义的变量

## 过滤器
过滤器是Jinja2中用于修改变量值的特殊函数。过滤器使用管道符号`|`连接在变量后面。

```html
<p>Hello, {{ name|upper }}!</p>
```

### 常用内置过滤器

#### 字符串过滤器

- **upper**：将字符串转换为大写
  ```html
  {{ 'hello'|upper }}  # 输出: HELLO
  ```

- **lower**：将字符串转换为小写
  ```html
  {{ 'HELLO'|lower }}  # 输出: hello
  ```

- **capitalize**：将字符串首字母大写
  ```html
  {{ 'hello world'|capitalize }}  # 输出: Hello world
  ```

- **title**：将字符串中每个单词的首字母大写
  ```html
  {{ 'hello world'|title }}  # 输出: Hello World
  ```

- **trim**：去除字符串首尾的空白字符
  ```html
  {{ '  hello  '|trim }}  # 输出: hello
  ```

- **length**：返回字符串的长度
  ```html
  {{ 'hello'|length }}  # 输出: 5
  ```

- **replace**：替换字符串中的子串
  ```html
  {{ 'hello world'|replace('world', 'Jinja2') }}  # 输出: hello Jinja2
  ```

- **default**：当变量未定义时，使用默认值
  ```html
  {{ undefined_var|default('默认值') }}  # 输出: 默认值
  ```

- **safe**：禁用自动转义，用于输出原始HTML
  ```html
  {{ html_content|safe }}  # 直接输出HTML内容
  ```

#### 数字过滤器

- **abs**：返回数字的绝对值
  ```html
  {{ -10|abs }}  # 输出: 10
  ```

- **round**：四舍五入到指定小数位数
  ```html
  {{ 3.14159|round(2) }}  # 输出: 3.14
  ```

- **int**：转换为整数
  ```html
  {{ '42'|int }}  # 输出: 42
  ```

- **float**：转换为浮点数
  ```html
  {{ '3.14'|float }}  # 输出: 3.14
  ```

#### 列表和字典过滤器

- **first**：返回列表的第一个元素
  ```html
  {{ [1, 2, 3]|first }}  # 输出: 1
  ```

- **last**：返回列表的最后一个元素
  ```html
  {{ [1, 2, 3]|last }}  # 输出: 3
  ```

- **length**：返回列表或字典的长度
  ```html
  {{ [1, 2, 3]|length }}  # 输出: 3
  {{ {'a': 1, 'b': 2}|length }}  # 输出: 2
  ```

- **sort**：对列表进行排序
  ```html
  {{ [3, 1, 2]|sort }}  # 输出: [1, 2, 3]
  ```

- **join**：将列表元素连接成字符串
  ```html
  {{ [1, 2, 3]|join(', ') }}  # 输出: 1, 2, 3
  ```

- **dictsort**：对字典按照键进行排序
  ```html
  {{ {'c': 3, 'a': 1, 'b': 2}|dictsort }}  # 输出: [('a', 1), ('b', 2), ('c', 3)]
  ```

#### 日期和时间过滤器

- **date**：格式化日期
  ```html
  {{ now|date('Y-m-d') }}  # 输出: 2023-10-01
  ```

- **time**：格式化时间
  ```html
  {{ now|time('H:i:s') }}  # 输出: 12:34:56
  ```

- **datetime**：格式化日期和时间
  ```html
  {{ now|datetime('Y-m-d H:i:s') }}  # 输出: 2023-10-01 12:34:56
  ```

### 过滤器的链式调用
多个过滤器可以链式调用，从左到右依次应用。

```html
{{ '  hello world  '|trim|title }}  # 输出: Hello World
```

### 自定义过滤器
在Jinja2中，还可以定义自己的过滤器。这将在[扩展开发](07_extensions.md)章节中详细介绍。

## 过滤器的参数
有些过滤器可以接受参数，参数使用括号传递。

```html
{{ 'hello'|replace('h', 'H', 1) }}  # 只替换第一个'h'，输出: Hello
{{ [1, 2, 3, 4, 5]|slice(2) }}  # 将列表分成每组2个元素
```

## 动手实践
请参考`examples/variables_demo.py`文件，运行示例代码，观察Jinja2变量和过滤器的使用方法。

## 练习
1. 创建一个包含多种数据类型的上下文
2. 在模板中使用不同的方式访问这些数据
3. 尝试使用各种过滤器修改变量的值
4. 练习过滤器的链式调用

## 下一步
完成本章节后，您可以继续学习[控制结构](03_control_structures.md)章节，了解Jinja2中的条件判断和循环等控制结构。