import re
import localdk as dk
import localBatteryLevel as dk2
import uiautomator2 as u2


def get_device_status():

    d = u2.connect('UYT5T18319017153')
    
    package_name = 'com.tencent.wework'  
    activity_name = 'com.tencent.wework.launch.LaunchSplashActivity' 
    d.app_start(package_name, activity_name,stop=True)
    d.click_post_delay = 3

    # 打卡
    button_text = '工作台'
    # 查找并点击按钮
    if d(text=button_text).exists:
        d(text=button_text).click()

    # 点击打卡
    button_text = '打卡'
    # 查找并点击按钮
    if d(text=button_text).exists:
        d(text=button_text).click()

    # 点击下班打卡
    d.click_post_delay = 10
    button_text = '下班打卡'
    # 查找并点击按钮
    if d(text=button_text).exists:
        d(text=button_text).click()

    # 取消
    d.click_post_delay = 5
    button_text = '取消'
    # 查找并点击按钮
    if d(text=button_text).exists:
        d(text=button_text).click()

    # 关闭
    d.click_post_delay = 10
    d.app_stop(package_name)
    
if __name__ == '__main__':   
    dk.unlockScreen()
    # result = get_device_status()
    # print(f"获取信息:{result}")
    # output_str = dk2.get_device_jiesuo()
    # print(f"获取信息:{output_str}")
    