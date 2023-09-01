import os.path
import configparser
import ctypes
import threading
from tkinter import *
from tkinter import ttk
from time import sleep

limit = 100
script_dir = os.getcwd()
monitoring_flag = 0


def get_log_first(path, limit, team, n):
    global log_to_show
    try:
        os.chdir(path)
    except:
        return None
    current_rev = os.popen('svn info --show-item revision').read()
    url = os.popen('svn info --show-item url').read()
    if limit != 0:
        if team != '':
            log = os.popen('svn log --search ' + team + ' -l ' + str(limit) + ' ' + url).read()
        else:
            log = os.popen('svn log' + ' -l ' + str(limit) + ' ' + url).read()
    else:
        if team != '':
            log = os.popen('svn log --search ' + team + ' ' + url).read()
        else:
            log = os.popen('svn log ' + url).read()
    if log == '':
        return None
    log =log.split('------------------------------------------------------------------------')
    list_revs = []
    for i in range(len(log)):
        log_string = log[i]
        log_string = log_string.split('\n')
        if len(log_string) > 2:
            rev = log_string[1].split(' | ')[0][1:]
            if int(rev) == int(current_rev):
                rev = '-> ' + rev
            author = log_string[1].split(' | ')[1]
            date = log_string[1].split(' | ')[2][:19]
            comment = log_string[3]
            to_list_revs = rev + ' | ' + author + ' | ' + date + ' | ' + comment
            list_revs.append(to_list_revs)
    os.chdir(script_dir)
    return list_revs


def get_log(path, team, n):
    global log_to_show, limit
    gray()
    progressbar.start()
    log_to_show = get_log_first(path, limit, team, 0)
    if log_to_show == None:
        limit = 100
        w = ctypes.windll.user32.MessageBoxW(None, u"Incorrect path.",
                                             u"Error!", 0 | 16 | 0x00001000)
        ungray()
        progressbar.stop()
        return
    listbox.delete(0, 'end')
    to_insert = log_to_show
    to_insert.reverse()
    for i in range(len(to_insert)):
        listbox.insert(0, log_to_show[i])
    ungray()
    progressbar.stop()


def is_locked(path, script_dir):
    os.chdir(path)
    os.chdir('..')
    path_splitted = path.split('\\')
    if len(path_splitted[-1]) < 1:
        path_splitted.pop(-1)
    folder_name = path_splitted[-1]
    is_locked = os.popen('2>nul ren ' + folder_name + ' ' + folder_name + ' && echo False || echo True').read()
    os.chdir(script_dir)
    if 'True' in is_locked:
        return True
    else:
        return False


def monitor(path, team, n):
    global monitoring_flag
    os.chdir(path)
    start_rev = os.popen('svn log --revision HEAD').read().split('\n')[1].split(' ')[0][1:]

    while True:
        for i in range(60):
            sleep(1)
            if monitoring_flag == 0:
                monitor_btn['state'] = 'normal'
                return
        log = os.popen('svn log --revision HEAD').read()
        try:
            info = log.split('\n')[1]
            message = log.split('\n')[3]
            monitor_rev = info.split(' ')[0][1:]
        except IndexError:
            continue
        if team in message and monitor_rev != start_rev:
            w = ctypes.windll.user32.MessageBoxW(None, u"Rev: " + monitor_rev,
                                                 u"New build!", 0 | 64 | 0x00001000)
            start_rev = monitor_rev


def update(path, rev, n):
    gray()
    progressbar.start()
    update = os.popen('svn up "' + path + '" -r ' + rev).read()
    try:
        if update.split('\n')[-2] == 'At revision ' + rev + '.':
            w = ctypes.windll.user32.MessageBoxW(None, u"Current revision: " + rev, u"Update finished",
                                                 0 | 64 | 0x00001000)
        else:
            w = ctypes.windll.user32.MessageBoxW(None,
                                                 u"Update failed. Use Clean up command.",
                                                 u"Error!", 0 | 16 | 0x00001000)
    except:
        w = ctypes.windll.user32.MessageBoxW(None,
                                             u"Update failed. Use Clean up command.",
                                             u"Error!", 0 | 16 | 0x00001000)
    ungray()
    progressbar.stop()


def cleanup(path, n):
    global script_dir
    gray()
    progressbar.start()
    os.chdir(path)
    cleanup = os.popen('svn cleanup').read()
    status = os.popen('svn status').read()
    if ' L  ' in status:
        w = ctypes.windll.user32.MessageBoxW(None, u"Clean up failed...",
                                             u"Error!", 0 | 16 | 0x00001000)
    else:
        w = ctypes.windll.user32.MessageBoxW(None, u"Clean up finished.",
                                             u"Success!", 0 | 64 | 0x00001000)
    os.chdir(script_dir)
    ungray()
    progressbar.stop()


def on_exit():
    team = entry_team.get()
    team = team.replace('"', '')
    path = entry_path.get()
    path = path.replace('"', '')
    # Write ini
    to_ini = f'[vars]\nteam = {team}\npath = {path}\n'
    file = open('svn_client_cfg.ini', "w", encoding='utf-8')
    file.write(to_ini)
    file.close()
    exit(0)


####################################################################################################


###########
#         #
#   GUI   #
#         #
###########

cfg = configparser.ConfigParser()

try:
    cfg.read('svn_client_cfg.ini', encoding='utf-8')
    team = cfg.get("vars", "team")
    path = cfg.get("vars", "path")
except:
    file = open('svn_client_cfg.ini', "w", encoding='utf-8')
    team = ''
    path = ''
    to_ini = f'[vars]\nteam = {team}\npath = {path}\n'
    file.write(to_ini)
    file.close()
    cfg.read('svn_client_cfg.ini', encoding='utf-8')
    team = cfg.get("vars", "team")
    path = cfg.get("vars", "path")

try:
    log_to_show = get_log_first(path, limit, team, 0)
except:
    log_to_show = []

# Create a window
window = Tk()
window.title("SVN client")
window.geometry("800x500")
window.minsize(440, 370)
window.resizable(True, True)
# window.iconbitmap(default="icon.ico")
window.protocol("WM_DELETE_WINDOW", on_exit)


# Bind hotkeys in russian layout
def is_ru_lang_keyboard():
    u = ctypes.windll.LoadLibrary("user32.dll")
    pf = getattr(u, "GetKeyboardLayout")
    return hex(pf(0)) == '0x4190419'


def keys(event):
    if is_ru_lang_keyboard():
        if event.keycode == 86:
            event.widget.event_generate("<<Paste>>")
        elif event.keycode == 67:
            event.widget.event_generate("<<Copy>>")
        elif event.keycode == 88:
            event.widget.event_generate("<<Cut>>")
        elif event.keycode == 65535:
            event.widget.event_generate("<<Clear>>")
        elif event.keycode == 65:
            event.widget.event_generate("<<SelectAll>>")


window.bind("<Control-KeyPress>", keys)


def enter_data():
        team = entry_team.get()
        team = team.replace('"', '')
        path = entry_path.get()
        path = path.replace('"', '')
        return team, path


def click_update_btn():
    if entry_path.get() == "" :
        w = ctypes.windll.user32.MessageBoxW(None, u"Path is empty!", u"Error!", 0x1000)
    else:
        team, path = enter_data()
        if is_locked(path, script_dir):
            w = ctypes.windll.user32.MessageBoxW(None, u"Files you try to update are locked. Kill processes which lock these files and press ОК", u"Error!", 0 | 48 | 0x00001000)
        update_thread = threading.Thread(target=update, args=(path, rev, 0), daemon=True)
        update_thread.start()


def click_refresh_btn():
    global log_to_show
    team, path = enter_data()
    refresh_thread = threading.Thread(target=get_log, args=(path, team, 0), daemon=True)
    refresh_thread.start()


def click_next_100_btn():
    global log_to_show, limit
    team, path = enter_data()
    limit += 100
    next_100_thread = threading.Thread(target=get_log, args=(path, team, 0), daemon=True)
    next_100_thread.start()


def click_show_all_btn():
    global log_to_show, limit
    team, path = enter_data()
    limit = 0
    show_all_thread = threading.Thread(target=get_log, args=(path, team, 0), daemon=True)
    show_all_thread.start()


def click_cleanup_btn():
    path = entry_path.get()
    path = path.replace('"', '')
    cleanup_thread = threading.Thread(target=cleanup, args=(path, 0), daemon=True)
    cleanup_thread.start()


def click_monitor_btn():
    global monitoring_flag
    path = entry_path.get()
    path = path.replace('"', '')
    monitor_thread = threading.Thread(target=monitor, args=(path, team, 0), daemon=True)
    if monitor_btn['text'] == 'Start monitoring':
        monitor_btn['text'] = 'Stop monitoring'
        monitoring_flag = 1
        monitor_thread.start()
    else:
        monitor_btn['text'] = 'Start monitoring'
        monitor_btn['state'] = 'disabled'
        monitoring_flag = 0


def onselect(evt):
    global rev
    w = evt.widget
    i = int(w.curselection()[0])
    value = w.get(i)
    value = value.split(' |')
    if '>' in value[0]:
        rev = value[0][3:]
    else:
        rev = value[0]


def gray():
    entry_team['state'] = 'disabled'
    entry_path['state'] = 'disabled'
    update_btn['state'] = 'disabled'
    refresh_btn['state'] = 'disabled'
    next_100_btn['state'] = 'disabled'
    show_all_btn['state'] = 'disabled'
    cleanup_btn['state'] = 'disabled'


def ungray():
    entry_team['state'] = 'normal'
    entry_path['state'] = 'normal'
    update_btn['state'] = 'normal'
    refresh_btn['state'] = 'normal'
    next_100_btn['state'] = 'normal'
    show_all_btn['state'] = 'normal'
    cleanup_btn['state'] = 'normal'


label_team = ttk.Label(text="Filter:")
label_team.pack(anchor='nw', padx=6, pady=6)

entry_team = ttk.Entry()
entry_team.pack(padx=6, pady=6, fill='x')
entry_team.insert(0, team)

label_path = ttk.Label(text="Path:")
label_path.pack(anchor='nw', padx=6, pady=6)

entry_path = ttk.Entry(width=160)
entry_path.pack(padx=6, pady=6, fill='x')
entry_path.insert(0, path)

label_log = ttk.Label(text="Log:")
label_log.pack(anchor='nw', padx=6, pady=6)

revs_var = StringVar(value=log_to_show)
listbox = Listbox(listvariable=revs_var)
scrollbar_horizontal = Scrollbar(listbox, orient="horizontal")
scrollbar_vertical = Scrollbar(listbox, orient="vertical")
listbox.pack(expand=1, fill=BOTH)
listbox['yscrollcommand'] = scrollbar_vertical.set
listbox['xscrollcommand'] = scrollbar_horizontal.set
listbox.bind('<<ListboxSelect>>', onselect)

scrollbar_horizontal.config(command=listbox.xview)
scrollbar_vertical.config(command=listbox.yview)
scrollbar_vertical.pack(side="right", fill="y")
scrollbar_horizontal.pack(side="bottom", fill="x")

progressbar = ttk.Progressbar(window, length=2000, orient="horizontal", mode="indeterminate")
progressbar.pack(side=BOTTOM, padx=6, pady=6)

update_btn = Button(text="Update", command=click_update_btn)
update_btn.pack(side=LEFT, padx=6, pady=6)

refresh_btn = Button(text="Refresh", command=click_refresh_btn)
refresh_btn.pack(side=LEFT, padx=6, pady=6)

next_100_btn = Button(text="Next 100", command=click_next_100_btn)
next_100_btn.pack(side=LEFT, padx=6, pady=6)

show_all_btn = Button(text="Show all", command=click_show_all_btn)
show_all_btn.pack(side=LEFT, padx=6, pady=6)

cleanup_btn = Button(text="Clean up", command=click_cleanup_btn)
cleanup_btn.pack(side=LEFT, padx=6, pady=6)

monitor_btn = Button(text="Start monitoring", command=click_monitor_btn)
monitor_btn.pack(side=LEFT, padx=6, pady=6)


###################################################################################################

window.mainloop()

