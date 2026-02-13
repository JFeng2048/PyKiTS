# -*- coding:utf-8 -*-
# file:do_parse.py
import ast

# 解析一段简单的代码
source_code = """
def greet(name):
    return 'Hello, ' + name
"""

tree = ast.parse(source_code) # 解析为AST
print(ast.dump(tree, indent=4)) # 以可读格式打印AST结构


'''
关键理解：ast.dump()的输出展示了树的层次结构。你会看到 Module作为根节点，其 body包含一个 FunctionDef节点，
这个节点内部又包含函数名 (name)、参数 (args) 和函数体 (body)，函数体本身由其他语句节点（如 Return）组成。
每个节点都是一个对象，拥有描述其特定作用的属性
'''

class AnalysisVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.variables = set()

    def visit_FunctionDef(self, node):
        # 当访问到函数定义节点时调用
        self.functions.append(node.name)
        self.generic_visit(node)  # 继续遍历该节点的子节点

    def visit_Assign(self, node):
        # 当访问到赋值语句节点时调用
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)
        self.generic_visit(node)

# 使用访问者遍历AST
visitor = AnalysisVisitor()
visitor.visit(tree)

print("函数列表:", visitor.functions)
print("变量集合:", visitor.variables)



class RenameTransformer(ast.NodeTransformer):
    def visit_Name(self, node):
        # 当访问到变量名节点时调用
        if node.id == 'x':
            # 创建一个新的变量名节点，并复制原节点的位置信息
            new_node = ast.Name(id='new_x', ctx=node.ctx)
            ast.copy_location(new_node, node) # 保持行号等信息
            return new_node  # 返回新节点以替换原节点
        return node  # 如果不修改，则返回原节点

# 应用转换器
transformer = RenameTransformer()
modified_tree = transformer.visit(tree)

# 注意：修改AST后，通常需要修复行号信息
ast.fix_missing_locations(modified_tree)