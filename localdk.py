import os
import time as tm
from datetime import datetime, time, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

import localLog

import subprocess
import localBatteryLevel as batteryLevel
import uiautomator2 as u2

import dkNotification as notification


def printC (_str):
    current_time = getCurrentTime ()
    print(current_time,_str)
    logStr ="%s%s" % (current_time, _str) 
    localLog.infoLog(logStr)
    
    

def getCurrentTime ():
    return  tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime())

def getCurrentTimeStr ():
    return datetime.now().strftime('%Y%m%d%H')

def disconnect():
    # adb disconnect 192.168.1.101:5555
    tcp_devices = get_tcp_devices()
    if tcp_devices:
        for device in tcp_devices:
            adbshell = f"adb disconnect {device}"
            printC(adbshell)
            os.system(adbshell)
    else:
        printC("#未找到通过TCP连接的设备，无法执行命令")


def execute(cmd):
    tcp_devices = get_tcp_devices()
    if tcp_devices:
        for device in tcp_devices:
            adbshell = f"adb -s {device} shell {cmd}"
            printC(adbshell)
            os.system(adbshell)
    else:
        printC("#未找到通过TCP连接的设备，无法执行命令")



def executepull():
    tcp_devices = get_tcp_devices()
    if tcp_devices:
        for device in tcp_devices:
            # os.system("adb pull /sdcard/"+getCurrentTimeStr()+".png D:\dkimg")
            adbshell = f"adb -s {device} pull /sdcard/"+getCurrentTimeStr()+".png D:\dkimg"
            printC(adbshell)
            os.system(adbshell)
    else:
        printC("未找到通过TCP连接的设备，无法执行命令")

def get_tcp_devices():
    try:
        output = subprocess.check_output(['adb', 'devices'])
        output_str = output.decode('utf-8')
        lines = output_str.strip().splitlines()[1:]  # 去掉表头那行
        tcp_devices = []

        for line in lines:
            device_info = line.strip().split('\t')
            device_serial = device_info[0]
            if "UYT5T18319017153".lower() in device_serial.lower() :
                tcp_devices.append(device_serial) 
            # 这里假设你有方法判断该设备是TCP连接的，比如通过设备名包含特定字符串等方式
            if device_serial.lower().startswith("192."):
                tcp_devices.append(device_serial)

        if len(tcp_devices) > 1:
            return [tcp_devices[0]]  # 只保留第一个设备

        return tcp_devices
    except subprocess.CalledProcessError as e:
        printC(f"获取设备列表出错: {e}")
        return []  

def unlockScreen ():
    #点亮屏并解锁--ing
    printC('#unlockScreen')
    #224 为点亮屏幕 可能会失效  使用LockScreen 代替
    # execute("input keyevent 224")
    # 判断是否黑屏　如果是则点亮屏幕
    device_status = batteryLevel.get_device_status()
    if device_status == 'OFF':
        LockScreen()
    else:
        printC('#The screen is already on')

    # 判断是否已经解锁，如果没有则解锁
    is_lock = batteryLevel.get_device_jiesuo()

    if is_lock == 'true':
        hdScreen()
        unlockByInput ()
        
    else:
        printC('#The screen is already unlocked')

    try:
        wx_new ()
    except Exception as e:
        printC("#wx_new error :{e}")
    
def unlockByInput ():
    execute("input mouse tap 542 1382")
    execute("input mouse tap 542 1505")
    execute("input mouse tap 542 1792")
    execute("input mouse tap 542 1078")

def wx ():
    execute("am force-stop com.tencent.wework")
    tm.sleep(10)

    printC('#open-wx')
    execute("am start com.tencent.wework/com.tencent.wework.launch.LaunchSplashActivity")
    tm.sleep(10)

    printC('#open work')
    execute("input mouse tap 780 1850")
    
    printC('#open ka')
    execute("input mouse tap 162 887")
    
    tm.sleep(10)
    printC('#ka area')
    execute("input mouse tap 550 1400")
    tm.sleep(5)
    
    saveTolocal()
    
    printC('#ka cacel')
    execute("input mouse tap 340 1250")
    
    printC('#returen last')
    execute("input keyevent 4")
    
    printC('#return HOME')
    execute("input keyevent 3")
    
    # 防止发送失败不继续执行
    try:
        sendEmail()
    except Exception as e:
        printC("#email error :{e}")

    LockScreen()

    # addTask()

def connect():
    tcp_devices = get_tcp_devices()
    if tcp_devices:
        for device in tcp_devices:
            d = u2.connect(device)
            return d
    else:
        printC("#未找到通过TCP连接的设备，无法执行命令")
        return None

def button_area_dk_text():
    return '上班打卡' if datetime.now().hour < 12 else '下班打卡'

package_name = 'com.tencent.wework'  
activity_name = 'com.tencent.wework.launch.LaunchSplashActivity' 

def wx_new ():
    d = connect()
    # 有时会有USB弹窗，点击取消
    printC('#点击取消')

    
    button_text = '取消'
    if d(text=button_text).exists:
        d(text=button_text).click()

    # 关闭App
    d.app_stop(package_name)

    tm.sleep(5)
    printC('#open-wx')
    d.app_start(package_name, activity_name)
   
    tm.sleep(10)
    printC('#open work')
    button_text = '工作台'
    if d(text=button_text).exists:
        d(text=button_text).click()
    
    
    tm.sleep(5)
    printC('#open ka')
    button_text = '打卡'
    if d(text=button_text).exists:
        d(text=button_text).click()
    
    tm.sleep(10)
    button_text = button_area_dk_text()
    printC(f'ka cacel:{button_text}')
    if d(text=button_text).exists:
        d(text=button_text).click()
    
    tm.sleep(5)
    printC('#ka cacel')
    button_text = '取消'
    if d(text=button_text).exists:
        d(text=button_text).click()

    tm.sleep(5)
    saveTolocal()
    
    # 关闭App
    tm.sleep(5)
    d.app_stop(package_name)
    
    # 防止发送失败不继续执行
    try:
        printC('# sendEmail')
        # sendEmail()
        
    except Exception as e:
        printC("#email error :{e}")

    LockScreen()



def saveTolocal ():
    printC('#Take a screenshot and save it locally D:\dkimg')
    try :
        execute('screencap -p /sdcard/'+getCurrentTimeStr()+'.png')
        tm.sleep(10)
        executepull()
        # os.system("adb pull /sdcard/"+getCurrentTimeStr()+".png D:\dkimg")
    except Exception as e:
        printC(f"saveTolocal fail：{e}")
        errorBegin ()
        
   
def errorBegin ():
   
    execute("am force-stop com.tencent.wework")
    execute("input keyevent 3")
    tm.sleep(3)
    wx_new ()
    

def hdScreen():
    printC('#Swipe screen')
    execute("input swipe 300  1000  300 500")
    execute("input swipe 300  1000  300 500")

def LockScreen():
    printC('#Lock screen')
    execute("input keyevent 26")
   
def task():
    printC("#Perform a task------")
    unlockScreen()

def task2():
    printC("$Perform a task2------")
    device_status = batteryLevel.get_device_status()
    if device_status == 'OFF':
        LockScreen()
    hdScreen()
    if device_status == 'ON':
        LockScreen()

    # battery_level = batteryLevel.get_device_battery_level()
    # print(battery_level)
    # if battery_level is not None and  battery_level < 30:
    #     notification.win_notification(battery_level)
    


def execute1 (cmd ):
    adbshell  =f"adb shell {cmd}"

    try:
        # 使用 subprocess.run 执行命令并捕获输出和错误
        result = subprocess.run(adbshell, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 输出命令的标准输出
        printC("Command Output:")
        printC(result.stdout)
        
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，捕获错误并输出
        printC("Command Error:")
        printC(e.stderr)

def sendEmail ():  
    printC('#send email')

    # 设置发件人邮箱、密码和收件人邮箱
    sender_email = '****@qq.com'
    sender_password = '****'
    receiver_email = '****@qq.com'


    # 设置邮件主题和内容
    subject = "打卡"
    body = "结果"

   # 创建一个MIMEMultipart邮件对象
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    # 设置邮件头部
    msg['From'] = Header(sender_email)
    msg['To'] = Header(receiver_email)
    msg['Subject'] = Header(subject)
    # image_path = "D:\\dkimg\\" +getCurrentTimeStr()+".png"
    # 读取图片并添加到邮件中 
    # with open(image_path, 'rb') as f:
              
    #     img = MIMEImage(f.read())
    #     # 可以设置图片的CID，用于在HTML中引用
    #     img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
    #     msg.attach(img)
    #     msg.attach(MIMEText('成功', 'plain', 'utf-8'))
    #     tm.sleep(5)

    # 发送邮件
    try:
        printC("#set email SMTP") 
        server = smtplib.SMTP_SSL('smtp.139.com',465)
        # server.starttls() 
        printC("#login email")
        server.login(sender_email, sender_password)
        tm.sleep(5)
        printC("#send email")
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        tm.sleep(5)
        printC("#email success")
        server.quit()

    except smtplib.SMTPConnectError:
        printC("#Unable to connect to SMTP server. Check your network connection and server Settings。")


    except smtplib.SMTPAuthenticationError:
        printC("#The email address or password is incorrect. Please check your login credentials。")


    except Exception as e:
        printC(f"#email error :{e}")
        tm.sleep(5)
        # sendEmail ()

    
    