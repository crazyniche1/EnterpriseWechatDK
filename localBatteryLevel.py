import os
import time as tm
from datetime import datetime, time, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

import subprocess
import re

def task():
    print('task')

def execute(cmd):
    tcp_devices = get_tcp_devices()
    if tcp_devices:
        for device in tcp_devices:
            adbshell = f"adb -s {device} shell {cmd}"
            return execute1(adbshell)
    else:
        print("未找到通过TCP连接的设备，无法执行命令")
        return None

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
    
    
def execute1 (cmd ):
    adbshell  = cmd
    try:
        # 使用 subprocess.run 执行命令并捕获输出和错误
        result = subprocess.run(adbshell, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 输出命令的标准输出
        # print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，捕获错误并输出
        print("Command Error:")
        print(e.stderr)
        return None

def get_device_battery_level():
    try:
        output_str = execute('dumpsys battery')
        match = re.search(r'level:\s*(\d+)', output_str)
        if match:
            # 提取并返回电量信息
            battery_level = match.group(1)
            return int(battery_level)
        else:
            print("Could not find battery level information.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"获取电量信息出错: {e}")
        return None

def get_device_status():
    try:
        #显示屏幕状态 ON 为亮屏，OFF 为息屏
        output_str = execute(' dumpsys power | findstr /R /C:"Display Power: state=" ')
        value = output_str.split('=')[-1].strip()
        print(f"显示屏幕状态:{value}")
        return value
       
    except Exception as e:
        print(f"解析出错: {e}")
        return None
    

def get_device_jiesuo():
    try:
        #isStatusBarKeyguard=true 未解锁，isStatusBarKeyguard=false 已解锁
        output_str =  execute(' dumpsys window | findstr "isStatusBarKeyguard" ')
        match = re.search(r'isStatusBarKeyguard=(\S+)', output_str)
        if match:
            print(f"显示解锁状态:{match.group(1)}")
            return match.group(1)
        else:
            return None
       
    except Exception as e:
        print(f"解析出错: {e}")
        return None 

# if __name__ == '__main__':
    
#     battery_level = get_device_battery_level()
#     print(f"获取电量信息: {battery_level}%")
    
    
    
