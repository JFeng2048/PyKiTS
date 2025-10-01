#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jinja2 性能优化演示

本示例展示了如何在Jinja2中实现各种性能优化技术，包括：
1. 模板缓存优化
2. 预编译模板
3. 上下文数据预处理
4. 加载器优化
5. 性能监控和分析
6. 生产环境配置

使用方法：
    python performance_optimization_demo.py
"""

import os
import time
import cProfile
import pstats
import io
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader, DictLoader, ChoiceLoader, select_autoescape

# 模拟数据生成器
def generate_mock_data():
    """
    生成用于测试的模拟数据
    
    返回:
        包含测试数据的字典
    """
    # 模拟用户数据
    users = []
    for i in range(100):
        users.append({
            'id': i + 1,
            'name': f'User {i + 1}',
            'email': f'user{i+1}@example.com',
            'roles': [
                {'id': 1, 'name': 'Reader'},
                {'id': 2, 'name': 'Editor'} if i % 3 == 0 else {'id': 1, 'name': 'Reader'}
            ],
            'logins': [{'timestamp': datetime.now() - timedelta(days=j)} for j in range(i % 10 + 1)],
            'last_login': datetime.now() - timedelta(days=i % 30)
        })
    
    # 模拟文章数据
    articles = []
    for i in range(50):
        articles.append({
            'id': i + 1,
            'title': f'Article {i + 1}: Performance Optimization Techniques',
            'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
            'views': 1000 + i * 100,
            'url': f'/articles/{i + 1}'
        })
    
    # 模拟商品数据
    items = []
    for i in range(200):
        items.append({
            'id': i + 1,
            'name': f'Product {i + 1}',
            'price': 10.0 + i * 2.5,
            'quantity': i % 10 + 1,
            'discount': 0.1 if i % 5 == 0 else 0,
            'stock': 100 - i if i < 100 else 0,
            'category': f'Category {i % 5 + 1}'
        })
    
    # 模拟分类数据
    categories = []
    for i in range(5):
        categories.append({
            'id': i + 1,
            'name': f'Category {i + 1}',
            'count': 20 + i * 5,
            'url': f'/categories/{i + 1}'
        })
    
    return {
        'users': users,
        'articles': articles,
        'items': items,
        'categories': categories
    }

# 数据预处理函数
def preprocess_data(raw_data):
    """
    预处理模板数据，提高渲染性能
    
    参数:
        raw_data: 原始数据
        
    返回:
        预处理后的数据
    """
    # 预处理用户数据
    processed_users = []
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    for user in raw_data['users']:
        # 预计算所有需要在模板中展示的值
        processed_users.append({
            'id': user['id'],
            'display_name': user['name'].title(),
            'email': user['email'],
            'role_names': ', '.join([role['name'] for role in user['roles']]),
            'login_count': len(user['logins']),
            'last_login_display': user['last_login'].strftime('%Y-%m-%d %H:%M'),
            'is_recently_active': user['last_login'] > thirty_days_ago
        })
    
    # 预处理商品数据
    processed_items = []
    featured_categories = ['Category 1', 'Category 3']
    
    for item in raw_data['items']:
        # 预计算价格、折扣等
        total_price = item['price'] * item['quantity']
        discount_percent = f'{item['discount'] * 100}%' if item['discount'] > 0 else '0%'
        
        processed_items.append({
            'id': item['id'],
            'display_name': item['name'].title(),
            'total_price': f'${total_price:.2f}',
            'discount_percent': discount_percent,
            'stock_status': '有货' if item['stock'] > 0 else '缺货',
            'is_featured': item['category'] in featured_categories
        })
    
    # 返回预处理后的数据
    return {
        'processed_users': processed_users,
        'processed_items': processed_items,
        'popular_articles': raw_data['articles'][:10],
        'categories': raw_data['categories'],
        # 添加其他可能需要的数据
        'now': datetime.now(),
        'cache_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'render_time_ms': 0,  # 将在渲染时设置
        'template_count': 15,  # 模拟值
        'cache_hit_rate': 95,  # 模拟值
        # 性能监控数据
        'perf_header_time': 5,
        'perf_content_time': 15,
        'perf_sidebar_time': 8,
        'perf_footer_time': 3,
        'perf_total_time': 31
    }

# 基础环境配置
def create_basic_environment(template_dir):
    """
    创建基础的Jinja2环境（无特殊优化）
    
    参数:
        template_dir: 模板目录路径
        
    返回:
        Jinja2环境实例
    """
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env

# 优化的环境配置
def create_optimized_environment(template_dir, preload_templates=True):
    """
    创建优化的Jinja2环境
    
    参数:
        template_dir: 模板目录路径
        preload_templates: 是否预加载模板
        
    返回:
        优化配置的Jinja2环境实例
    """
    # 创建模板加载器
    loader = create_optimized_loader(template_dir)
    
    # 创建环境
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(['html', 'xml']),
        # 空白控制优化
        trim_blocks=True,
        lstrip_blocks=True,
        # 缓存优化
        cache_size=1000,  # 增加缓存大小
        auto_reload=False,  # 生产环境关闭自动重载
        # 其他优化
        optimized=True  # 启用优化模式
    )
    
    # 添加常用的全局函数
    env.globals['get_current_time'] = lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    env.globals['environment_type'] = 'production'
    
    # 预加载模板
    if preload_templates:
        preload_templates_list(env, template_dir)
    
    return env

# 创建优化的加载器
def create_optimized_loader(template_dir):
    """
    创建优化的模板加载器
    
    参数:
        template_dir: 模板目录路径
        
    返回:
        优化配置的模板加载器
    """
    # 预加载常用模板到内存
    common_templates = {}
    
    # 预加载性能示例模板
    try:
        with open(os.path.join(template_dir, 'performance_example.html'), 'r', encoding='utf-8') as f:
            common_templates['performance_example.html'] = f.read()
    except Exception as e:
        print(f"无法预加载模板: {e}")
    
    # 创建组合加载器
    return ChoiceLoader([
        DictLoader(common_templates),  # 内存加载器（优先）
        FileSystemLoader(template_dir)  # 文件系统加载器
    ])

# 预加载模板
def preload_templates_list(env, template_dir):
    """
    预加载模板列表
    
    参数:
        env: Jinja2环境实例
        template_dir: 模板目录路径
    """
    # 获取所有模板文件
    template_files = []
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith(('.html', '.htm', '.txt')):
                # 计算相对路径
                rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                # 转换为Unix风格的路径
                template_name = rel_path.replace(os.path.sep, '/')
                template_files.append(template_name)
    
    # 预加载模板
    for template_name in template_files:
        try:
            env.get_template(template_name)
        except Exception as e:
            print(f"预加载模板失败 {template_name}: {e}")

# 测量渲染性能
def measure_rendering_performance(env, template_name, context):
    """
    测量模板渲染性能
    
    参数:
        env: Jinja2环境实例
        template_name: 模板名称
        context: 渲染上下文
        
    返回:
        (渲染结果, 渲染时间(秒))
    """
    # 确保模板已加载（如果使用缓存）
    template = env.get_template(template_name)
    
    # 测量渲染时间
    start_time = time.time()
    result = template.render(**context)
    end_time = time.time()
    
    return result, end_time - start_time

# 性能分析器
def profile_template_rendering(env, template_name, context):
    """
    使用cProfile分析模板渲染性能
    
    参数:
        env: Jinja2环境实例
        template_name: 模板名称
        context: 渲染上下文
        
    返回:
        渲染结果
    """
    # 获取模板
    template = env.get_template(template_name)
    
    # 创建分析器
    pr = cProfile.Profile()
    pr.enable()
    
    # 执行渲染
    result = template.render(**context)
    
    # 停止分析
    pr.disable()
    
    # 打印分析结果
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(20)  # 显示前20个函数
    print(s.getvalue())
    
    return result

# 缓存命中率跟踪器
class CacheHitTracker:
    """
    简单的缓存命中率跟踪器
    """
    def __init__(self):
        self.hits = 0
        self.misses = 0
        
    def hit(self):
        """记录缓存命中"""
        self.hits += 1
        
    def miss(self):
        """记录缓存未命中"""
        self.misses += 1
        
    def get_hit_rate(self):
        """\计算缓存命中率"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0

# 自定义缓存类示例
class CustomTemplateCache:
    """
    自定义模板缓存实现示例
    """
    def __init__(self, tracker=None):
        self.cache = {}
        self.tracker = tracker or CacheHitTracker()
        self.max_size = 500  # 缓存大小限制
        
    def get(self, key):
        """从缓存获取模板"""
        if key in self.cache:
            self.tracker.hit()
            return self.cache[key]
        self.tracker.miss()
        return None
        
    def set(self, key, value, timeout=None):
        """将模板存入缓存"""
        # 简单的LRU缓存策略实现
        if len(self.cache) >= self.max_size:
            # 删除第一个元素（最简单的策略）
            first_key = next(iter(self.cache))
            del self.cache[first_key]
        
        self.cache[key] = value

# 性能比较测试
def compare_performance(basic_env, optimized_env, template_name, context):
    """
    比较基础环境和优化环境的性能差异
    
    参数:
        basic_env: 基础环境
        optimized_env: 优化环境
        template_name: 模板名称
        context: 渲染上下文
    """
    print("=" * 80)
    print(f"性能比较测试: {template_name}")
    print("=" * 80)
    
    # 预热缓存
    print("预热缓存...")
    for _ in range(3):
        basic_env.get_template(template_name).render(**context)
        optimized_env.get_template(template_name).render(**context)
    
    # 测试基础环境
    print("\n测试基础环境性能...")
    basic_results = []
    for i in range(10):
        result, render_time = measure_rendering_performance(basic_env, template_name, context)
        basic_results.append(render_time)
        print(f"  渲染 {i+1}: {render_time:.4f}秒")
    
    # 测试优化环境
    print("\n测试优化环境性能...")
    optimized_results = []
    for i in range(10):
        result, render_time = measure_rendering_performance(optimized_env, template_name, context)
        optimized_results.append(render_time)
        print(f"  渲染 {i+1}: {render_time:.4f}秒")
    
    # 计算平均时间
    avg_basic = sum(basic_results) / len(basic_results)
    avg_optimized = sum(optimized_results) / len(optimized_results)
    improvement = ((avg_basic - avg_optimized) / avg_basic) * 100
    
    # 输出比较结果
    print("=" * 80)
    print(f"性能比较结果:")
    print(f"  基础环境平均渲染时间: {avg_basic:.4f}秒")
    print(f"  优化环境平均渲染时间: {avg_optimized:.4f}秒")
    print(f"  性能提升: {improvement:.2f}%")
    print("=" * 80)

# 预编译模板示例
def precompile_templates_demo(template_dir, output_dir):
    """
    预编译模板演示
    
    参数:
        template_dir: 模板目录
        output_dir: 输出目录
    """
    print("\n预编译模板演示...")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建环境
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # 查找所有模板
    template_files = []
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith(('.html', '.htm', '.txt')):
                rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                template_name = rel_path.replace(os.path.sep, '/')
                template_files.append(template_name)
    
    # 预编译模板
    for template_name in template_files:
        try:
            print(f"预编译: {template_name}")
            # 加载模板（触发编译）
            template = env.get_template(template_name)
            
            # 在这里可以将编译后的模板保存到文件或其他存储
            # 为了简化，我们只记录编译完成
            
        except Exception as e:
            print(f"预编译失败 {template_name}: {e}")
    
    print(f"预编译完成，共处理 {len(template_files)} 个模板")

# 模板内存使用分析
def analyze_memory_usage(env, template_name, context):
    """
    分析模板渲染的内存使用情况
    
    参数:
        env: Jinja2环境实例
        template_name: 模板名称
        context: 渲染上下文
    """
    print("\n分析内存使用情况...")
    
    try:
        # 尝试导入memory_profiler库
        from memory_profiler import memory_usage
        
        # 定义要测量的函数
        def render_template():
            template = env.get_template(template_name)
            return template.render(**context)
        
        # 测量内存使用
        mem_usage = memory_usage(render_template, interval=0.1, timeout=None)
        
        print(f"最大内存使用: {max(mem_usage):.2f} MB")
        print(f"平均内存使用: {sum(mem_usage) / len(mem_usage):.2f} MB")
        
    except ImportError:
        print("注意: memory_profiler 库未安装，无法分析内存使用情况。")
        print("可以通过 'pip install memory_profiler' 安装此库。")

# 主函数
def main():
    """
    主函数，运行所有性能优化演示
    """
    print("Jinja2 性能优化演示")
    print("=" * 80)
    print("本程序展示了Jinja2模板引擎中的各种性能优化技术和最佳实践")
    print("=" * 80)
    
    # 获取当前目录和模板目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(os.path.dirname(current_dir), 'templates')
    output_dir = os.path.join(current_dir, 'compiled_templates')
    
    # 生成模拟数据
    print("生成模拟数据...")
    raw_data = generate_mock_data()
    
    # 预处理数据
    print("预处理数据...")
    context = preprocess_data(raw_data)
    
    # 创建基础环境
    print("创建基础Jinja2环境...")
    basic_env = create_basic_environment(template_dir)
    
    # 创建优化环境
    print("创建优化的Jinja2环境...")
    optimized_env = create_optimized_environment(template_dir)
    
    # 测试模板名称
    template_name = 'performance_example.html'
    
    try:
        # 1. 性能比较测试
        compare_performance(basic_env, optimized_env, template_name, context)
        
        # 2. 预编译模板演示
        precompile_templates_demo(template_dir, output_dir)
        
        # 3. 性能分析
        print("\n\n执行详细性能分析...")
        profile_template_rendering(optimized_env, template_name, context)
        
        # 4. 内存使用分析
        analyze_memory_usage(optimized_env, template_name, context)
        
        # 5. 缓存策略演示
        print("\n\n缓存策略演示...")
        tracker = CacheHitTracker()
        custom_cache = CustomTemplateCache(tracker)
        
        # 创建使用自定义缓存的环境
        cache_env = Environment(
            loader=FileSystemLoader(template_dir),
            cache=custom_cache
        )
        
        # 测试缓存命中率
        print("测试缓存命中率...")
        for i in range(20):
            cache_env.get_template(template_name)
        
        print(f"缓存命中率: {tracker.get_hit_rate():.2f}%")
        print(f"缓存命中次数: {tracker.hits}")
        print(f"缓存未命中次数: {tracker.misses}")
        
        print("\n所有性能优化演示完成！")
        print("=" * 80)
        print("建议在实际应用中根据具体情况选择合适的优化策略。")
        print("始终记住：先测量，再优化！")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()