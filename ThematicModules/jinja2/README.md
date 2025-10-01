# Jinja2学习资源

## 项目介绍
本项目提供了一个全面、系统的Jinja2学习资源，涵盖从基础到高级的所有核心知识点。通过详细的教程文档和可执行的示例代码，帮助您系统性地学习和掌握Jinja2模板引擎。

## 目录结构
```
ThematicModules/jinja2/
├── docs/              # 教程文档目录
├── examples/          # 示例代码目录
├── templates/         # 模板文件目录
│   ├── includes/      # 可包含的模板文件
│   └── macros/        # 宏定义文件
├── exercises/         # 练习项目目录
│   └── solutions/     # 练习参考答案
├── requirements.txt   # 依赖包配置
└── README.md          # 项目说明文档
```

## 安装和使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行示例
每个示例代码都可以独立运行：
```bash
cd examples
python basic_usage.py
```

### 3. 学习方式
1. 首先阅读docs目录下的教程文档，按顺序学习各个知识点
2. 然后运行对应的示例代码，观察实际效果
3. 尝试修改模板文件或示例代码，加深理解
4. 完成exercises目录下的练习，巩固学习成果

## 学习路径

### 初级阶段
- [基础语法](docs/01_basic_syntax.md)：了解Jinja2的基本语法和用法
- [变量和过滤器](docs/02_variables_and_filters.md)：学习如何在模板中使用变量和过滤器
- [控制结构](docs/03_control_structures.md)：掌握条件判断和循环等控制结构

### 中级阶段
- [模板继承](docs/04_template_inheritance.md)：学习模板继承和布局复用
- [宏和包含](docs/05_macros_and_includes.md)：掌握宏定义和模板包含的使用
- [上下文和环境配置](docs/06_context_and_environment.md)：了解Jinja2的上下文和环境配置

### 高级阶段
- [扩展开发](docs/07_extensions.md)：学习如何开发自定义扩展
- [安全性](docs/08_security.md)：了解Jinja2的安全特性和最佳实践
- [性能优化](docs/09_performance.md)：学习如何优化Jinja2的性能

## 适用对象
- 对Python有基础了解的初学者
- 需要使用Jinja2进行模板开发的开发者
- 希望系统学习模板引擎的技术人员

## 其他说明
- 所有示例代码均在Python 3.8+环境下测试通过
- 如有问题或建议，请随时提出
- 祝您学习愉快！