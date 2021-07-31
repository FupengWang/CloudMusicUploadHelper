import getpass
import time

import pyncm
import qrcode
from pyncm import GetCurrentSession, LoadSessionFromString
from pyncm.apis.login import GetCurrentLoginStatus, WriteLoginInfo

SESSION_FILE = "ncm_cloud.key"


def login(debug=False):
    """
    提供两种登陆方式: 手机+密码 , 二维码
    Pycharm下不能正常使用getpass
    所以建议调试时传入debug为True使用input读入密码
    :param debug:
    :return:
    """
    try:
        with open(SESSION_FILE) as K:
            pyncm.SetCurrentSession(LoadSessionFromString(K.read()))
            print("读取登录信息成功:[ %s ]" % pyncm.GetCurrentSession().login_info['content']['profile']['nickname'], "已登录")
            return True
    except FileNotFoundError:
        print("未能成功读取登录信息\n请选择登陆方式:\n[1]手机号+密码登录  [2]二维码登录")
        loginType = int(input())
        if loginType == 1:
            phoneNumber = input('手机 >>>')
            if debug:
                password = input('密码 >>>')
            else:
                password = getpass.getpass('密码 >>>')
            try:
                pyncm.login.LoginViaCellphone(phoneNumber, password)
                WriteLoginInfo(GetCurrentLoginStatus())
            except:
                print("出现异常, 请检查账号密码后重试! ")
                return False

        elif loginType == 2:
            def dot_thingy():
                while True:
                    s = list('   ')
                    while s.count('.') < len(s):
                        s[s.count('.')] = '.'
                        yield ''.join(s)

            dot = dot_thingy()
            uuid = pyncm.login.LoginQrcodeUnikey()['unikey']
            url = f'https://music.163.com/login?codekey={uuid}'
            IMG = qrcode.make(url)
            IMG.show()
            print('[-] UUID:', uuid)
            while True:
                rsp = pyncm.login.LoginQrcodeCheck(uuid)
                if rsp['code'] == 803 or rsp['code'] == 800: break
                message = f"[!] {rsp['code']} -- {rsp['message']}"
                print(message, next(dot), end='\r')
                time.sleep(1)
            WriteLoginInfo(GetCurrentLoginStatus())
        else:
            exit()

    if pyncm.login.GetCurrentLoginStatus()['code'] == 200:
        with open(SESSION_FILE, 'w+') as K:
            K.write(pyncm.DumpSessionAsString(GetCurrentSession()))
        print('成功登录并保存了登录信息:', pyncm.GetCurrentSession().login_info['content']['profile']['nickname'], '已登录',
              f'\n请不要删除当前目录下的"{SESSION_FILE}"文件, 这是登陆凭证!')
        return True
    else:
        print("未能成功登录! 请检查")
        return False
