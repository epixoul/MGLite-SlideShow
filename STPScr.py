import os
import time
import dotenv as dte
import json
import re
import threading

#First of all you should run this code, if any error occurred you should check "log_stp" to fix the problem. If you couldn't then let ous know on "https://github.com/epixoul/MGLite-SlideShow"
#Push log to log file with current system time
def push_log(log_val):
    stp_log = open('Log_Push/log_stp.txt', 'a+', encoding='utf8')
    stp_log.write(f"[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}]: {log_val}\n")
    stp_log.close()

#Create Log, Json, Env Files
for i in ["Log_Push/log_stp.txt", "Log_Push/log_launch.txt", ".env", "val.json"]:
    try:
        if os.path.exists(i):
            os.remove(f"{i}")
        open(f'{i}', 'x', encoding='utf8').close()
        if i == "Log_Push/log_stp.txt":
            log_St = open('Log_Push/log_stp.txt', 'a+', encoding='utf8')
            log_St.write(f"-- ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄ -- [Log Starter line] -- ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄ --\n\n")
            log_St.close()
        push_log(f"File (re)generation -> \"{re.search(r'[^/]+$', i).group(0)}\" file (re)created.")
    except Exception as err:
        push_log(f"File (re)generation -> \"{re.search(r'[^/]+$', i).group(0)}\" -> {err}")
        print(err)

#Load Json and .Env files
env = open(".env", "w+", encoding='utf8')
jsf = open('val.json', 'w+', encoding='utf8')

try:
    dte.load_dotenv()
    push_log(f".ENV load -> Successfully .env file loaded.")
except Exception as err:
    push_log(f".ENV load err -> {err}")

#Load Slides path and determine config which will be used
bw_path = ""
_flag = False
ct=0
for ctt in os.listdir("Slides"):
    ct+=1
if not ct:
    push_log(f"Slides load err -> No Slides loaded, It can cause corruption.")
else:   push_log(f"Slides load -> Successfully {ct} Slides loaded.")
val={'load_delay': '4',
     'selected_display': '1',
     'brw_name': 'opera',
     'brw_drive_install_path': 'c:/',
     'brw_exe_path': 'auto',
     'html_path': 'ssh.html',
     'slide_show_time_ms': f'{int(1800/ct) if 15 >= ct > 0 else 120}000',
     'show_slides_randomly' : 'yes',
     'show_slides_by_click' : 'no',
     'auto_run_startup': 'yes'}
temp_val=val

#Find browser run file
def brw_exe_find(name, path):
    global bw_path
    try:
        for root, dirs, files in os.walk(path):
            if name in files:
                bw_path = os.path.join(root, name)
                return
            if _flag:
                return
    except Exception as err:
        print(err)
        return

#Progress text line as thread
def progr_termin():
    global _flag
    cc=124
    for i in "Please wait to complete the searching...  ":
        cc+=1
        print(f"\033[38;5;{cc}m"+i, end='')
        time.sleep(0.03)
    animation = ['|', '/', '—', '\\']
    while not _flag:
        for char in animation:
            if _flag: break
            print("\033[38;5;208m"+f"\b\b{char} ", end='', flush=True)
            time.sleep(0.3)

#Thread control function
def thrd_fun():
    global _flag, bw_path
    bw_path_th = threading.Thread(target=brw_exe_find,
                                  args=(f'{val["brw_name"]}.exe', f'{val["brw_drive_install_path"]}',))
    proger = threading.Thread(target=progr_termin)
    proger.start()
    bw_path = 'NotFound'
    bw_path_th.start()
    bw_path_th.join(20)
    _flag = True
    proger.join(0)
    time.sleep(3)

#Input or process setup data
def stp_vals():
    print("\033[38;5;208m"+"These are examples for "+"\033[38;5;197m"+"\"Opera Gx\""+"\033[38;5;208m"+" run, you can change the parameters:\n⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄")
    for i in val:
        try:
            if i=="brw_exe_path":
                print("\033[38;5;208m"+"*- \"If you press "+"\033[38;5;197m"+"\"Enter\""+"\033[38;5;208m"+", it will automatically search for the browser path in the drive/path you specified.\"\n"
                      "*- \"Please wait for the message to show up, as it may take some time to complete the search...\"\n⌄ ⌄ ⌄  ⌄ ⌄ ⌄  ⌄ ⌄ ⌄")
            var = input("\033[38;5;154m"+f"— Input "+"\033[38;5;135m"+f"{i}"+"\033[38;5;154m"+" value [Default example value: "+"\033[38;5;135m"+f"{val[i]}"+"\033[38;5;154m"
                        "]\nIf you don't want to change it, then press "+"\033[38;5;197m"+"\"Enter\""+"\033[38;5;154m"+" <<  ")
            if var.strip():
                temp_val[i]=val[i]=var.strip().lower()
                print("\033[38;5;197m" +f"-\"{var.strip().lower()}\"")
            else: print("\033[38;5;197m"+f"-\"{val[i]}\"")
            if i == "brw_exe_path":
                global bw_path
                if not var:
                    thrd_fun()
                    var=bw_path
                temp_val[i] = val[i] = re.sub(r"\\", "/", str(var)).strip().lower()
                print("\033[38;5;208m"+f"\r \b*- Search is Done! -> result: "+"\033[38;5;197m"+f"{val[i]}")
                push_log(f"Browser .exe path catch -> {val[i]} -> {"The path is valid." if os.path.exists(val[i]) else "The path isn't valid or Null."}")
            dte.set_key(dte.find_dotenv(),i,val[i].lower())
        except Exception as err:
            push_log(f"Input value evaluate err -> {err}")
    try:
        json.dump(temp_val, jsf, ensure_ascii=False, indent=4)
        push_log(f"JSON evaluate -> Successfully data evaluated.")
    except Exception as err:
        push_log(f"JSON evaluate err -> {err}")
    jsf.close()
    env.close()

stp_vals()