# -*- coding:utf-8 -*-
# file:curses_demo.py
try:
    import curses
except ImportError:
    print("curses 模块不可用，请安装 windows-curses: pip install windows-curses")
    exit(1)

def main(stdscr):
    # 清屏
    stdscr.clear()
    # 添加提示文本
    stdscr.addstr(0, 0, "按 'i' 进入插入模式，按 'q' 退出")
    stdscr.refresh()

    mode = 'command'
    while True:
        key = stdscr.getch()
        if mode == 'command':
            if key == ord('i'):
                mode = 'insert'
                stdscr.addstr(1, 0, "插入模式")
                stdscr.refresh()
            elif key == ord('q'):
                break
        elif mode == 'insert':
            if key == 27:  # ESC
                mode = 'command'
                stdscr.addstr(1, 0, "命令模式")
                stdscr.refresh()
            else:
                stdscr.addch(key)


curses.wrapper(main)