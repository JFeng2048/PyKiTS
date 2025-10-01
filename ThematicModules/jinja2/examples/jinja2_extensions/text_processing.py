"""
文本处理扩展

此扩展提供了一系列文本处理相关的过滤器、测试和全局函数，用于增强Jinja2模板的文本处理能力。
"""

from jinja2.ext import Extension
import re
import string

class TextProcessingExtension(Extension):
    """Jinja2文本处理扩展，提供常用的文本处理功能"""
    
    # 扩展名称，用于注册和配置
    name = 'text_processing'
    
    def __init__(self, environment):
        """初始化扩展，注册过滤器、测试和全局函数"""
        super().__init__(environment)
        
        # 注册过滤器
        environment.filters['truncate_words'] = self.truncate_words
        environment.filters['highlight'] = self.highlight
        environment.filters['slugify'] = self.slugify
        environment.filters['remove_html'] = self.remove_html
        environment.filters['word_wrap'] = self.word_wrap
        environment.filters['abbreviate'] = self.abbreviate
        environment.filters['capitalize_words'] = self.capitalize_words
        environment.filters['replace_words'] = self.replace_words
        
        # 注册测试
        environment.tests['contains_words'] = self.contains_words
        environment.tests['starts_with'] = self.starts_with
        environment.tests['ends_with'] = self.ends_with
        environment.tests['is_email'] = self.is_email
        environment.tests['is_url'] = self.is_url
        
        # 注册全局函数
        environment.globals['count_words'] = self.count_words
        environment.globals['generate_token'] = self.generate_token
        environment.globals['format_number'] = self.format_number

    def truncate_words(self, text, max_words=10, suffix='...'):
        """
        截断文本到指定的单词数量
        
        参数:
            text (str): 要截断的文本
            max_words (int): 最大单词数量
            suffix (str): 截断后添加的后缀
        
        返回:
            str: 截断后的文本
        """
        if not text or not isinstance(text, str):
            return text
        words = text.split()
        if len(words) <= max_words:
            return text
        return ' '.join(words[:max_words]) + suffix

    def highlight(self, text, keyword, css_class='highlight', case_sensitive=False):
        """
        高亮显示文本中的关键词
        
        参数:
            text (str): 要处理的文本
            keyword (str/list): 要高亮的关键词，可以是单个关键词或关键词列表
            css_class (str): 高亮元素的CSS类名
            case_sensitive (bool): 是否区分大小写
        
        返回:
            str: 包含高亮标记的文本
        """
        if not text or not isinstance(text, str) or not keyword:
            return text
        
        # 如果关键词是列表，将其转换为正则表达式的OR模式
        if isinstance(keyword, (list, tuple)):
            pattern = '|'.join([re.escape(k) for k in keyword if k])
        else:
            pattern = re.escape(keyword)
        
        # 设置正则表达式标志
        flags = 0 if case_sensitive else re.IGNORECASE
        
        # 执行替换
        return re.sub(f'({pattern})', f'<span class="{css_class}">\\1</span>', text, flags=flags)

    def slugify(self, text, separator='-', allow_unicode=False):
        """
        将文本转换为URL友好的格式（slug）
        
        参数:
            text (str): 要转换的文本
            separator (str): 用于替换非字母数字字符的分隔符
            allow_unicode (bool): 是否允许Unicode字符
        
        返回:
            str: URL友好的文本
        """
        if not text or not isinstance(text, str):
            return text
        
        # 转换为小写
        text = text.lower()
        
        # 如果不允许Unicode，将非ASCII字符转换为ASCII
        if not allow_unicode:
            import unicodedata
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        
        # 替换非字母数字字符为分隔符
        text = re.sub(r'[^a-z0-9]+', separator, text)
        
        # 移除首尾的分隔符
        text = text.strip(separator)
        
        return text

    def remove_html(self, text, preserve_whitespace=True):
        """
        移除文本中的HTML标签
        
        参数:
            text (str): 包含HTML的文本
            preserve_whitespace (bool): 是否保留空格
        
        返回:
            str: 移除HTML后的纯文本
        """
        if not text or not isinstance(text, str):
            return text
        
        # 移除HTML标签
        text = re.sub(r'<[^>]*>', '', text)
        
        # 如果不保留多余的空格，将多个空格替换为单个空格
        if not preserve_whitespace:
            text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def word_wrap(self, text, width=72, break_long_words=True):
        """
        对文本进行自动换行
        
        参数:
            text (str): 要换行的文本
            width (int): 每行的最大宽度
            break_long_words (bool): 是否断开长单词
        
        返回:
            str: 换行后的文本
        """
        if not text or not isinstance(text, str):
            return text
        
        result = []
        lines = text.split('\n')
        
        for line in lines:
            if len(line) <= width:
                result.append(line)
                continue
            
            # 处理需要换行的行
            current_line = ''
            words = line.split(' ')
            
            for word in words:
                # 如果单词本身超过宽度并且允许断开
                if len(word) > width and break_long_words:
                    # 断开长单词
                    while word:
                        if not current_line:
                            # 如果当前行是空的，直接取最大宽度的部分
                            result.append(word[:width])
                            word = word[width:]
                        else:
                            # 否则，计算剩余空间
                            remaining = width - len(current_line) - 1  # -1 是为了空格
                            if remaining <= 0:
                                # 没有剩余空间，换行
                                result.append(current_line)
                                current_line = ''
                            else:
                                # 取尽可能多的字符
                                take = min(len(word), remaining)
                                current_line += ' ' + word[:take]
                                word = word[take:]
                else:
                    # 普通单词处理
                    if not current_line:
                        current_line = word
                    elif len(current_line) + 1 + len(word) <= width:
                        current_line += ' ' + word
                    else:
                        result.append(current_line)
                        current_line = word
            
            # 添加最后一行
            if current_line:
                result.append(current_line)
        
        return '\n'.join(result)

    def abbreviate(self, text, max_length=50, suffix='...'):
        """
        按字符数截断文本
        
        参数:
            text (str): 要截断的文本
            max_length (int): 最大字符数
            suffix (str): 截断后添加的后缀
        
        返回:
            str: 截断后的文本
        """
        if not text or not isinstance(text, str):
            return text
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix

    def capitalize_words(self, text):
        """
        将文本中每个单词的首字母大写
        
        参数:
            text (str): 要处理的文本
        
        返回:
            str: 首字母大写后的文本
        """
        if not text or not isinstance(text, str):
            return text
        
        # 使用title()方法并修正缩写词等特殊情况
        result = []
        for word in text.split(' '):
            if word:
                # 保留全大写的单词（如缩写词）
                if word.isupper():
                    result.append(word)
                else:
                    result.append(word.capitalize())
            else:
                result.append('')
        
        return ' '.join(result)

    def replace_words(self, text, replacements):
        """
        替换文本中的特定单词或短语
        
        参数:
            text (str): 要处理的文本
            replacements (dict): 替换字典，键为要替换的单词，值为替换后的内容
        
        返回:
            str: 替换后的文本
        """
        if not text or not isinstance(text, str) or not replacements or not isinstance(replacements, dict):
            return text
        
        # 构建正则表达式，确保较长的模式先匹配
        pattern = '|'.join(sorted([re.escape(k) for k in replacements.keys()], key=len, reverse=True))
        
        # 定义替换函数
        def replace(match):
            return replacements[match.group(0)]
        
        # 执行替换
        return re.sub(pattern, replace, text)

    def contains_words(self, text, words, case_sensitive=False):
        """
        检查文本是否包含指定的单词列表中的任何一个单词
        
        参数:
            text (str): 要检查的文本
            words (str/list): 要查找的单词，可以是单个单词或单词列表
            case_sensitive (bool): 是否区分大小写
        
        返回:
            bool: 如果文本包含任何一个单词，返回True，否则返回False
        """
        if not text or not isinstance(text, str) or not words:
            return False
        
        if case_sensitive:
            text_lower = text
        else:
            text_lower = text.lower()
        
        if isinstance(words, str):
            words = [words]
        
        for word in words:
            if not word:
                continue
            
            if case_sensitive:
                word_to_check = word
            else:
                word_to_check = word.lower()
            
            # 使用单词边界确保完整匹配
            if re.search(r'\\b' + re.escape(word_to_check) + r'\\b', text_lower):
                return True
        
        return False

    def starts_with(self, text, prefix, case_sensitive=True):
        """
        检查文本是否以指定的前缀开头
        
        参数:
            text (str): 要检查的文本
            prefix (str): 要查找的前缀
            case_sensitive (bool): 是否区分大小写
        
        返回:
            bool: 如果文本以指定前缀开头，返回True，否则返回False
        """
        if not text or not isinstance(text, str) or not prefix or not isinstance(prefix, str):
            return False
        
        if case_sensitive:
            return text.startswith(prefix)
        else:
            return text.lower().startswith(prefix.lower())

    def ends_with(self, text, suffix, case_sensitive=True):
        """
        检查文本是否以指定的后缀结尾
        
        参数:
            text (str): 要检查的文本
            suffix (str): 要查找的后缀
            case_sensitive (bool): 是否区分大小写
        
        返回:
            bool: 如果文本以指定后缀结尾，返回True，否则返回False
        """
        if not text or not isinstance(text, str) or not suffix or not isinstance(suffix, str):
            return False
        
        if case_sensitive:
            return text.endswith(suffix)
        else:
            return text.lower().endswith(suffix.lower())

    def is_email(self, text):
        """
        检查文本是否是有效的电子邮件地址
        
        参数:
            text (str): 要检查的文本
        
        返回:
            bool: 如果文本是有效的电子邮件地址，返回True，否则返回False
        """
        if not text or not isinstance(text, str):
            return False
        
        # 简单的电子邮件正则表达式
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
        return re.match(email_regex, text) is not None

    def is_url(self, text):
        """
        检查文本是否是有效的URL
        
        参数:
            text (str): 要检查的文本
        
        返回:
            bool: 如果文本是有效的URL，返回True，否则返回False
        """
        if not text or not isinstance(text, str):
            return False
        
        # 简单的URL正则表达式
        url_regex = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(?:/[^\s]*)?$'
        return re.match(url_regex, text) is not None

    def count_words(self, text):
        """
        计算文本中的单词数量
        
        参数:
            text (str): 要计算的文本
        
        返回:
            int: 单词数量
        """
        if not text or not isinstance(text, str):
            return 0
        
        # 分割文本并计算非空单词数量
        words = [word for word in text.split() if word.strip()]
        return len(words)

    def generate_token(self, length=16, chars=None):
        """
        生成随机令牌
        
        参数:
            length (int): 令牌长度
            chars (str): 可用字符集，如果为None，使用大小写字母和数字
        
        返回:
            str: 随机生成的令牌
        """
        import random
        
        if chars is None:
            chars = string.ascii_letters + string.digits
        
        return ''.join(random.choice(chars) for _ in range(length))

    def format_number(self, number, decimals=2, thousand_separator=','):
        """
        格式化数字，添加千位分隔符
        
        参数:
            number (int/float/str): 要格式化的数字
            decimals (int): 小数位数
            thousand_separator (str): 千位分隔符
        
        返回:
            str: 格式化后的数字字符串
        """
        try:
            # 尝试将输入转换为浮点数
            num = float(number)
            
            # 格式化数字，添加千位分隔符和指定的小数位数
            formatted = f"{{:,}}" if thousand_separator == ',' else f"{{:}}"
            formatted = formatted.format(num)
            
            # 处理小数部分
            if '.' in formatted:
                integer_part, decimal_part = formatted.split('.')
                # 添加千位分隔符（如果不是逗号）
                if thousand_separator != ',':
                    integer_part = integer_part.replace(',', thousand_separator)
                # 截断或补零到指定的小数位数
                decimal_part = decimal_part[:decimals].ljust(decimals, '0') if decimals > 0 else ''
                return f"{integer_part}.{decimal_part}" if decimal_part else integer_part
            else:
                # 整数情况，添加千位分隔符
                if thousand_separator != ',':
                    formatted = formatted.replace(',', thousand_separator)
                # 添加小数部分（如果需要）
                return f"{formatted}.{'0' * decimals}" if decimals > 0 else formatted
        except (ValueError, TypeError):
            # 如果转换失败，返回原始输入
            return number

# 为方便单独使用，提供直接的函数访问
def get_text_processing_extension():
    """获取文本处理扩展的实例"""
    return TextProcessingExtension