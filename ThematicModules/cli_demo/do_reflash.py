# ----------------------------------------------------------------------
# prompt_toolkit 无频闪流式UI最终演示代码
# 保证可运行，包含详细的错误捕获
# ----------------------------------------------------------------------

import asyncio
import traceback
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window, FormattedTextControl, ConditionalContainer
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import Condition

# 1. 定义UI样式，让界面更清晰
style = Style.from_dict({
    'title': 'bold #66d9ef',  # 亮蓝色，醒目
    'line': '#555555',  # 暗灰色分割线
    'param-name': 'bold #f92672',  # 粉色参数名
    'param-value': '#e6db74',  # 黄色参数值
    'streaming-title': 'bold #a6e22e',  # 绿色流式标题
    'thinking': 'italic #75715e',  # 灰色思考文本
    'error': 'bg:#ff0000 #ffffff',  # 错误信息样式
})

# 2. 创建数据缓冲区，作为UI的数据模型
thinking_buffer = Buffer(read_only=True)
tool_name_buffer = Buffer(read_only=True)
path_buffer = Buffer(read_only=True)
content_buffer = Buffer(read_only=True)
error_buffer = Buffer(read_only=True)  # 新增：用于显示错误信息

# 3. 创建状态切换的Event和正确的Filter
show_tool_view = asyncio.Event()
# 使用Condition将函数调用包装成prompt_toolkit能理解的Filter对象
tool_view_active_filter = Condition(lambda: show_tool_view.is_set())

# 4. 定义UI窗口和固定布局
thinking_window = Window(
    FormattedTextControl(lambda: [('class:thinking', thinking_buffer.text)]),
    wrap_lines=True
)

tool_name_window = Window(
    FormattedTextControl(lambda: [
        ('class:title', 'Tool Call: '),
        ('class:param-value bold', tool_name_buffer.text)
    ]),
    height=1
)

path_window = Window(
    FormattedTextControl(lambda: [
        ('class:param-name', '  path: '),
        ('class:param-value', path_buffer.text)
    ]),
    height=1
)

content_window = Window(
    content=FormattedTextControl(lambda: [('class:param-value', content_buffer.text)]),
    wrap_lines=True
)

error_window = Window(
    content=FormattedTextControl(lambda: [('class:error', error_buffer.text)]),
    wrap_lines=True
)

# 组合成工具调用视图
tool_call_container = HSplit([
    tool_name_window,
    path_window,
    Window(height=1, char='─', style='class:line'),
    Window(FormattedTextControl([('class:streaming-title', 'Streaming Content...')]), height=1),
    content_window,
])

# 5. 使用ConditionalContainer进行无闪烁视图切换
root_container = HSplit([
    ConditionalContainer(
        content=thinking_window,
        filter=~tool_view_active_filter  # 对Filter对象使用取反操作
    ),
    ConditionalContainer(
        content=tool_call_container,
        filter=tool_view_active_filter  # 直接使用Filter对象
    ),
    # 新增：一个条件性显示的错误窗口
    ConditionalContainer(
        content=error_window,
        filter=lambda: bool(error_buffer.text)
    ),
])

layout = Layout(root_container)

# 6. 定义键绑定
kb = KeyBindings()


@kb.add('c-c', eager=True)
def _(event):
    """ 按 Ctrl-C 退出 """
    event.app.exit(result="Cancelled by user.")


# 7. 创建Application实例
app = Application(layout=layout, key_bindings=kb, style=style, full_screen=True)


# 8. 异步任务：模拟LLM流并更新UI
async def mock_llm_stream():
    try:
        # 阶段一：思考
        thinking_text = "Okay, the user wants to see a working demo. I will now display the `file.write` tool call. First, the 'thinking' phase..."
        for char in thinking_text:
            thinking_buffer.text += char
            await asyncio.sleep(0.03)

        await asyncio.sleep(2)

        # 阶段二：切换到工具调用视图
        show_tool_view.set()

        # 阶段三：流式填充工具名和参数
        tool_name = "file.write"
        for char in tool_name:
            tool_name_buffer.text += char
            await asyncio.sleep(0.05)

        await asyncio.sleep(0.5)

        path_text = "src/components/final_demo.js"
        for char in path_text:
            path_buffer.text += char
            await asyncio.sleep(0.05)

        await asyncio.sleep(1)

        # 阶段四：流式填充内容
        content_text = """import React from 'react';

// This component demonstrates a flicker-free streaming UI
const FinalDemo = () => {
  return (
    <div>
      <h1>Success!</h1>
      <p>This content was rendered by prompt_toolkit without any screen flickering.</p>
    </div>
  );
};

export default FinalDemo;
"""
        for char in content_text:
            content_buffer.text += char
            await asyncio.sleep(0.015)

        # 阶段五：等待几秒钟然后退出
        await asyncio.sleep(5)
        app.exit(result="Simulation finished successfully.")

    except Exception:
        # 终极错误捕获：获取完整的追溯信息并显示在UI中
        error_message = traceback.format_exc()
        error_buffer.text = error_message
        # 让应用再运行一段时间以显示错误，然后退出
        await asyncio.sleep(10)
        app.exit(result="Exited due to an unexpected error.")


# 9. 运行主程序
async def main():
    # 在后台运行模拟流任务
    simulation_task = asyncio.create_task(mock_llm_stream())

    # 运行并等待UI应用退出
    result = await app.run_async()

    # 打印最终结果，无论成功或失败
    print(f"\n--- Application Result ---\n{result}\n--------------------------")

    # 确保后台任务也被取消，避免挂起
    simulation_task.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (EOFError, KeyboardInterrupt):
        print("\nApplication exited by user.")

