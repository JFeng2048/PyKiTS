# -*- coding:utf-8 -*-
# file:do_terminaltexteffects.py
"""
pip install terminaltexteffects

python do_terminaltexteffects.py all
"""
import click
import subprocess
import sys


@click.group()
def tte_demo():
    """TerminalTextEffects 特效演示管理程序"""
    pass


# 以下是各个特效的演示命令，你可以根据需要继续添加

@tte_demo.command()
@click.argument('text', default='Hello TTE!')
def beams(text):
    """光束特效 - 光束扫过显示文字"""
    run_tte_effect('beams', text)


@tte_demo.command()
@click.argument('text', default='Matrix')
def matrix(text):
    """矩阵数字雨效果"""
    run_tte_effect('matrix', text)


@tte_demo.command()
@click.argument('text', default='Fireworks!')
def fireworks(text):
    """烟花绽放效果"""
    run_tte_effect('fireworks', text)


@tte_demo.command()
@click.argument('text', default='It is raining')
def rain(text):
    """下雨效果"""
    run_tte_effect('rain', text)


@tte_demo.command()
@click.argument('text', default='Decrypting')
def decrypt(text):
    """解密效果（类似电影中的解密场景）"""
    run_tte_effect('decrypt', text)


@tte_demo.command()
@click.argument('text', default='Bouncing')
def bounce(text):
    """弹跳球效果"""
    run_tte_effect('bouncyballs', text)


@tte_demo.command()
@click.argument('text', default='Black Hole')
def blackhole(text):
    """黑洞效果 - 文字被黑洞吸入"""
    run_tte_effect('blackhole', text)


@tte_demo.command()
@click.argument('text', default='Bubbles')
def bubbles(text):
    """气泡效果"""
    run_tte_effect('bubbles', text)


@tte_demo.command()
@click.argument('text', default='Burning')
def burn(text):
    """燃烧效果"""
    run_tte_effect('burn', text)

@tte_demo.command()
@click.argument('text')
@click.option('--speed', default=1.0, help='动画速度')
def beams(text, speed):
    run_tte_effect('beams', text, speed)

@tte_demo.command()
@click.option('--text', default='All Effects', help='要显示的文本')
def all(text):
    """执行所有特效"""
    effects = [
        ('beams', text),
        ('matrix', 'Matrix'),
        ('fireworks', 'Fireworks!'),
        ('rain', 'It is raining'),
        ('decrypt', 'Decrypting'),
        ('bouncyballs', 'Bouncing'),
        ('blackhole', 'Black Hole'),
        ('bubbles', 'Bubbles'),
        ('burn', 'Burning')
    ]
    
    for effect_name, effect_text in effects:
        click.echo(f"\n正在执行 {effect_name} 特效...")
        run_tte_effect(effect_name, effect_text)
        click.echo(f"{effect_name} 特效执行完成\n" + "="*50)


def run_tte_effect(effect_name: str, text: str):
    """运行指定的 TTE 特效"""
    try:
        # 通过子进程调用 TTE，使用 stdin 传递文本
        result = subprocess.run(
            ['tte', effect_name],
            input=text,
            capture_output=False,  # 设为 False 以便实时看到特效输出
            text=True
        )

        # 检查命令执行是否成功
        if result.returncode != 0:
            click.echo(f"错误：执行 {effect_name} 特效时出现问题", err=True)

    except FileNotFoundError:
        click.echo("错误：未找到 tte 命令。请确保已安装 TerminalTextEffects。", err=True)
        click.echo("安装命令：pip install terminaltexteffects", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"未知错误：{str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    tte_demo()