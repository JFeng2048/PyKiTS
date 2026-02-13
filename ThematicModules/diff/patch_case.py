import diff_match_patch as dmp_module

# 你的原始文本和LLM返回的新文本
original_code = """import time

def process_data(data):
    \"\"\"一个重要的函数。\"\"\"
    print("正在处理数据...")
    time.sleep(2)
    return len(data)

def helper_function():
    \"\"\"一个我们不想修改的辅助函数。\"\"\"
    pass
"""

modified_code = """import time
import redis

cache = redis.Redis()

def process_data(data):
    \"\"\"一个重要的函数。\"\"\"
    if cache.exists(data):
        return cache.get(data)
    result = len(data)
    cache.set(data, result, ex=60)
    return result

def helper_function():
    \"\"\"一个我们不想修改的辅助函数。\"\"\"
    pass
"""

# 1. 创建一个 dmp 对象
dmp = dmp_module.diff_match_patch()

# 2. 在本地生成补丁 (patch) 对象
# 注意：这次我们是比较两个完整的文本，而不是让LLM返回diff
patches = dmp.patch_make(original_code, modified_code)

# 3. 将补丁应用到原始文本上
# patch_apply 返回一个元组：(应用后的新文本, 一个布尔值列表表示每个补丁是否成功)
new_text, results = dmp.patch_apply(patches, original_code)


print("\n--- 应用Patch后的完整文件内容 ---")
print(new_text)
print(results)

print("\n--- 应用结果 ---")
# results 会像 [True, True, ...]
print(results)
