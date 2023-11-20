# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

from util.sample import Util

import requests

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

def getURL(organization:str, project:str) -> str:
    return f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=7.0'

if __name__ == '__main__':
    # 起動引数の取得
    # args = sys.argv
    # args[0]はpythonのファイル名。
    # 実際の引数はargs[1]から。

    result = requests.get(
        getURL(
            ImportEnvKeyEnum.ORGANIZATION.value,
            ImportEnvKeyEnum.PROJECT.value),
        auth=('git', ImportEnvKeyEnum.Token.value)).json()
    
    logger.info(result)
    
    for repo in result['value']:
        print(repo['id'])
