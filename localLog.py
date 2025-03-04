import logging
import logging.config
from datetime import datetime, time

def getCurrentTimeStr ():
    return datetime.now().strftime('%Y%m%d%H')

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter':'standard',
            'filename': 'D:\\dkimg\\logs\\'+getCurrentTimeStr()+'.log',  # 绝对路径
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

logging.config.dictConfig(log_config)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# def log_():
#     print('log')
#     logger.info('这是一条调试信息（高级配置）')
    
def infoLog (info):
   
    try:
        logger.info(info)
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)

# if __name__ == '__main__':
#     log_()