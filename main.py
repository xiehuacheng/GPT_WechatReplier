import pyautogui
import pyperclip
import time
import pygetwindow
import openai
import re

openai.api_key = ""  # 在这输入你的api

# 定义全局上下文
context = [{'role': 'system', 'content': 'You are an assistant.'}]

reply = ""


# 定义对话处理函数
def process_dialogue(user_input):
    # 将用户输入添加到全局上下文中
    context.append({'role': 'user', 'content': user_input})

    # 发送请求调用GPT
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=context
    )

    # 解析响应并获取机器人的回复
    reply = response['choices'][0]['message']['content']

    # 将机器人的回复添加到全局上下文中
    context.append({'role': 'assistant', 'content': reply})

    # 返回机器人的回复
    return reply


# 调试函数，用于获取窗口的大小，用来设置下面相关的坐标值
# def get_size():
#     # 通过窗口标题获取窗口对象
#     window_title = "微信"
#     window = pygetwindow.getWindowsWithTitle(window_title)[0]
#
#     # 获取窗口的大小
#     window_width = window.width
#     window_height = window.height
#
#     print("窗口大小：", window_width, "x", window_height)


def check_new_messages():
    global context, reply
    while True:
        # 指定对话窗口的区域
        window_rightTop_position = pyautogui.locateOnScreen(
            r"C:\Users\11622\Desktop\GPT_WechatReplier\closeBox.png")  # 这里放置窗口的关闭按钮截图
        while window_rightTop_position is not None:
            window_rightTop_center = pyautogui.center(window_rightTop_position)
            window_rightTop_center_x = window_rightTop_center[0]  # 窗口右上角的 x 坐标
            window_rightTop_center_y = window_rightTop_center[1]  # 窗口右上角的 y 坐标
            window_width = 670  # 窗口的宽度
            window_height = 620  # 窗口的高度

            current_state = pyautogui.screenshot(
                region=(window_rightTop_center_x - window_width, window_rightTop_center_y, window_width,
                        window_height))  # 获取初始对话窗口的截图作为初始状态
            while True:
                new_state = pyautogui.screenshot(region=(
                    window_rightTop_center_x - window_width, window_rightTop_center_y, window_width,
                    window_height))  # 获取新的对话窗口的截图
                if new_state != current_state:  # 如果新截图与初始状态不同，说明有新消息

                    # 指定搜索区域
                    search_region = (
                        window_rightTop_center_x - window_width, window_rightTop_center_y + 530, 670, 90)  # 屏幕下方区域

                    # 获取对方发送的信息
                    other_message_box_position = pyautogui.locateOnScreen(
                        r"C:\Users\11622\Desktop\GPT_WechatReplier\otherMessageBox.png",
                        region=search_region)  # 这里放置其他人的信息气泡截图（绿色）
                    if other_message_box_position is not None:
                        other_message_box_center = pyautogui.center(other_message_box_position)
                        other_message_box_x = other_message_box_center[0] - 30  # 在 x 坐标上减去10
                        other_message_box_y = other_message_box_center[1]
                        pyautogui.doubleClick(other_message_box_x, other_message_box_y)  # 执行双击操作
                        pyautogui.hotkey('ctrl', 'c')  # 复制对方发送的信息
                        other_message = pyperclip.paste()  # 获取剪贴板内容
                        if other_message.startswith("@Chat撅PT "):  # 在这里可以修改机器人的触发条件（关键词）
                            message = re.sub(r"@Chat撅PT ", "", other_message)
                            if message == "重置上下文":
                                reply = "成功重置上下文，可以继续提问啦！"
                                context = [{'role': 'system', 'content': 'You are an assistant.'}]
                            elif message == "展示上下文":
                                reply = "\n".join([f"{msg['role']}: {msg['content']}" for msg in context])
                            else:
                                print("对方发送的信息:", message)
                                print("正在处理对方的信息...")
                                reply = process_dialogue(message)
                                print("处理成功，准备发送...")
                        else:
                            current_state = pyautogui.screenshot(region=(
                                window_rightTop_center_x - window_width, window_rightTop_center_y, window_width,
                                window_height))  # 将新截图设置为当前状态
                            reply = ""
                            continue

                    message_box_position = pyautogui.locateOnScreen(
                        r"C:\Users\11622\Desktop\GPT_WechatReplier\emojiBox.png")  # 这里放置emoji表情的入口图标截图
                    message_box_center = pyautogui.center(message_box_position)
                    message_box_center_x = message_box_center[0]
                    message_box_center_y = message_box_center[1] + 30
                    pyautogui.click(message_box_center_x, message_box_center_y)
                    pyperclip.copy(reply)  # 将自动回复内容复制到剪贴板
                    pyautogui.hotkey('ctrl', 'v')  # 粘贴回复内容到输入框
                    pyautogui.press('enter')
                    print("发送成功！")
                    time.sleep(1)
                    current_state = pyautogui.screenshot(region=(
                        window_rightTop_center_x - window_width, window_rightTop_center_y, window_width,
                        window_height))  # 将新截图设置为当前状态
                    reply = ""
                time.sleep(1)  # 暂停1秒钟，避免频繁检查


if __name__ == '__main__':
    check_new_messages()
