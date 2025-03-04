电脑端通过Python脚本控制手机实现上下班打卡

- 说明
- dkService ：主服务
- dkWinClient: 生成windows client
- localBatteryLevel：查看手机电量、检查锁屏及解锁
- localdk：打卡步骤逻辑
- localLog：生成本地日志文件


** 其它
- Test、ico后缀、spec后缀、build dist是打包exe时自动生成可删除

** 升级玩法2种
- 1. 将Python 文件在window的任务计划程序自动执行
- 2. 手机端安装termux，执行脚本 


> pyinstaller --onefile --windowed --icon icondk.ico  dkWinClient.py