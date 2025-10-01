# Jinja2 练习项目

本目录包含了一系列Jinja2模板引擎的练习项目，旨在帮助你巩固和实践Jinja2的各种功能和技巧。

## 练习结构

每个练习通常包含以下部分：

1. **练习文件** (`*_exercise.py`) - 包含练习任务和需要你完成的代码
2. **模板文件** (`templates/*.html`) - 与练习相关的模板文件
3. **解决方案** (`solutions/*_exercise_solution.py`) - 练习的参考解决方案

## 现有练习

### 1. 基础语法练习 (basic_exercise.py)
- 熟悉Jinja2的基本语法
- 学习如何创建环境、加载模板、准备上下文数据
- 练习变量输出、表达式和基本过滤器的使用

### 2. 控制结构练习 (control_structures_exercise.py)
- 掌握条件语句 (if-elif-else)
- 学习循环控制 (for循环、循环变量)
- 练习嵌套循环和复杂条件判断
- 了解break和continue的使用

### 3. 模板继承练习 (template_inheritance_exercise.py)
- 理解模板继承的概念
- 学习如何创建和使用基础模板
- 掌握块(block)的定义和覆盖
- 练习使用super()函数

## 如何使用这些练习

1. 首先确保你已经安装了Jinja2：
   ```
   pip install -r ../requirements.txt
   ```

2. 选择一个练习文件，例如 `basic_exercise.py`，打开并阅读其中的任务说明

3. 根据任务要求，完成代码中的TODO部分

4. 运行练习脚本：
   ```
   python basic_exercise.py
   ```

5. 检查输出结果，验证是否符合预期

6. 如果你遇到困难，可以参考`solutions`目录下的解决方案

## 练习建议

- 先从基础练习开始，逐步深入到更复杂的功能
- 尝试修改和扩展练习内容，加深理解
- 将学到的技能应用到实际项目中
- 定期回顾和复习，巩固知识点

## 资源链接

- [Jinja2官方文档](https://jinja.palletsprojects.com/)
- [Jinja2中文文档](https://docs.jinkan.org/docs/jinja2/)
- 教程文件位于`../docs`目录
- 示例代码位于`../examples`目录

祝你学习愉快！

© 2025 Jinja2学习中心