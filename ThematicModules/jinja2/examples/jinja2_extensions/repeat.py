"""
重复标签扩展

此扩展提供了一个`{% repeat n %}...{% endrepeat %}`标签，用于在模板中重复执行一段代码指定的次数。
它还提供了循环信息（如索引、是否是第一个/最后一个元素等），类似于内置的for循环。
"""

from jinja2.ext import Extension
from jinja2.nodes import CallBlock, Const, Name, TemplateReference
from jinja2.runtime import LoopContext

class RepeatExtension(Extension):
    """Jinja2重复标签扩展，允许重复执行模板代码块"""
    
    # 扩展名称，用于注册和配置
    name = 'repeat'
    
    # 定义此扩展处理的标签
    tags = {'repeat'}
    
    def parse(self, parser):
        """
        解析模板中的repeat标签
        
        参数:
            parser: Jinja2解析器实例
        
        返回:
            表示重复代码块的节点
        """
        # 获取当前行号，用于错误报告
        lineno = next(parser.stream).lineno
        
        # 解析重复次数表达式（count参数）
        count = parser.parse_expression()
        
        # 可选的变量名，用于存储循环索引
        loop_var = None
        if parser.stream.skip_if('name:as'):
            loop_var = parser.stream.expect('name').value
            parser.stream.expect('block_end')
        else:
            # 确保有结束括号
            parser.stream.expect('block_end')
        
        # 解析重复的内容直到遇到endrepeat标签
        body = parser.parse_statements(['name:endrepeat'], drop_needle=True)
        
        # 创建一个CallBlock节点，调用我们的_repeat函数
        call_block = CallBlock(
            self.call_method('_repeat', [count]),
            [], [], body
        ).set_lineno(lineno)
        
        # 如果指定了循环变量，将循环索引赋值给它
        if loop_var:
            # 创建一个赋值节点，将循环索引存储到指定变量
            # 注意：这部分逻辑比较复杂，这里简化处理，实际使用中可能需要更复杂的实现
            pass
        
        return call_block
    
    def _repeat(self, count, caller):
        """
        重复执行caller函数指定次数
        
        参数:
            count (int): 重复次数
            caller: 包含要重复执行的模板代码的函数
        
        返回:
            str: 重复执行后的结果字符串
        """
        # 确保count是整数
        try:
            count = int(count)
            # 防止负数或过大的数
            if count < 0:
                count = 0
            elif count > 1000:  # 限制最大重复次数，防止无限循环
                count = 1000
        except (ValueError, TypeError):
            count = 0
        
        result = []
        for i in range(count):
            # 创建循环上下文对象，提供循环信息
            loop = LoopContext(
                index0=i,             # 从0开始的索引
                index=i+1,            # 从1开始的索引
                revindex0=count-i-1,  # 从0开始的反向索引
                revindex=count-i,     # 从1开始的反向索引
                first=i == 0,         # 是否是第一个元素
                last=i == count-1,    # 是否是最后一个元素
                length=count,         # 总长度
                depth0=0,             # 嵌套深度（从0开始）
                depth=1               # 嵌套深度（从1开始）
            )
            
            # 调用caller函数，传递循环信息
            result.append(caller(loop=loop))
        
        # 连接所有结果并返回
        return ''.join(result)

# 为方便单独使用，提供直接的函数访问
def get_repeat_extension():
    """获取重复标签扩展的实例"""
    return RepeatExtension