# -*- coding:utf-8 -*-
# file:do_asciimatics.py
"""
pip install asciimatics

# 查看所有命令
python do_asciimatics.py --help

# 列出所有可用特效
python do_asciimatics.py list

# 运行所有特效
python do_asciimatics.py show-all

# 运行所有特效，自定义持续时间
python do_asciimatics.py show-all --duration 5

# 运行所有特效，跳过UI交互
python do_asciimatics.py show-all --skip-ui

# 运行单个特效
python do_asciimatics.py run scroll
python do_asciimatics.py run banner "Hello World"
python do_asciimatics.py run rainbow

# 也可以使用原始命令名称（保持兼容）
python do_asciimatics.py scroll-text
python do_asciimatics.py starfield

cycle-colors     颜色循环效果
figlet-banner    Figlet艺术字横幅效果
list             列出所有可用的特效
particle-effect  简单的粒子效果演示
rainbow-text     彩虹文字效果
run              运行指定的单个特效
scroll-text      文本滚动特效
show-all         依次运行所有特效
simple-ui        演示一个简单的交互式UI表单
starfield        星空效果

"""

# !/usr/bin/env python3
"""
Asciimatics 特效演示管理器
使用 Click 框架统一管理各种 Asciimatics 特效演示


"""

import click
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Print, Cycle, Stars
from asciimatics.renderers import FigletText, Box, Rainbow
from asciimatics.widgets import Frame, Layout, Label, Button, Text
from asciimatics.exceptions import ResizeScreenError, StopApplication
import time
import sys
import inspect


class AsciimaticsManager:
    """Asciimatics 特效管理器类"""

    def __init__(self):
        self.effects = {}
        self.default_duration = 3

    def register_effect(self, name=None, description=None):
        """装饰器：注册特效函数"""

        def decorator(func):
            effect_name = name or func.__name__
            effect_desc = description or func.__doc__ or "无描述"

            self.effects[effect_name] = {
                'function': func,
                'description': effect_desc.strip()
            }
            return func

        return decorator

    def get_effect(self, name):
        """获取特效函数"""
        return self.effects.get(name)

    def list_effects(self):
        """列出所有特效"""
        return self.effects.items()


# 创建管理器实例
manager = AsciimaticsManager()


@click.group()
def cli():
    """Asciimatics 特效演示管理器

    使用各种炫酷的终端文本特效和动画
    """
    pass


@cli.command()
@click.argument('text', default='Hello Asciimatics!')
@manager.register_effect(name='scroll', description='文本滚动特效')
def scroll_text(text):
    """文本滚动特效"""

    def demo(screen):
        for i in range(screen.width - len(text)):
            screen.clear()
            screen.print_at(text, i, screen.height // 2, colour=Screen.COLOUR_GREEN)
            screen.refresh()
            time.sleep(0.1)

    Screen.wrapper(demo)


@cli.command()
@click.argument('text', default='ASCII')
@manager.register_effect(name='banner', description='Figlet艺术字横幅效果')
def figlet_banner(text):
    """Figlet艺术字横幅效果"""

    def demo(screen):
        renderer = FigletText(text, "big")
        effect = Print(screen, renderer, x=0, y=screen.height // 2 - 3, speed=1)
        scene = Scene([effect], 100)
        screen.play([scene])

    Screen.wrapper(demo)


@cli.command()
@manager.register_effect(name='ui', description='交互式UI表单演示')
def simple_ui():
    """演示一个简单的交互式UI表单"""

    class DemoFrame(Frame):
        def __init__(self, screen):
            super(DemoFrame, self).__init__(screen,
                                            screen.height,
                                            screen.width,
                                            has_border=True,
                                            title="Asciimatics Demo")
            layout = Layout([1], fill_frame=True)
            self.add_layout(layout)
            layout.add_widget(Label("欢迎使用 Asciimatics!", height=2))
            layout.add_widget(Text("姓名", "name"))
            layout.add_widget(Button("提交", self._submit))
            self.fix()

        def _submit(self):
            name = self.find_widget("name").value
            self.screen.clear()
            self.screen.print_at(f"你好, {name}!", 0, 0, colour=Screen.COLOUR_CYAN)
            self.screen.refresh()
            time.sleep(2)
            raise StopApplication("提交完成")

    Screen.wrapper(lambda screen: DemoFrame(screen))


@cli.command()
@manager.register_effect(name='particles', description='粒子效果演示')
def particle_effect():
    """简单的粒子效果演示"""

    def demo(screen):
        particles = []
        for i in range(20):
            particles.append({
                'x': screen.width // 2,
                'y': screen.height // 2,
                'vx': (i % 5) - 2,
                'vy': (i // 5) - 2
            })

        for _ in range(50):
            screen.clear()
            for p in particles:
                screen.print_at('*', int(p['x']), int(p['y']), colour=Screen.COLOUR_YELLOW)
                p['x'] += p['vx']
                p['y'] += p['vy']
            screen.refresh()
            time.sleep(0.1)

    Screen.wrapper(demo)


@cli.command()
@click.argument('text', default='Rainbow')
@manager.register_effect(name='rainbow', description='彩虹文字效果')
def rainbow_text(text):
    """彩虹文字效果"""

    def demo(screen):
        renderer = Rainbow(screen, FigletText(text, "small"))
        effect = Print(screen, renderer, x=0, y=screen.height // 2 - 3, speed=1)
        scene = Scene([effect], 100)
        screen.play([scene])

    Screen.wrapper(demo)


@cli.command()
@manager.register_effect(name='stars', description='星空效果')
def starfield():
    """星空效果"""

    def demo(screen):
        effects = [Stars(screen, screen.width)]
        scene = Scene(effects, 200)
        screen.play([scene])

    Screen.wrapper(demo)


@cli.command()
@click.argument('text', default='Colors')
@manager.register_effect(name='cycle', description='颜色循环效果')
def cycle_colors(text):
    """颜色循环效果"""

    def demo(screen):
        renderer = FigletText(text, "small")
        effect = Cycle(screen, renderer, screen.height // 2 - 3)
        scene = Scene([effect], 200)
        screen.play([scene])

    Screen.wrapper(demo)


@cli.command()
@click.option('--duration', default=3, help='每个效果的持续时间（秒）')
@click.option('--skip-ui', is_flag=True, help='跳过交互式UI效果')
def show_all(duration, skip_ui):
    """依次运行所有特效"""
    effects = dict(manager.list_effects())

    if not effects:
        click.echo("没有可用的特效")
        return

    click.echo(f"🎬 将依次运行 {len(effects)} 个特效")
    click.echo(f"⏱️  每个特效持续约 {duration} 秒")
    click.echo("⏹️  按 Ctrl+C 可以随时中断演示")
    click.echo("-" * 50)

    for i, (name, info) in enumerate(effects.items(), 1):
        if skip_ui and name == 'ui':
            click.echo(f"⏭️  跳过交互式UI效果 ({i}/{len(effects)})")
            continue

        click.echo(f"🎭 运行特效 {i}/{len(effects)}: {name} - {info['description']}")

        try:
            effect_func = info['function']

            # 检查函数是否需要text参数
            sig = inspect.signature(effect_func)
            if 'text' in sig.parameters:
                default_text = name.replace('-', ' ').title()
                effect_func(text=default_text)
            else:
                effect_func()

            time.sleep(duration)

        except KeyboardInterrupt:
            click.echo("\n⏹️  演示被用户中断")
            sys.exit(0)
        except Exception as e:
            click.echo(f"❌ 执行特效 {name} 时出错: {str(e)}", err=True)

    click.echo("✅ 所有特效演示完成！")


@cli.command()
def list():
    """列出所有可用的特效"""
    effects = dict(manager.list_effects())

    if not effects:
        click.echo("没有可用的特效")
        return

    click.echo("🎭 可用的 Asciimatics 特效:")
    click.echo("-" * 50)

    for name, info in effects.items():
        click.echo(f"  ✨ {name:12} - {info['description']}")


@cli.command()
@click.argument('effect_name')
@click.argument('text', required=False)
def run(effect_name, text):
    """运行指定的单个特效"""
    effect_info = manager.get_effect(effect_name)

    if not effect_info:
        click.echo(f"❌ 特效 '{effect_name}' 不存在")
        click.echo("💡 使用 'list' 命令查看所有可用特效")
        return

    click.echo(f"🎭 运行特效: {effect_name} - {effect_info['description']}")

    try:
        effect_func = effect_info['function']

        # 检查函数是否需要text参数
        sig = inspect.signature(effect_func)
        if 'text' in sig.parameters:
            if text is None:
                # 如果没有提供文本，使用默认值
                text = effect_name.replace('-', ' ').title()
            effect_func(text=text)
        else:
            if text is not None:
                click.echo("⚠️  该特效不需要文本参数，忽略提供的文本")
            effect_func()

    except Exception as e:
        click.echo(f"❌ 执行特效时出错: {str(e)}", err=True)
        sys.exit(1)


# 为原始命令函数添加别名，保持向后兼容
for name, info in manager.list_effects():
    # 这些命令已经在上面用 @cli.command() 装饰过了
    # 这里只是确保它们都在 CLI 中可用
    pass

if __name__ == '__main__':
    cli()