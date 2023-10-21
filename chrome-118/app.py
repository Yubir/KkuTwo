import time
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import sv_ttk

# 대기 프린트
print(
"""
끄투 도우미 창이 켜지고 있습니다.

끄투 도우미는 끄투 코리아 게임에 접속 후에 사용해주세요.
"""
)

def enter_message(event=None):
    message = entry.get()
    entry.delete(0, tk.END)
    send_message(message)

def send_message(message):
    # 끄투 채팅입력창 찾기
    input_element = driver.find_element(
        By.CSS_SELECTOR,
        'input[style="float: left; border-right: none; border-top-right-radius: 0px; border-bottom-right-radius: 0px; margin-top: 5px; width: calc(100% - 82px); height: 20px;"]'
    )

    # 채팅에 입력하기
    for char in message:
        input_element.send_keys(char)
        time.sleep(0.05)  # 실제 사람인 것처럼 쿨타임 조정 [ 마음대로 조정하셔도 됩니다 ]

    # 채팅에 입력 후 엔터 누르기
    input_element.send_keys('\n')

def reload_words():
    global lines
    lines = []
    file_names = ["한국어-끝말잇기.txt", "영어-끝말잇기.txt", "한국어-끝말잇기-추가.txt", "다른.txt"]  # 단어 파일명 목록
    for file_name in file_names:
        with open(file_name, "r", encoding="utf-8") as file:
            lines += file.readlines()
    print("단어 메모장을 다시 불러왔습니다.")

# 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 크롬드라이버 거시기 경로
driver_path = 'chromedriver.exe'

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# 끄투 코리아에 접속 
driver.get("https://kkutu.co.kr/")

# 텍스트 연속뜨기 방지
previous_text = None

# 파일 읽기
lines = []
file_names = ["한국어-끝말잇기.txt", "영어-끝말잇기.txt", "한국어-끝말잇기-추가.txt"]  # 단어 파일명 목록
for file_name in file_names:
    with open(file_name, "r", encoding="utf-8") as file:
        lines += file.readlines()

# tkinter 폼 만들기
window = tk.Tk()
window.title("KKuTwo Helper")

# sv_ttk를 사용하여 다크 모드 테마 적용하기
sv_ttk.set_theme("dark")

# 프레임 만들기
input_frame = ttk.Frame(window)
input_frame.pack(pady=10)

# 입력창 만들기 ( 엔터로도 전송 가능 )
entry = ttk.Entry(input_frame, width=30)
entry.pack(side=tk.LEFT)
entry.bind("<Return>", enter_message)

# 전송버튼 만들기
send_button = ttk.Button(input_frame, text="전송", command=enter_message)
send_button.pack(side=tk.LEFT)

# 단어 다시 불러오기 버튼 만들기
reload_button = ttk.Button(input_frame, text="단어 다시 불러오기", command=reload_words)
reload_button.pack(side=tk.LEFT)

# 텍스트 박스 만들기 ( 단어가 뜰 )
text_box = tk.Text(window)
text_box.pack(fill=tk.BOTH, expand=True)

# 텍스트 박스를 윈도우 크기만큼 조정
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)

# 텍스트 박스를 클릭했을 때 채팅창에 입력되도록 처리하기
def on_textbox_click(event):
    index = text_box.index(tk.CURRENT)
    line_number = index.split('.')[0]
    line_start = line_number + ".0"
    line_end = line_number + ".end"
    selected_line = text_box.get(line_start, line_end)

    if selected_line.strip() != "":
        # 누르는 즉시 채팅창에 입력하기
        send_message(selected_line)

text_box.bind("<Button-1>", on_textbox_click)

# 끄투코리아 인 게임에 단어가 뜰 때까지 대기하기
while True:
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jjo-display"))
        )
        if element.is_displayed():
            text = element.text
            if text != previous_text:
                text_box.insert("1.0", "\n\n\n")
                previous_text = text

                # 앞자리가 같은 단어를 찾고 textbox에 출력하기
                # 'A(B)'와 같은 형태인 경우를 분리하여 처리하기
                if '(' in text and ')' in text:
                    text_without_brackets = text.split('(')[0]
                    text_in_brackets = text.split('(')[1].split(')')[0]

                    # 괄호 안의 내용 (text_in_brackets)를 먼저 출력하기
                    matching_lines_in_brackets = [line.strip() for line in lines if line.strip().startswith(text_in_brackets)]
                    unique_matching_lines_in_brackets = set(matching_lines_in_brackets)
                    sorted_lines_in_brackets = sorted(unique_matching_lines_in_brackets, key=len, reverse=True)
                    for line in sorted_lines_in_brackets[::-1]:
                        text_box.insert("1.0", line + "\n")

                    # 괄호 밖의 내용 (text_without_brackets)를 나중에 출력하기
                    matching_lines_without_brackets = [line.strip() for line in lines if line.strip().startswith(text_without_brackets)]
                    unique_matching_lines_without_brackets = set(matching_lines_without_brackets)
                    sorted_lines_without_brackets = sorted(unique_matching_lines_without_brackets, key=len, reverse=True)
                    for line in sorted_lines_without_brackets[::-1]:
                        text_box.insert("1.0", line + "\n")

                # 일반적인 경우 처리하기
                else:
                    matching_lines = [line.strip() for line in lines if line.strip().startswith(text)]
                    unique_matching_lines = set(matching_lines)
                    sorted_lines = sorted(unique_matching_lines, key=len, reverse=True)
                    for line in sorted_lines[::-1]:
                        text_box.insert("1.0", line + "\n")
    except:
        pass

    window.update_idletasks()
    window.update()

# 드라이버 종료 ( 사용안함 )
# driver.quit()

window.mainloop()