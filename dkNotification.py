from plyer import notification

def win_notification (args = None):
    notification.notify(
        title='电量提示',
        message=f'电量为：{0 if args is None else args} ，请充电' ,
        timeout=10  # 通知自动关闭的时间，单位为秒
    )