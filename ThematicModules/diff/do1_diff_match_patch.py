# -*- coding:utf-8 -*-
# file:do1_diff_match_patch.py
# !/usr/bin/env python3
"""
diff_match_patch 完整使用示例
涵盖差异比较、文本匹配、补丁生成与应用等所有功能
"""

import sys
from typing import List, Tuple, Any
from datetime import datetime

try:
    from diff_match_patch import diff_match_patch
except ImportError:
    print("正在安装 diff_match_patch 库...")
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "diff-match-patch"])
    from diff_match_patch import diff_match_patch


class DiffMatchPatchDemo:
    """diff_match_patch 完整演示类"""

    def __init__(self):
        """初始化 dmp 实例"""
        self.dmp = diff_match_patch()
        print("=" * 60)
        print("diff_match_patch 完整示例")
        print("=" * 60)

    def demo_diff_basic(self) -> None:
        """演示基础差异比较功能"""
        print("\n1. 基础差异比较")
        print("-" * 40)

        # 示例文本
        text1 = "The quick brown fox jumps over the lazy dog."
        text2 = "The quick brown fox leaps over the sleepy dog."

        print(f"原文: {text1}")
        print(f"新文: {text2}")

        # 计算差异
        diffs = self.dmp.diff_main(text1, text2)
        print("\n原始差异结果:")
        self._print_diffs(diffs)

        # 清理优化
        self.dmp.diff_cleanupSemantic(diffs)
        print("\n语义清理后:")
        self._print_diffs(diffs)

        # 计算差异统计
        stats = self._get_diff_stats(diffs)
        print(f"\n差异统计: {stats}")

    def demo_diff_advanced(self) -> None:
        """演示高级差异功能"""
        print("\n2. 高级差异功能")
        print("-" * 40)

        text1 = """# 示例代码
def hello_world():
    print("Hello, World!")
    return True

def calculate_sum(a, b):
    result = a + b
    return result"""

        text2 = """# 示例代码
def hello_world():
    print("Hello, World!")
    return True

def calculate_sum(a, b):
    # 计算两个数的和
    result = a + b
    return result

def new_function():
    print("这是新函数")
    return None"""

        # 计算差异
        diffs = self.dmp.diff_main(text1, text2)

        # 不同的清理策略
        print("a) 语义清理 (diff_cleanupSemantic):")
        diffs_semantic = diffs[:]
        self.dmp.diff_cleanupSemantic(diffs_semantic)
        self._print_diffs(diffs_semantic, max_length=50)

        print("\nb) 效率优化 (diff_cleanupEfficiency):")
        diffs_efficiency = diffs[:]
        self.dmp.diff_cleanupEfficiency(diffs_efficiency)
        self._print_diffs(diffs_efficiency, max_length=50)

        print("\nc) 合并相邻操作 (diff_cleanupMerge):")
        diffs_merge = diffs[:]
        self.dmp.diff_cleanupMerge(diffs_merge)
        self._print_diffs(diffs_merge, max_length=50)

        # 计算编辑距离
        print("\nd) 计算编辑距离 (Levenshtein距离):")
        levenshtein_dist = self.dmp.diff_levenshtein(diffs)
        print(f"编辑距离: {levenshtein_dist}")

        # 生成HTML格式的差异
        print("\ne) HTML格式差异:")
        html_diff = self.dmp.diff_prettyHtml(diffs)
        # 简化显示
        html_preview = html_diff[:200] + "..." if len(html_diff) > 200 else html_diff
        print(html_preview)

    def demo_match(self) -> None:
        """演示文本匹配功能"""
        print("\n3. 文本匹配功能")
        print("-" * 40)

        text = """Python是一种广泛使用的高级编程语言，
由Guido van Rossum创建，于1991年首次发布。
Python的设计哲学强调代码的可读性和简洁的语法。
它支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。"""

        patterns = ["Python", "编程语言", "Guido", "不存在的文本"]

        for pattern in patterns:
            print(f"\n搜索模式: '{pattern}'")

            # 基本匹配
            location = self.dmp.match_main(text, pattern, 0)
            print(f"  基本匹配位置: {location}")

            # 位掩码匹配
            location_bitap = self.dmp.match_bitap(text, pattern, 0)
            print(f"  Bitap匹配位置: {location_bitap}")

            # 阈值匹配
            location_threshold = self.dmp.match_main(text, pattern, 0, 0.7)
            print(f"  阈值匹配位置: {location_threshold}")

            if location != -1:
                # 显示上下文
                start = max(0, location - 20)
                end = min(len(text), location + len(pattern) + 20)
                context = text[start:end].replace('\n', ' ')
                print(f"  上下文: ...{context}...")

    def demo_patch(self) -> None:
        """演示补丁功能"""
        print("\n4. 补丁生成与应用")
        print("-" * 40)

        # 原始文本
        original = """用户管理系统
============

功能列表:
1. 用户注册
2. 用户登录
3. 查看个人信息"""

        # 修改后的文本
        modified = """用户管理系统
============

功能列表:
1. 用户注册
2. 用户登录
3. 查看个人信息
4. 修改密码
5. 注销账户"""

        print("原始文本:")
        print(original)
        print("\n修改后文本:")
        print(modified)

        # 生成补丁
        patches = self.dmp.patch_make(original, modified)

        print("\na) 补丁内容:")
        for i, patch in enumerate(patches):
            print(f"\n补丁 #{i + 1}:")
            print(f"  开始位置: {patch.start1}")
            print(f"  长度: {patch.length1}")
            print(f"  差异: {patch.diffs}")

        # 补丁文本表示
        patch_text = self.dmp.patch_toText(patches)
        print("\nb) 补丁文本表示:")
        print(patch_text)

        # 从文本解析补丁
        parsed_patches = self.dmp.patch_fromText(patch_text)
        print(f"\nc) 解析补丁数量: {len(parsed_patches)}")

        # 应用补丁
        print("\nd) 应用补丁:")
        result_text, results = self.dmp.patch_apply(patches, original)
        print(f"  应用结果: {result_text}")
        print(f"  每个补丁应用状态: {results}")

        # 验证应用结果
        if result_text == modified:
            print("  ✓ 补丁应用成功!")
        else:
            print("  ✗ 补丁应用失败!")

        # 分割补丁示例
        print("\ne) 补丁分割:")
        long_text = "A" * 100 + "B" * 100
        patches_long = self.dmp.patch_make("", long_text)

        # 尝试分割大补丁
        patches_split = []
        for patch in patches_long:
            patches_split.extend(self.dmp.patch_splitMax(patch))

        print(f"  原始补丁数: {len(patches_long)}")
        print(f"  分割后补丁数: {len(patches_split)}")

    def demo_advanced_patch(self) -> None:
        """演示高级补丁功能"""
        print("\n5. 高级补丁功能")
        print("-" * 40)

        # 创建基础文档
        base_doc = """项目计划
========

第一周: 需求分析
第二周: 系统设计
第三周: 开发实现"""

        # 两个用户的修改
        user1_doc = """项目计划
========

第一周: 需求分析
第二周: 系统设计
第三周: 开发实现
第四周: 测试验证"""

        user2_doc = """项目计划
========

第一周: 需求收集与分析
第二周: 系统架构设计
第三周: 开发实现"""

        print("模拟协作编辑场景:")
        print(f"基础文档: \n{base_doc}")

        # 生成两个补丁
        patch1 = self.dmp.patch_make(base_doc, user1_doc)
        patch2 = self.dmp.patch_make(base_doc, user2_doc)

        # 尝试合并补丁
        print("\na) 尝试合并补丁:")

        # 先应用patch1到base
        merged, results1 = self.dmp.patch_apply(patch1, base_doc)
        print(f"  应用补丁1后: {merged}")

        # 再尝试应用patch2到合并结果
        final, results2 = self.dmp.patch_apply(patch2, merged)
        print(f"  应用补丁2后: {final}")

        print(f"  补丁1应用状态: {results1}")
        print(f"  补丁2应用状态: {results2}")

        # 检查冲突
        conflicts = [i for i, success in enumerate(results2) if not success]
        if conflicts:
            print(f"  发现冲突的补丁: {conflicts}")

        # 补丁优化
        print("\nb) 补丁优化:")
        patches = self.dmp.patch_make("Hello World", "Hello Beautiful World")

        # 添加冗余上下文
        for patch in patches:
            patch.length1 += 5
            patch.length2 += 5

        print(f"  优化前补丁: {patches}")
        self.dmp.patch_addContext(patches, "Hello World")
        print(f"  添加上下文后: {patches}")

    def demo_custom_settings(self) -> None:
        """演示自定义设置"""
        print("\n6. 自定义设置")
        print("-" * 40)

        # 创建新实例并调整设置
        custom_dmp = diff_match_patch()

        # 调整参数
        custom_dmp.Diff_Timeout = 0.5  # 设置超时时间（秒）
        custom_dmp.Diff_EditCost = 4  # 编辑成本

        custom_dmp.Match_Threshold = 0.6  # 匹配阈值
        custom_dmp.Match_Distance = 500  # 搜索距离

        custom_dmp.Patch_DeleteThreshold = 0.6  # 删除阈值
        custom_dmp.Patch_Margin = 8  # 补丁边距

        print("自定义参数设置:")
        print(f"  Diff_Timeout: {custom_dmp.Diff_Timeout}")
        print(f"  Diff_EditCost: {custom_dmp.Diff_EditCost}")
        print(f"  Match_Threshold: {custom_dmp.Match_Threshold}")
        print(f"  Match_Distance: {custom_dmp.Match_Distance}")
        print(f"  Patch_DeleteThreshold: {custom_dmp.Patch_DeleteThreshold}")
        print(f"  Patch_Margin: {custom_dmp.Patch_Margin}")

        # 测试自定义设置的效果
        text1 = "A" * 1000 + "B" * 1000
        text2 = "A" * 1000 + "C" * 1000

        print("\n使用自定义设置计算差异...")
        diffs = custom_dmp.diff_main(text1, text2)
        stats = self._get_diff_stats(diffs)
        print(f"差异统计: {stats}")

    def demo_performance(self) -> None:
        """演示性能相关功能"""
        print("\n7. 性能优化示例")
        print("-" * 40)

        # 大文本处理
        print("处理大文本的优化策略:")

        # 生成大文本
        large_text1 = "这是大文本。" * 1000
        large_text2 = large_text1.replace("大文本", "长篇文本") + " 新增内容。" * 50

        print(f"文本1长度: {len(large_text1)} 字符")
        print(f"文本2长度: {len(large_text2)} 字符")

        # 分块处理策略
        print("\na) 分块处理:")
        chunks1 = self._split_text(large_text1, 5000)
        chunks2 = self._split_text(large_text2, 5000)

        print(f"  分块数量: {len(chunks1)}")
        print(f"  每块大小: 约5000字符")

        # 设置超时
        print("\nb) 设置超时:")
        self.dmp.Diff_Timeout = 0.1  # 100毫秒超时

        start_time = datetime.now()
        try:
            diffs = self.dmp.diff_main(large_text1, large_text2)
            elapsed = (datetime.now() - start_time).total_seconds()
            print(f"  计算完成，耗时: {elapsed:.3f}秒")
            print(f"  差异数量: {len(diffs)}")
        except Exception as e:
            print(f"  计算超时或出错: {e}")

        # 重置超时
        self.dmp.Diff_Timeout = 1.0

    def demo_integration(self) -> None:
        """演示集成示例"""
        print("\n8. 实际应用集成示例")
        print("-" * 40)

        print("a) 简单的版本控制系统:")

        class SimpleVersionControl:
            def __init__(self):
                self.dmp = diff_match_patch()
                self.versions = []
                self.patches = []

            def commit(self, new_content: str) -> None:
                """提交新版本"""
                if not self.versions:
                    # 第一个版本
                    self.versions.append({
                        'id': 0,
                        'content': new_content,
                        'timestamp': datetime.now().isoformat()
                    })
                    print(f"  创建初始版本 0")
                    return

                # 与上一个版本比较
                last_content = self.versions[-1]['content']
                if new_content == last_content:
                    print("  内容未变化，跳过提交")
                    return

                # 生成补丁
                patch = self.dmp.patch_make(last_content, new_content)
                patch_text = self.dmp.patch_toText(patch)

                # 保存新版本
                version_id = len(self.versions)
                self.versions.append({
                    'id': version_id,
                    'content': new_content,
                    'timestamp': datetime.now().isoformat(),
                    'patch': patch_text
                })
                self.patches.append(patch_text)

                print(f"  提交版本 {version_id}")
                print(f"  补丁大小: {len(patch_text)} 字符")

            def revert(self, version_id: int) -> str:
                """恢复到指定版本"""
                if version_id >= len(self.versions):
                    raise ValueError("版本不存在")

                content = self.versions[version_id]['content']
                print(f"  恢复到版本 {version_id}")
                return content

            def get_diff(self, version1: int, version2: int) -> List[Tuple[int, str]]:
                """获取两个版本之间的差异"""
                if version1 >= len(self.versions) or version2 >= len(self.versions):
                    raise ValueError("版本不存在")

                text1 = self.versions[version1]['content']
                text2 = self.versions[version2]['content']

                diffs = self.dmp.diff_main(text1, text2)
                self.dmp.diff_cleanupSemantic(diffs)

                print(f"  版本 {version1} 和 {version2} 之间的差异:")
                return diffs

        # 使用版本控制系统
        vcs = SimpleVersionControl()

        # 提交几个版本
        vcs.commit("第一版内容")
        vcs.commit("第二版修改后的内容")
        vcs.commit("第三版再次修改的内容")

        # 获取差异
        diffs = vcs.get_diff(0, 2)
        self._print_diffs(diffs, max_length=30)

        print("\nb) 实时协作编辑演示:")

        class CollaborativeEditor:
            def __init__(self, initial_text: str):
                self.dmp = diff_match_patch()
                self.text = initial_text
                self.operations = []

            def apply_operation(self, operation: str, cursor_pos: int) -> str:
                """应用操作并返回补丁"""
                old_text = self.text

                if operation.startswith("INSERT:"):
                    # 插入文本
                    insert_text = operation[7:]
                    self.text = self.text[:cursor_pos] + insert_text + self.text[cursor_pos:]
                elif operation.startswith("DELETE:"):
                    # 删除文本
                    delete_len = int(operation[7:])
                    self.text = self.text[:cursor_pos] + self.text[cursor_pos + delete_len:]

                # 生成补丁
                patch = self.dmp.patch_make(old_text, self.text)
                patch_text = self.dmp.patch_toText(patch)

                return patch_text

            def apply_patch(self, patch_text: str) -> bool:
                """应用补丁"""
                patches = self.dmp.patch_fromText(patch_text)
                new_text, results = self.dmp.patch_apply(patches, self.text)

                if all(results):
                    self.text = new_text
                    return True
                return False

        editor = CollaborativeEditor("初始文本")
        patch = editor.apply_operation("INSERT:新内容", 4)
        print(f"  生成补丁: {patch[:50]}...")
        print(f"  当前文本: {editor.text}")

    def _print_diffs(self, diffs: List[Tuple[int, str]], max_length: int = 100) -> None:
        """打印差异结果"""
        for op, text in diffs:
            # 截断长文本
            if len(text) > max_length:
                text = text[:max_length] + "..."

            if op == self.dmp.DIFF_INSERT:
                print(f"  [+] {repr(text)}")
            elif op == self.dmp.DIFF_DELETE:
                print(f"  [-] {repr(text)}")
            else:
                print(f"  [=] {repr(text)}")

    def _get_diff_stats(self, diffs: List[Tuple[int, str]]) -> dict:
        """获取差异统计信息"""
        stats = {
            'insert': 0,
            'delete': 0,
            'equal': 0,
            'insert_chars': 0,
            'delete_chars': 0,
            'equal_chars': 0
        }

        for op, text in diffs:
            if op == self.dmp.DIFF_INSERT:
                stats['insert'] += 1
                stats['insert_chars'] += len(text)
            elif op == self.dmp.DIFF_DELETE:
                stats['delete'] += 1
                stats['delete_chars'] += len(text)
            else:
                stats['equal'] += 1
                stats['equal_chars'] += len(text)

        return stats

    def _split_text(self, text: str, chunk_size: int) -> List[str]:
        """分割文本为块"""
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def run_all_demos(self) -> None:
        """运行所有演示"""
        demos = [
            self.demo_diff_basic,
            self.demo_diff_advanced,
            self.demo_match,
            self.demo_patch,
            self.demo_advanced_patch,
            self.demo_custom_settings,
            self.demo_performance,
            self.demo_integration
        ]

        for demo in demos:
            try:
                demo()
                print("\n" + "=" * 60 + "\n")
            except Exception as e:
                print(f"演示出错: {e}")
                import traceback
                traceback.print_exc()
                print("\n" + "=" * 60 + "\n")


def main():
    """主函数"""
    # 创建演示实例
    demo = DiffMatchPatchDemo()

    # 运行所有演示
    demo.run_all_demos()

    print("diff_match_patch 示例运行完成！")
    print("关键点总结:")
    print("1. diff_main() - 计算文本差异")
    print("2. diff_cleanup*() - 清理优化差异")
    print("3. match_main() - 文本匹配")
    print("4. patch_make() - 生成补丁")
    print("5. patch_apply() - 应用补丁")
    print("6. 调整参数优化性能")


if __name__ == "__main__":
    main()