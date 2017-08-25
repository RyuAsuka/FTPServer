# coding:utf-8
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from conf import setting
import logger


SERVER_IP = '192.168.0.177'
SERVER_PORT = 2121


def get_user(user_file):
    user_list = []
    with open(user_file) as f:
        for line in f:
            print(len(line.split()))
            if not line.startswith('#') and line:
                if len(line.split()) == 4:
                    user_list.append(line.split())
                else:
                    print('Wrong config of user.conf')
    return user_list


def ftp_server():
    authorizer = DummyAuthorizer()
    user_list = get_user('conf\\user.conf')
    for user in user_list:
        name, password, permit, homedir = user
        try:
            authorizer.add_user(name, password, homedir, perm=permit)
        except Exception as e:
            print(e)

    if setting.enable_anonymous == 'on':
        authorizer.add_anonymous('D:\\Home\\')

    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = setting.max_download
    dtp_handler.write_limit = setting.max_upload

    handler = FTPHandler
    handler.authorizer = authorizer

    if setting.enable_logging == 'on':
        logger.config_logger()

    handler.banner = setting.welcome_msg

    handler.passive_ports = range(setting.passive_ports[0], setting.passive_ports[1])

    server = FTPServer((SERVER_IP, SERVER_PORT), handler)
    server.max_cons = setting.max_cons
    server.max_cons_per_ip = setting.max_per_ip

    server.serve_forever()

if __name__ == '__main__':
    ftp_server()
