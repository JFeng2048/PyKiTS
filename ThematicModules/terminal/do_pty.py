import subprocess
import sys
# import pexpect


class TerminalAutomation:
    def __init__(self):
        self.output_buffer = ""

    def run_command_simple(self, command):
        """执行简单命令并返回输出[citation:6]。"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Command timed out'}

    def run_command_realtime(self, command, timeout=30):
        """实时执行命令并收集输出。"""
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                       bufsize=1)
            self.output_buffer = ""  # 清空缓冲区

            while True:
                output = process.stdout.readline()
                if output:
                    self.output_buffer += output
                    sys.stdout.write(output)  # 实时打印到控制台
                    sys.stdout.flush()
                if process.poll() is not None:
                    break
            return {'success': process.returncode == 0, 'returncode': process.returncode}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    # def run_interactive_command(self, command, interactions=None):
    #     """执行交互式命令。"""
    #     try:
    #         child = pexpect.spawn(command, encoding='utf-8')
    #         child.logfile_read = sys.stdout  # 实时输出到控制台
    #
    #         if interactions:
    #             for prompt, response in interactions:
    #                 child.expect(prompt)
    #                 child.sendline(response)
    #
    #         child.expect(pexpect.EOF)  # 等待命令结束
    #         return {'success': True, 'output': child.before}
    #     except pexpect.EOF:
    #         return {'success': False, 'error': 'Unexpected EOF'}
    #     except pexpect.TIMEOUT:
    #         return {'success': False, 'error': 'Timeout'}


# 使用示例
automator = TerminalAutomation()

# 1. 执行简单命令
result = automator.run_command_simple("dir")
if result['success']:
    print("命令成功！")
    print(result['stdout'])
else:
    print("命令失败:", result.get('stderr', result.get('error')))

# 2. 实时执行长时间运行命令
result = automator.run_command_realtime("python -c 'for i in range(5): print(f\"Line {i}\")'")
print("最终捕获的输出:", automator.output_buffer)

# 3. 执行交互式命令 (例如需确认的操作)
interactions = [("Are you sure?", "yes")]
# result = automator.run_interactive_command("rm important_file.txt", interactions)