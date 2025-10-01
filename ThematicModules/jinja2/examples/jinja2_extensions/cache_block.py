"""
缓存块扩展

此扩展提供了一个`{% cache key [, timeout] %}...{% endcache %}`标签，用于在模板中缓存特定块的内容。
它可以显著提高重复渲染相同内容的模板的性能，特别是对于包含数据库查询或复杂计算的内容。
"""

from jinja2.ext import Extension
from jinja2.nodes import Block, CallBlock, Name, Const
import time
import hashlib
import uuid

class CacheBlockExtension(Extension):
    """Jinja2缓存块扩展，用于缓存模板中特定块的内容"""
    
    # 扩展名称，用于注册和配置
    name = 'cache'
    
    # 定义此扩展处理的标签
    tags = {'cache'}
    
    def __init__(self, environment):
        """
        初始化扩展，设置缓存字典
        
        参数:
            environment: Jinja2环境实例
        """
        super().__init__(environment)
        
        # 初始化内存缓存字典
        self.cache = {}
        
        # 设置默认缓存超时时间（秒）
        self.default_timeout = environment.cache_timeout if hasattr(environment, 'cache_timeout') else 3600
        
        # 可选的缓存键前缀，用于区分不同应用或环境的缓存
        self.cache_prefix = environment.cache_prefix if hasattr(environment, 'cache_prefix') else ''
        
        # 最大缓存项数量，防止内存溢出
        self.max_cache_size = environment.max_cache_size if hasattr(environment, 'max_cache_size') else 1000
    
    def parse(self, parser):
        """
        解析模板中的cache标签
        
        参数:
            parser: Jinja2解析器实例
        
        返回:
            表示缓存块的节点
        """
        # 获取当前行号，用于错误报告
        lineno = next(parser.stream).lineno
        
        # 解析缓存键表达式
        cache_key = parser.parse_expression()
        
        # 可选的过期时间（以秒为单位）
        expire_time = None
        if parser.stream.skip_if('comma'):
            expire_time = parser.parse_expression()
        
        # 确保有结束括号
        parser.stream.expect('block_end')
        
        # 解析缓存块内容直到遇到endcache标签
        body = parser.parse_statements(['name:endcache'], drop_needle=True)
        
        # 创建CallBlock节点，调用我们的_cache_block函数
        return CallBlock(
            self.call_method('_cache_block', [cache_key, expire_time]),
            [], [], body
        ).set_lineno(lineno)
    
    def _cache_key_to_string(self, key):
        """
        将缓存键转换为字符串形式
        
        参数:
            key: 原始缓存键（可以是任何类型）
        
        返回:
            str: 处理后的缓存键字符串
        """
        # 如果键已经是字符串，直接使用
        if isinstance(key, str):
            cache_key = key
        else:
            # 对于其他类型，转换为字符串表示
            cache_key = str(key)
        
        # 添加前缀
        if self.cache_prefix:
            cache_key = f"{self.cache_prefix}:{cache_key}"
        
        # 对长键进行哈希处理，防止键过长
        if len(cache_key) > 256:
            cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        
        return cache_key
    
    def _cache_block(self, cache_key, expire_time, caller):
        """
        实现缓存逻辑
        
        参数:
            cache_key: 缓存键
            expire_time: 过期时间（秒），None表示使用默认值
            caller: 包含要缓存的模板代码的函数
        
        返回:
            str: 缓存的或新渲染的内容
        """
        # 获取当前时间戳
        current_time = time.time()
        
        # 处理缓存键
        cache_key_str = self._cache_key_to_string(cache_key)
        
        # 确定过期时间
        if expire_time is None:
            expire_time = self.default_timeout
        else:
            try:
                expire_time = int(expire_time)
                # 确保过期时间为正数
                if expire_time < 0:
                    expire_time = self.default_timeout
            except (ValueError, TypeError):
                expire_time = self.default_timeout
        
        # 检查缓存是否有效
        if cache_key_str in self.cache:
            cached_content, timestamp = self.cache[cache_key_str]
            # 如果缓存未过期，则返回缓存内容
            if (current_time - timestamp) < expire_time:
                return cached_content
            # 否则删除过期缓存
            else:
                del self.cache[cache_key_str]
        
        # 检查缓存大小，如果超过限制，删除一些旧的缓存项
        if len(self.cache) >= self.max_cache_size:
            # 获取所有缓存项及其时间戳
            cache_items = [(k, v[1]) for k, v in self.cache.items()]
            # 按时间戳排序，删除最早的一半缓存项
            cache_items.sort(key=lambda x: x[1])
            for k, _ in cache_items[:len(cache_items) // 2]:
                if k in self.cache:
                    del self.cache[k]
        
        # 渲染内容
        content = caller()
        
        # 缓存渲染结果
        self.cache[cache_key_str] = (content, current_time)
        
        return content
    
    def clear_cache(self, key=None):
        """
        清除缓存
        
        参数:
            key: 可选，特定的缓存键，如果为None，清除所有缓存
        """
        if key is None:
            self.cache.clear()
        else:
            cache_key_str = self._cache_key_to_string(key)
            if cache_key_str in self.cache:
                del self.cache[cache_key_str]
    
    def get_cache_info(self):
        """
        获取缓存信息
        
        返回:
            dict: 包含缓存统计信息的字典
        """
        return {
            'size': len(self.cache),
            'max_size': self.max_cache_size,
            'default_timeout': self.default_timeout,
            'prefix': self.cache_prefix
        }

# 为方便单独使用，提供直接的函数访问
def get_cache_block_extension():
    """获取缓存块扩展的实例"""
    return CacheBlockExtension