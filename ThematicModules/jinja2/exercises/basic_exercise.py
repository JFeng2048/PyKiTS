# -*- coding: utf-8 -*-

"""
Jinja2基础语法练习

这个练习将帮助你熟悉Jinja2的基本语法和使用方法。
请完成以下任务：

1. 创建Jinja2环境，设置正确的模板加载器
2. 加载模板文件'basic_exercise.html'（你需要自己创建这个模板文件）
3. 准备上下文数据，包含以下变量：
   - name: 你的名字
   - age: 你的年龄
   - skills: 一个包含你技能的列表
   - contact: 一个包含email和phone的字典
   - current_time: 当前时间
4. 渲染模板并打印结果
5. 将渲染结果保存到文件'rendered_basic_exercise.html'
6. 使用from_string方法直接渲染一个简单的字符串模板

完成后运行这个脚本，确保一切正常工作。
"""

from jinja2 import Environment, FileSystemLoader
import datetime

# TODO: 创建Jinja2环境，设置模板加载器和自动转义
env = None

# TODO: 加载模板文件'basic_exercise.html'
template = None

# TODO: 准备上下文数据
context = {
    # 请填写你的信息
}

# TODO: 渲染模板
output = None

# TODO: 打印渲染结果
print("=== 渲染结果开始 ===")
# 在这里打印输出
print("=== 渲染结果结束 ===")

# TODO: 将渲染结果保存到文件

# TODO: 使用from_string方法直接渲染一个简单的字符串模板

print("基础语法练习完成！")