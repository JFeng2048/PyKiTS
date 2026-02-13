import difflib

# 这是你发给LLM的、从文件中精确定位到的旧函数代码
original_code = """def process_data(data):
    \"\"\"一个重要的函数。\"\"\"
    print("正在处理数据...")
    time.sleep(2)
    return len(data)
"""

# 这是LLM返回的、修改后的新函数代码
modified_code = """def process_data(data):
    \"\"\"一个重要的函数。\"\"\"
    if cache.exists(data):
        return cache.get(data)
    result = len(data)
    cache.set(data, result, ex=60)
    return result
"""

# difflib.unified_diff 需要的是行列表
original_lines = original_code.splitlines(keepends=True)
modified_lines = modified_code.splitlines(keepends=True)

# 生成diff
# fromfile 和 tofile 参数会出现在diff的头部
diff_generator = difflib.unified_diff(
    original_lines,
    modified_lines,
    fromfile='original_code', # 任意名称
    tofile='modified_code'    # 任意名称
)

# 将生成器转换成一个字符串，这就是标准的patch内容
patch_str = "".join(diff_generator)

print("--- 生成的Patch内容 ---")
print(patch_str)
