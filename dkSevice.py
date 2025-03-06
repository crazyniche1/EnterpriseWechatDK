import os
import time as tm
from datetime import datetime, time, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

import random


import localLog

import subprocess

import localdk as dk
import localBatteryLevel as batteryLevel

def printC (_str):
    current_time = getCurrentTime ()
    print(current_time,_str)
    logStr ="%s%s" % (current_time, _str) 
    localLog.infoLog(logStr)
    

def getCurrentTime ():
    return  tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime())

def getCurrentTimeStr ():
    return datetime.now().strftime('%Y%m%d%H')

def execute(cmd):
    tcp_devices = get_tcp_devices()
    if tcp_devices:
        for device in tcp_devices:
            adbshell = f"adb -s {device} shell {cmd}"
            print(adbshell)
            os.system(adbshell)
    else:
        print("未找到通过TCP连接的设备，无法执行命令")

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
        print(f"获取设备列表出错: {e}")
        return []  
    

# def hdScreen():
#     printC('#Swipe screen')
#     execute("input swipe 300  1000  300 500")
#     execute("input swipe 300  1000  300 500")

   
def task():
    dk.task()
    addTask()

    
def task2():
    # printC('task2')
    dk.task2()

    
def addTask():
    jobs = scheduler.get_jobs()
    numb = len(jobs)
    printC("$当前调度器中的作业数量:"+ str(numb))
    if(numb < 2) :
        updatejobtimes()


  
def random_time_around_zao():
    random_hour = 9
    lower_bound = time(random_hour, 15)
    upper_bound = time(random_hour, 20)

    random_minute = random.randint(lower_bound.minute, upper_bound.minute)
    return datetime.combine(datetime.today(), time(random_hour, random_minute))

def random_time_around_wan():
    random_hour  = 18
    lower_bound = time(random_hour, 50)
    upper_bound = time(random_hour, 59)


    random_minute = random.randint(lower_bound.minute, upper_bound.minute)
    return datetime.combine(datetime.today(), time(random_hour, random_minute))

scheduler = BackgroundScheduler()

def setup_job():
   
    random_date = random_time_around_zao()
    random_date2 = random_time_around_wan()


    if(datetime.today().hour < random_date.hour) :
        scheduler.add_job(task, 'cron', year=random_date.year, month=random_date.month, day=random_date.day,
                        hour=random_date.hour, minute=random_date.minute, second=random_date.second)
    
    # if(datetime.today().hour < random_date2.hour) :
    scheduler.add_job(task, 'cron', year=random_date2.year, month=random_date2.month, day=random_date2.day,
                    hour=random_date2.hour, minute=random_date2.minute, second=random_date2.second)

    for job in scheduler.get_jobs():
        printC("#job.name:"+ str(job))
    
    preventScrDisconn()

    scheduler.start()

    jobs = scheduler.get_jobs()
    numb = len(jobs)
    printC("The number of jobs currently in the scheduler:"+str(numb))


def random_time_around_zao_m():
    random_hour = 9
    lower_bound = time(random_hour, 1)
    upper_bound = time(random_hour, 15)
    random_minute = random.randint(lower_bound.minute, upper_bound.minute)
    # 获取今天的日期并加上一天得到明天的日期
    tomorrow_date = datetime.today() + timedelta(days=1)
    return datetime.combine(tomorrow_date, time(random_hour, random_minute))

def random_time_around_wan_m():
    random_hour  = 18
    lower_bound = time(random_hour, 45)
    upper_bound = time(random_hour, 59)
    random_minute = random.randint(lower_bound.minute, upper_bound.minute)
    # 获取今天的日期并加上一天得到明天的日期
    tomorrow_date = datetime.today() + timedelta(days=1)
    return datetime.combine(tomorrow_date, time(random_hour, random_minute))


def updatejobtimes():
    random_date = random_time_around_zao_m()
    random_date2 = random_time_around_wan_m()
    scheduler.add_job(task, 'cron', year=random_date.year, month=random_date.month, day=random_date.day,
                      hour=random_date.hour, minute=random_date.minute, second=random_date.second)
    
    scheduler.add_job(task, 'cron', year=random_date.year, month=random_date.month, day=random_date.day,
                      hour=random_date2.hour, minute=random_date2.minute, second=random_date2.second)
    
    for job in scheduler.get_jobs():
        printC("#job.name:"+ str(job))

def preventScrDisconn ():
    scheduler.add_job(task2, 'cron' ,hour='*/2', minute='0', replace_existing=True)


def electricQuantity():
    battery_level = batteryLevel.get_device_battery_level()
    printC(f"#当前电量 : {battery_level}")

setup_job()

try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

    
    