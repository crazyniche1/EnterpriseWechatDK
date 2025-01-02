import tkinter as tk
import tkinter.messagebox as tkmb
import localdk as dk
import time as tm
import threading as thread

import sched

import localBatteryLevel as batteryLevel

def get_battery_percentage():
    battery = batteryLevel.get_device_battery_level()
    if(battery < 30):
        hitErrorDL ()
    return battery

refreshCount = 0

def update_battery_label＿Thread():
    thread.Thread(target= update_battery_label).start()

def update_battery_label():
    global refreshCount # 声明 refreshCount 是全局变量
    battery_percent.set(f'{refreshCount}电量: {get_battery_percentage()}%')
    # 更新频率：每12小时更新一次 
    root.after(1000*60*60*12, update_battery_label)
   
    if(refreshCount < 100):
        refreshCount=refreshCount+1
    else:
        refreshCount = 0


def dksTask ():
    # print('dksTask')
     dk.task()

def wifiConnect ():
    thread.Thread(target= wifiConnectByThread).start()
   

def wifiConnectByThread ():
    output_str = batteryLevel.execute1('scrcpy --tcpip')
    # print('dksTask'+output_str)

delayedMin = 1

def delayThread ():
    global delayedMin
    delayedMin = float( entry_var.get() )
    thread.Thread(target= delayedTask).start()

def delayedTask():
    global refreshCount
    # 初始化 sched 模块的 scheduler 类
    scheduler = sched.scheduler(tm.time, tm.sleep)
    # 增加调度任务
    scheduler.enter(60 * delayedMin, 1, dksTask)
    # 运行任务
    scheduler.run()

# 创建窗口
root = tk.Tk()
root.title("监控电量")
root.geometry('400x200')

battery_percent = tk.StringVar()
battery_percent.set(f'初始化电量')

label = tk.Label(root, 
                 textvariable=battery_percent, 
                 font=("Helvetica", 20), 
                 padx= 40 ,
                 pady= 10 ,
                                  
                 )
label.pack()

Button = tk.Button(root, text="wifi connect",bg="#F0F0F0", width=10,   padx= 40 , pady= 10 ,command = wifiConnect)
Button.pack(padx=10,pady=10)

Button1 = tk.Button(root, text="begin",bg="#F0F0F0", width=10,   padx= 40 , pady= 10 ,command = dksTask)              
Button1.pack()

Button2 = tk.Button(root, text="refresh",bg="#F0F0F0", width=10,   padx= 40 , pady= 10 ,command = update_battery_label)
Button2.pack(padx=10,pady=10)

entry_var = tk.StringVar(value= delayedMin )
Entry = tk.Entry(root, bd =1, textvariable=entry_var )
Entry.pack(padx=10,pady=10,side = tk.RIGHT)

Button3 = tk.Button(root, text="delayed",bg="#F0F0F0", width=10,   padx= 40 , pady= 10 ,command = delayThread)
Button3.pack(padx=10,pady=10,side = tk.LEFT)




def hitErrorDL ():
    tkmb.showerror(title='提示', message='电量不足！')


# 设置窗口始终在最前
root.attributes('-topmost', True)

update_battery_label()

# 启动主循环
root.mainloop()


