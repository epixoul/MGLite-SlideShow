import os
import re
import json
import time
import webbrowser
import pyautogui
import pygetwindow as gw
from SLDCT import import_imgs
from dotenv import load_dotenv
from win32api import GetSystemMetrics
from bs4 import BeautifulSoup as Soup
from win32gui import FindWindow, MoveWindow

#After you run the "STPScr" script and everything went well, you should run this script, or it will automatically run on startup if you set auto_run_startup to "yes"

#Load .env file
load_dotenv()

#Push log to log file with current system time
sep_flag=True
def push_log(log_val):
    global sep_flag
    launch_log = open('Log_Push/log_launch.txt', 'a+', encoding='utf8')
    if sep_flag:
        launch_log.write(f"\n[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]: New Log -- ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄ --\n")
        sep_flag=False
    launch_log.write(f"[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]: {log_val}\n")
    launch_log.close()

#Check for log is running well
def push_log_check():
    try:
        with open('Log_Push/log_launch.txt', "r") as log:
            log_len = len(log.readlines())
        if log_len >= 500:
            log.close()
            os.remove('Log_Push/log_launch.txt')
            open('Log_Push/log_launch.txt', 'x', encoding='utf8').close()
            log_len = len(open('Log_Push/log_launch.txt', "r").readlines())
        if not log_len:
            launch_log = open('Log_Push/log_launch.txt', 'a+', encoding='utf8')
            launch_log.write(f"-- ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄ -- [Log Starter line] -- ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄ --\n")
            launch_log.close()
            push_log(f"Log file recreate -> Successfully log file recreated.")

    except Exception as err:
        push_log(f"Log file recreate err -> {err}")

#Kill the browser to load properly
def kill_browser():
    try:
        if os.system(f'taskkill /IM {os.getenv('brw_name')}.exe /F') != 0:
            push_log(f"Browser kill err -> Something went wrong while trying to kill browser, but it may work properly.")
        else: push_log(f"Browser kill -> Successfully browser closed.")
    except Exception as err:
        push_log(f"Browser kill err -> {err}")

#Load browser after data passed to Html file
def open_browser():
    os.startfile(os.getenv('brw_exe_path'))
    webbrowser.get(os.getenv('brw_exe_path') + " %s").open(os.path.abspath(os.getenv('html_path')))

#Set delay for process to not throw or cause unwanted errors
def apply_delay(seconds):
    time.sleep(seconds)

#Using "BeautifulSoup" module for data pass
def write_soup_out(soup_ind, tag, attr, patt, js_val):
    script_tag = soup_ind.find(tag, attr)
    script_tag.string = re.sub(str(patt), str(json.dumps(js_val)), script_tag.string)
    with open(os.getenv('html_path'), "wb") as f_output:
        f_output.write(soup_ind.prettify("utf-8"))

#Pass data to Html file
def pass_val_html():
    global jsf
    slides_arr = []
    print()
    try:
        for entry in os.listdir("Slides"):
            full_path = os.path.join("Slides/", entry)
            slides_arr.append(full_path)
        if not os.listdir("Slides"):
            push_log(f"Local slides-folder load err -> Path was empty.")
        else: push_log(f"Local slides-folder load -> Successfully {len(os.listdir("Slides"))} slides locally loaded.")
    except Exception as err:
        push_log(f"Local slides-folder load err -> {err}")

    try:
        with open(os.path.abspath(os.getenv('html_path'))) as html_file:
            soup_ind = Soup(html_file, 'html.parser')
        jsf = open('val.json', 'r')
        jsf = json.load(jsf)
        push_log(f"Html or json file load -> Successfully data files loaded.")
    except Exception as err:
        push_log(f"Html or json file load err -> {err}")

    try:
        write_soup_out(soup_ind, "script",{"id": "json-data"},r".(?<={)(.*?)(?<=})(.*)",jsf)
        write_soup_out(soup_ind, "script",{"id": "img-data"},r".(?<=\[)(.*?)(?<=\])(.*)",slides_arr)
        push_log(f"Html data pass -> Successfully data pushed to html.")
    except Exception as err:
        push_log(f"Html data pass err -> {err}")

#Configure and browser's window control
def configure_window():
    pyautogui.FAILSAFE = False
    display_res = []
    display = int(os.getenv('Selected_display')) - 1
    for i in range(display + 1):
        display_res.append(GetSystemMetrics(i * 78))
        display_res.append(GetSystemMetrics(i * 78 + 1))
    browser_handle = FindWindow(None, gw.getWindowsWithTitle("MGLite Display")[0].title)
    if display:
        MoveWindow(browser_handle, display_res[0], -10, display_res[2] - display_res[0], display_res[3], True)
        pyautogui.moveTo(int((display_res[2] - display_res[0]) / 2) + display_res[0], int(display_res[3]/3))
    else:
        MoveWindow(browser_handle, 0, -10, display_res[0], display_res[1], True)
        pyautogui.moveTo(int(display_res[0] / 2), int(display_res[1]/3))
    apply_delay(3)
    gw.getWindowsWithTitle("MGLite Display")[0].maximize()
    pyautogui.click()
    pyautogui.press(["f11"])
    pyautogui.moveTo(0, display_res[1])

#Load data and process browser load
def st_script():
    push_log_check()
    try:
        kill_browser()
        import_log = import_imgs()
        for i in import_log:
            push_log(i)
        pass_val_html()
        apply_delay(int(os.getenv('load_delay')))
        open_browser()
        apply_delay(int(os.getenv('load_delay')))
        configure_window()
        push_log(f"Slides display -> Successfully slide/slides displayed.")
    except Exception as err:
        push_log(f"Slides display err -> {err}")

st_script()