"""
调试扩展

此扩展提供了一系列用于调试模板的工具，包括：
- `{% debug [label] %}...{% enddebug %}`标签：捕获和显示块渲染过程中的调试信息
- `{% dump var %}`标签：显示变量的详细信息
- `{% timeit %}...{% endtimeit %}`标签：测量代码块的执行时间
- 调试过滤器和全局函数
"""

from jinja2.ext import Extension
from jinja2.nodes import CallBlock, Name, Const, TemplateData
import traceback
import sys
import time
import pprint
import inspect

class DebugExtension(Extension):
    """Jinja2调试扩展，提供模板调试工具"""
    
    # 扩展名称，用于注册和配置
    name = 'debug'
    
    # 定义此扩展处理的标签
    tags = {'debug', 'dump', 'timeit'}
    
    def __init__(self, environment):
        """
        初始化扩展，注册过滤器和全局函数
        
        参数:
            environment: Jinja2环境实例
        """
        super().__init__(environment)
        
        # 设置是否在生产环境启用调试（默认为False）
        self.debug_enabled = getattr(environment, 'debug', False)
        
        # 注册调试过滤器
        environment.filters['debug_print'] = self.debug_print_filter
        environment.filters['type_of'] = self.type_of_filter
        environment.filters['dir_of'] = self.dir_of_filter
        environment.filters['json_debug'] = self.json_debug_filter
        
        # 注册调试全局函数
        environment.globals['debug_print'] = self.debug_print_global
        environment.globals['get_context'] = self.get_context_global
        environment.globals['get_env_config'] = self.get_env_config_global
        environment.globals['log_message'] = self.log_message_global
    
    def parse(self, parser):
        """
        解析模板中的调试标签
        
        参数:
            parser: Jinja2解析器实例
        
        返回:
            表示调试块的节点
        """
        # 获取当前token，确定是哪个标签
        token = next(parser.stream)
        lineno = token.lineno
        
        if token.value == 'debug':
            return self._parse_debug_tag(parser, lineno)
        elif token.value == 'dump':
            return self._parse_dump_tag(parser, lineno)
        elif token.value == 'timeit':
            return self._parse_timeit_tag(parser, lineno)
        
        # 如果不是已知标签，抛出错误
        parser.fail(f"未知的调试标签: {token.value}", lineno)
    
    def _parse_debug_tag(self, parser, lineno):
        """解析debug标签"""
        # 解析可选的标签名
        label = None
        if not parser.stream.current.type == 'block_end':
            label = parser.parse_expression()
        
        parser.stream.expect('block_end')
        
        # 解析调试块内容
        body = parser.parse_statements(['name:enddebug'], drop_needle=True)
        
        # 创建CallBlock节点
        return CallBlock(
            self.call_method('_debug_block', [label]),
            [], [], body
        ).set_lineno(lineno)
    
    def _parse_dump_tag(self, parser, lineno):
        """解析dump标签"""
        # 解析要转储的变量
        var_name = parser.stream.expect('name').value
        
        # 可选的格式化选项
        format_option = None
        if parser.stream.skip_if('comma'):
            format_option = parser.parse_expression()
        
        parser.stream.expect('block_end')
        
        # 创建表达式节点，调用_dump_variable函数
        return CallBlock(
            self.call_method('_dump_variable', [Const(var_name)]),
            [Name(var_name, 'load')], [], []
        ).set_lineno(lineno)
    
    def _parse_timeit_tag(self, parser, lineno):
        """解析timeit标签"""
        # 解析可选的标签名
        label = None
        if not parser.stream.current.type == 'block_end':
            label = parser.parse_expression()
        
        parser.stream.expect('block_end')
        
        # 解析计时块内容
        body = parser.parse_statements(['name:endtimeit'], drop_needle=True)
        
        # 创建CallBlock节点
        return CallBlock(
            self.call_method('_timeit_block', [label]),
            [], [], body
        ).set_lineno(lineno)
    
    def _debug_block(self, label, caller):
        """执行调试块并添加调试信息"""
        if not self.debug_enabled:
            # 如果调试未启用，直接执行内容
            return caller()
        
        try:
            # 记录开始时间
            start_time = time.time()
            
            # 执行块内容
            content = caller()
            
            # 计算执行时间
            execution_time = (time.time() - start_time) * 1000  # 转换为毫秒
            
            # 创建调试信息
            label_text = label or 'Block'
            debug_info = f"<!-- DEBUG: {label_text} rendered in {execution_time:.2f}ms -->"
            
            return content + debug_info
        except Exception as e:
            # 捕获并格式化错误信息
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            # 获取错误的堆栈跟踪，但只保留与模板相关的部分
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            
            # 过滤掉不相关的堆栈帧
            filtered_tb = []
            for line in tb_lines:
                # 保留与模板相关的行或错误类型行
                if 'template' in line.lower() or 'error' in line.lower() or 'traceback' in line.lower():
                    filtered_tb.append(line)
            
            # 限制堆栈跟踪的长度
            if len(filtered_tb) > 10:
                filtered_tb = filtered_tb[:10] + ['...\n']
            
            error_info = ''.join(filtered_tb)
            
            label_text = label or 'Block'
            debug_info = f"<!-- DEBUG ERROR: {label_text} failed with: {error_info} -->"
            
            # 在调试模式下，返回错误信息而不是抛出异常
            return debug_info
    
    def _dump_variable(self, var_name, var_value):
        """显示变量的详细信息"""
        if not self.debug_enabled:
            return ''
        
        try:
            # 获取变量类型
            var_type = type(var_value).__name__
            
            # 获取变量的字符串表示，限制长度
            var_repr = repr(var_value)
            if len(var_repr) > 500:
                var_repr = var_repr[:500] + '...'
            
            # 对于复杂类型，获取更多信息
            additional_info = ''
            if hasattr(var_value, '__len__'):
                try:
                    additional_info += f", length={len(var_value)}"
                except (TypeError, AttributeError):
                    pass
            
            # 创建调试信息
            debug_output = f"<!-- DUMP: {var_name} ({var_type}{additional_info}) = {var_repr} -->"
            
            return debug_output
        except Exception as e:
            return f"<!-- DUMP ERROR: Could not dump {var_name}: {str(e)} -->"
    
    def _timeit_block(self, label, caller):
        """测量块的执行时间"""
        if not self.debug_enabled:
            return caller()
        
        try:
            # 执行多次以获得更准确的测量结果
            num_runs = 1
            
            # 如果执行时间很短，可以增加运行次数
            quick_test_start = time.time()
            caller()  # 快速测试
            quick_test_time = time.time() - quick_test_start
            
            if quick_test_time < 0.001:  # 如果小于1ms
                num_runs = 1000
            elif quick_test_time < 0.01:  # 如果小于10ms
                num_runs = 100
            elif quick_test_time < 0.1:  # 如果小于100ms
                num_runs = 10
            
            # 实际测量
            start_time = time.time()
            for _ in range(num_runs):
                caller()
            total_time = time.time() - start_time
            
            # 计算平均执行时间
            avg_time = (total_time / num_runs) * 1000  # 转换为毫秒
            
            label_text = label or 'Block'
            debug_info = f"<!-- TIMEIT: {label_text} - {num_runs} runs, avg: {avg_time:.4f}ms, total: {total_time*1000:.2f}ms -->"
            
            # 只执行一次并返回实际内容
            actual_content = caller()
            return actual_content + debug_info
        except Exception as e:
            label_text = label or 'Block'
            return f"<!-- TIMEIT ERROR: {label_text} failed with: {str(e)} -->"
    
    def debug_print_filter(self, value, label=None):
        """调试过滤器：打印变量的值到控制台"""
        if self.debug_enabled:
            label_text = label or 'DEBUG'
            print(f"{label_text}: {value}")
        return value  # 返回原始值，不影响模板渲染
    
    def type_of_filter(self, value):
        """调试过滤器：返回变量的类型"""
        return type(value).__name__
    
    def dir_of_filter(self, value):
        """调试过滤器：返回变量的属性和方法列表"""
        if hasattr(value, '__dir__'):
            return dir(value)
        return []
    
    def json_debug_filter(self, value):
        """调试过滤器：将变量转换为JSON格式的字符串"""
        import json
        try:
            # 尝试使用pprint进行格式化
            return pprint.pformat(value)
        except Exception:
            try:
                # 如果pprint失败，尝试使用json.dumps
                return json.dumps(value, default=str, ensure_ascii=False, indent=2)
            except Exception as e:
                return f"<无法序列化: {str(e)}>"
    
    def debug_print_global(self, *args, **kwargs):
        """调试全局函数：打印信息到控制台"""
        if self.debug_enabled:
            print("DEBUG:", *args, **kwargs)
    
    def get_context_global(self, context):
        """调试全局函数：获取当前模板上下文"""
        if not self.debug_enabled:
            return {}
        
        # 返回上下文的副本，移除可能包含敏感信息的项
        safe_context = {}
        for key, value in context.items():
            # 跳过内部变量和函数
            if not key.startswith('_'):
                try:
                    # 尝试序列化，确保可以安全显示
                    repr(value)
                    safe_context[key] = value
                except Exception:
                    safe_context[key] = f"<无法显示: {type(value).__name__}>"
        
        return safe_context
    
    def get_env_config_global(self):
        """调试全局函数：获取Jinja2环境配置"""
        if not self.debug_enabled:
            return {}
        
        # 返回环境配置的相关信息
        config = {
            'loader': str(self.environment.loader),
            'autoescape': self.environment.autoescape.__class__.__name__,
            'extensions': [ext.name for ext in self.environment.extensions.values()],
            'cache_size': getattr(self.environment, 'cache_size', 'default'),
            'trim_blocks': self.environment.trim_blocks,
            'lstrip_blocks': self.environment.lstrip_blocks,
        }
        
        return config
    
    def log_message_global(self, message, level='info'):
        """调试全局函数：记录消息"""
        if not self.debug_enabled:
            return
        
        # 在实际应用中，这里可以集成到正式的日志系统
        print(f"[{level.upper()}] {message}")

# 为方便单独使用，提供直接的函数访问
def get_debug_extension():
    """获取调试扩展的实例"""
    return DebugExtension