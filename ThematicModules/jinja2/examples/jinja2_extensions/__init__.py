"""
Jinja2扩展开发示例包

此包包含了各种Jinja2扩展的示例实现，包括：
- 文本处理扩展
- 重复标签扩展
- 缓存块扩展
- 调试扩展
- 配置扩展
- 综合扩展

每个扩展都演示了不同的Jinja2扩展开发技术和用例。
"""

# 导入所有扩展以供使用
from .text_processing import TextProcessingExtension
from .repeat import RepeatExtension
from .cache_block import CacheBlockExtension
from .debug import DebugExtension
from .configurable import ConfigurableExtension
from .comprehensive import ComprehensiveExtension

# 定义版本信息
__version__ = '1.0.0'

# 提供扩展列表，方便一次性注册所有扩展
ALL_EXTENSIONS = [
    TextProcessingExtension,
    RepeatExtension,
    CacheBlockExtension,
    DebugExtension,
    ConfigurableExtension,
    ComprehensiveExtension
]

__all__ = [
    'TextProcessingExtension',
    'RepeatExtension',
    'CacheBlockExtension',
    'DebugExtension',
    'ConfigurableExtension',
    'ComprehensiveExtension',
    'ALL_EXTENSIONS',
    '__version__'
]