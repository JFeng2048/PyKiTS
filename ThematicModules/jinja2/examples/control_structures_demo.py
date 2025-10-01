from jinja2 import Environment, FileSystemLoader
import datetime

# 配置Jinja2环境
def setup_environment(templates_dir='../templates'):
    """设置Jinja2环境，加载指定目录下的模板"""
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True
    )
    return env

# 准备示例数据
def prepare_context_data():
    """准备用于演示控制结构的上下文数据"""
    # 基本用户信息
    user = {
        'username': '张三',
        'is_logged_in': True,
        'is_admin': False,
        'age': 25,
        'country': 'China',
        'roles': ['user', 'editor'],
        'score': 85
    }
    
    # 列表数据
    items = ['苹果', '香蕉', '橙子', '葡萄', '草莓']
    
    # 空列表
    empty_list = []
    
    # 用于演示break和continue的列表
    items_with_control = ['开始', '项目1', 'skip', '项目2', 'stop', '不应该显示的项目']
    
    # 表格数据（嵌套列表）
    table_data = [
        ['姓名', '年龄', '职位'],
        ['张三', 25, '工程师'],
        ['李四', 30, '产品经理'],
        ['王五', 28, '设计师']
    ]
    
    # 用户列表（字典列表）
    users = [
        {'username': '用户1', 'is_active': True},
        {'username': '用户2', 'is_active': False},
        {'username': '用户3', 'is_active': True},
        {'username': '用户4', 'is_active': False}
    ]
    
    # 完整上下文数据
    context = {
        'user': user,
        'items': items,
        'empty_list': empty_list,
        'items_with_control': items_with_control,
        'table_data': table_data,
        'users': users,
        'current_time': datetime.datetime.now(),
        'score': 85
    }
    
    return context

# 渲染并显示模板
def render_template(env, template_name, context):
    """渲染指定的模板并返回结果"""
    template = env.get_template(template_name)
    return template.render(**context)

# 基本条件语句示例
def demonstrate_basic_conditionals(env, context):
    """演示基本的条件语句"""
    print("=== 基本条件语句示例 ===")
    
    # 简单的if语句
    simple_template = """
{% if user.is_logged_in %}
欢迎回来，{{ user.username }}！
{% endif %}
"""
    
    # if-else语句
    if_else_template = """
{% if user.is_admin %}
您是管理员。
{% else %}
您是普通用户。
{% endif %}
"""
    
    # if-elif-else语句
    grade_template = """
{% if score >= 90 %}
成绩：优秀
{% elif score >= 80 %}
成绩：良好
{% elif score >= 60 %}
成绩：及格
{% else %}
成绩：不及格
{% endif %}
"""
    
    # 渲染并打印结果
    print("1. if语句:")
    print(env.from_string(simple_template).render(**context))
    
    print("2. if-else语句:")
    print(env.from_string(if_else_template).render(**context))
    
    print("3. if-elif-else语句:")
    print(env.from_string(grade_template).render(**context))
    print()

# 条件运算符示例
def demonstrate_operators(env, context):
    """演示条件运算符"""
    print("=== 条件运算符示例 ===")
    
    # 逻辑运算符示例
    logic_template = """
{% if user.age >= 18 and user.country == 'China' %}
您符合条件。
{% endif %}
"""
    
    # 成员运算符示例
    member_template = """
{% if 'admin' in user.roles %}
您有管理员权限。
{% else %}
您没有管理员权限。
{% endif %}
"""
    
    # 测试运算符示例
    test_template = """
{% if variable is defined %}
变量已定义: {{ variable }}
{% else %}
变量未定义。
{% endif %}
"""
    
    # 渲染并打印结果
    print("1. 逻辑运算符 (and, or, not):")
    print(env.from_string(logic_template).render(**context))
    
    print("2. 成员运算符 (in, not in):")
    print(env.from_string(member_template).render(**context))
    
    print("3. 测试运算符 (is, is not):")
    print(env.from_string(test_template).render(**context))
    print()

# 循环示例
def demonstrate_loops(env, context):
    """演示循环结构"""
    print("=== 循环结构示例 ===")
    
    # 基本列表循环
    list_loop_template = """
列表项:
{% for item in items %}
- {{ item }}
{% endfor %}
"""
    
    # 字典循环
    dict_loop_template = """
用户信息:
{% for key, value in user.items() %}
{{ key }}: {{ value }}
{% endfor %}
"""
    
    # 循环索引和属性
    index_loop_template = """
带索引的列表:
{% for item in items %}
{{ loop.index }}. {{ item }}
{% if loop.first %} - 第一个元素{% endif %}
{% if loop.last %} - 最后一个元素{% endif %}
{% endfor %}
总共有 {{ loop.length }} 个元素
"""
    
    # else子句
    else_loop_template = """
{% for item in empty_list %}
- {{ item }}
{% else %}
列表为空
{% endfor %}
"""
    
    # 渲染并打印结果
    print("1. 基本列表循环:")
    print(env.from_string(list_loop_template).render(**context))
    
    print("2. 字典循环:")
    print(env.from_string(dict_loop_template).render(**context))
    
    print("3. 循环索引和属性:")
    print(env.from_string(index_loop_template).render(**context))
    
    print("4. else子句 (列表为空时):")
    print(env.from_string(else_loop_template).render(**context))
    print()

# 循环控制示例
def demonstrate_loop_control(env, context):
    """演示循环控制（break和continue）"""
    print("=== 循环控制示例 ===")
    
    # break和continue示例
    control_template = """
处理项目列表 (遇到'stop'停止，遇到'skip'跳过):
{% for item in items_with_control %}
{% if item == 'stop' %}
{% break %}
{% endif %}
{% if item == 'skip' %}
{% continue %}
{% endif %}
- {{ item }}
{% endfor %}
"""
    
    # 渲染并打印结果
    print(env.from_string(control_template).render(**context))
    print()

# 嵌套循环示例
def demonstrate_nested_loops(env, context):
    """演示嵌套循环"""
    print("=== 嵌套循环示例 ===")
    
    # 嵌套循环（表格数据）
    nested_template = """
表格数据:
{% for row in table_data %}
{% for cell in row %}
{{ cell }}	{% endfor %}
{% endfor %}
"""
    
    # 循环与条件结合
    loop_conditional_template = """
用户状态列表:
{% for user in users %}
{% if user.is_active %}
* {{ user.username }} (活跃)
{% else %}
* {{ user.username }} (非活跃)
{% endif %}
{% endfor %}
"""
    
    # 渲染并打印结果
    print("1. 嵌套循环（表格数据）:")
    print(env.from_string(nested_template).render(**context))
    
    print("2. 循环与条件结合:")
    print(env.from_string(loop_conditional_template).render(**context))
    print()

# 主函数
def main():
    """主函数，运行所有示例"""
    # 设置环境
    env = setup_environment()
    
    # 准备上下文数据
    context = prepare_context_data()
    
    # 运行各种示例
    demonstrate_basic_conditionals(env, context)
    demonstrate_operators(env, context)
    demonstrate_loops(env, context)
    demonstrate_loop_control(env, context)
    demonstrate_nested_loops(env, context)
    
    # 渲染完整的HTML模板
    html_output = render_template(env, 'control_example.html', context)
    
    # 将HTML输出保存到文件
    with open('../output/control_structures_demo.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"完整的HTML示例已保存到 ../output/control_structures_demo.html")
    print(f"您可以在浏览器中打开该文件查看所有控制结构的演示")

if __name__ == '__main__':
    # 确保输出目录存在
    import os
    os.makedirs('../output', exist_ok=True)
    
    # 运行主函数
    main()