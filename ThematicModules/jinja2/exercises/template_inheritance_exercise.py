# -*- coding: utf-8 -*-

"""
Jinja2模板继承练习

这个练习将帮助你熟悉Jinja2的模板继承机制。
请完成以下任务：

1. 创建Jinja2环境
2. 加载基础模板和子模板
3. 准备上下文数据，包含以下变量：
   - page_title: 页面标题
   - site_name: 网站名称
   - navigation: 导航菜单数据
   - content: 页面内容
   - footer_text: 页脚文本
4. 渲染子模板并打印结果
5. 尝试创建多个不同的子模板，展示模板继承的灵活性
6. 使用super()函数在子模板中调用父模板的内容

完成后运行这个脚本，确保一切正常工作。
"""

from jinja2 import Environment, FileSystemLoader

# TODO: 创建Jinja2环境
env = None

# TODO: 准备上下文数据
context = {
    'page_title': 'Jinja2模板继承练习',
    'site_name': 'Jinja2学习中心',
    'navigation': [
        {'name': '首页', 'url': '/'},
        {'name': '教程', 'url': '/tutorials'},
        {'name': '练习', 'url': '/exercises'},
        {'name': '资源', 'url': '/resources'}
    ],
    'content': '这是页面的主要内容，在子模板中定义。',
    'footer_text': '© 2025 Jinja2学习中心 - 版权所有'
}

# TODO: 加载子模板文件'child_exercise.html'
template = None

# TODO: 渲染模板
output = None

# TODO: 打印渲染结果
print("=== 模板继承练习渲染结果开始 ===")
# 在这里打印输出
print("=== 模板继承练习渲染结果结束 ===")

# TODO: 将渲染结果保存到文件

# TODO: 尝试创建并渲染另一个子模板

print("模板继承练习完成！")