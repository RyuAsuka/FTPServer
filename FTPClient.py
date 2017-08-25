# coding:utf-8

"""Simple Python FTP Client

Usage:
    python FTPClient.py <server_ip> [server_port]

Commands:
    ls <remote|local>                   List Files in current directory
    cd <remote|local> <dir>             Change Working directory
    upload <filename>                   Upload file from local directory to current remote directory
    download <filename> <localDir>      Download file from remote directory to
    md <remote|local> <DirName>         Make a new folder in current directory
    del <remote|local> <filename>       Delete a file in current remote directory
    deltree <remote|local> <DirName>    Delete a directory in current remote directory
    rename <remote|local> <old> <new>   Rename a file or a directory
    quit                                Quit FTP Client
"""
from ftplib import FTP
import sys
import os
import filehelper


prompt = '$'


class FTPClient(object):
    """
    FTP Client Class
    """
    def __init__(self):
        self.ftp = FTP()
        self.server_ip = ''
        self.server_port = 0
        self.pwd = ''
        self.pwd_local = os.getcwd()

    def cli_parse(self, argv):
        """
        Parse the CLI arguments
        :param argv: the list of arguments
        :return: None
        """
        argc = len(argv)
        server_port = 0
        server_ip = ''
        if argc < 2 or argc > 3:
            print(__doc__)
            return None
        elif argc == 2:
            server_ip = argv[1]
            server_port = 21
        elif argc == 3:
            server_ip = argv[1]
            server_port = int(argv[2])
        self.server_ip = server_ip
        self.server_port = server_port
        self.__create_client()

    def __create_client(self):
        """
        Create the client
        :return: None
        """
        ftp = self.ftp
        timeout = 600
        print('Server: ', self.server_ip + ':' + str(self.server_port))
        ftp.connect(self.server_ip, self.server_port, timeout=timeout)
        username = input('Username(Enter for anonymous): ')
        password = input('Password: ')

        ftp.login(user=username, passwd=password)
        ftp.encoding = 'GB18030'
        print(ftp.getwelcome())
        self.__run_client()

    def __run_client(self):
        """
        A infinity loop to run the FTP Client
        :return: None
        """
        self.pwd = self.ftp.pwd()
        while True:
            command = input('ftp://' + self.server_ip + ':' + str(self.server_port) + self.pwd + prompt + ' ')

            if command == 'quit' or command == 'exit':
                print('Bye')
                self.ftp.quit()
                break

            elif command == '':
                continue

            elif command.split()[0] == 'ls':
                if len(command.split()) != 2:
                    print('Argument error: ls <remote|local>')
                    continue
                else:
                    self.__list_file(command.split()[1])

            elif filehelper.split_command(command)[0] == 'cd':
                if len(command.split()) != 3:
                    print('Argument error: cd <remote|local> <directory>')
                    continue
                else:
                    self.__change_dir(filehelper.split_command(command)[1], filehelper.split_command(command)[2])

            elif filehelper.split_command(command)[0] == 'upload':
                remote_dir = filehelper.split_command(command)[1]
                local_dir = filehelper.split_command(command)[2]
                self.__upload(remote_dir, local_dir)

            elif command.split()[0] == 'download':
                remote_dir = filehelper.split_command(command)[1]
                local_dir = filehelper.split_command(command)[2]
                self.__download(remote_dir, local_dir)

            elif filehelper.split_command(command)[0] == 'md':
                if len(command.split()) != 3:
                    print('Argument error: md <remote|local> <dir_name>')
                    continue
                else:
                    self.__makedir(filehelper.split_command(command)[1], filehelper.split_command(command)[2])

            elif filehelper.split_command(command)[0] == 'del':
                if len(command.split()) != 3:
                    print('Argument error: del <remote|local> <filename>')
                    continue
                else:
                    self.__delete(filehelper.split_command(command)[1], filehelper.split_command(command)[2])

            elif filehelper.split_command(command)[0] == 'deltree':
                if len(command.split()) != 3:
                    print('Argument error: deltree <remote|local> <dir_name>')
                    continue
                else:
                    self.__deltree(filehelper.split_command(command)[1], filehelper.split_command(command)[2])

            elif filehelper.split_command(command)[0] == 'rename':
                if len(command.split()) != 4:
                    print('Argument error: rename <remote|local> <old_filename> <new_filename>')
                    continue
                else:
                    self.__rename(filehelper.split_command(command)[1], filehelper.split_command(command)[2],
                                  filehelper.split_command(command)[3])

            else:
                print(__doc__)
                continue

    def __list_file(self, arg):
        """
        list the file of current directory
        :param arg: remote OR local
        :return: None
        """
        if arg == 'remote':
            self.ftp.dir()
        elif arg == 'local':
            path = os.getcwd()
            print(path)
            filehelper.lslocal(path + '\\')
        else:
            return None

    def __change_dir(self, arg, directory):
        """
        Change the current directory to a new directory
        :param arg: remote OR local
        :param directory: the target directory
        :return: None
        """
        if arg == 'remote':
            self.ftp.cwd(dirname=directory)
            self.pwd = self.ftp.pwd()
        elif arg == 'local':
            os.chdir(directory)
            self.pwd_local = os.getcwd()
        else:
            return None

    def __upload(self, remote, local):
        """
        Upload the file or directory from local to remote
        :param remote: the target file or directory
        :param local: the local file or directory
        :return: None
        """
        buf_size = 1024
        if self.__is_dir(local, dir_type='local'):
            print('Enter directory: ', local)
            if not filehelper.dir_is_exist(remote):
                self.__makedir('remote', remote)
            self.__change_dir('remote', remote)
            self.__change_dir('local', local)
            for item in self.ftp.nlst():
                self.__upload(item, item)
            self.__change_dir('remote', '..')
            self.__change_dir('local', '..')
            print('Leave directory: ', local)
        else:
            fp = open(local, 'rb')
            self.ftp.storbinary('STOR ' + remote, fp, buf_size)
            print('Upload: ' + self.pwd_local + '\\' + local + ' -> ' + self.pwd + '/' + remote)
            fp.close()

    def __download(self, remote, local):
        """
        Download the file or directory from remote to local
        :param remote: the remote file or directory
        :param local: the local file or directory
        :return: None
        """
        buf_size = 1024
        if self.__is_dir(remote, dir_type='remote'):
            print('Enter directory: ', remote)
            if not filehelper.dir_is_exist(local):
                self.__makedir('local', local)
            self.__change_dir('local', local)
            self.__change_dir('remote', remote)
            for item in self.ftp.nlst():
                self.__download(item, item)
            self.__change_dir('remote', '..')
            self.__change_dir('local', '..')
            print('Leave directory: ', remote)
        else:
            fp = open(local, 'wb')
            self.ftp.retrbinary('RETR ' + remote, fp.write, buf_size)
            print('Download: ' + self.pwd + '/' + remote + ' -> ' + self.pwd_local + '\\' + local)
            fp.close()

    def __makedir(self, arg, dir_name):
        """
        Make a new directory on local or remote
        :param arg: remote OR local
        :param dir_name: The new directory name
        :return: None
        """
        if arg == 'remote':
            self.ftp.mkd(dir_name)
        elif arg == 'local':
            os.makedirs('./' + dir_name)
        else:
            return None

    def __delete(self, arg, filename):
        """
        Delete a file on local or remote
        :param arg: remote OR local
        :param filename: the name of file to delete
        :return:
        """
        if arg == 'remote':
            self.ftp.delete(filename)
        elif arg == 'local':
            os.remove(filename)
        else:
            return None

    def __deltree(self, arg, dir_name):
        """
        Delete a directory on local or remote
        :param arg: remote OR local
        :param dir_name: the name of directory to delete
        :return: None
        """
        if arg == 'remote':
            self.ftp.rmd(dir_name)
        elif arg == 'local':
            os.removedirs(dir_name)
        else:
            return None

    def __rename(self, arg, old_filename, new_filename):
        """
        Rename a file or directory
        :param arg: remote OR local
        :param old_filename: the old filename or directory name
        :param new_filename: the new filename or directory name
        :return:
        """
        if arg == 'remote':
            self.ftp.rename(old_filename, new_filename)
        elif arg == 'local':
            os.rename(old_filename, new_filename)
        else:
            return None

    def __is_dir(self, directory, dir_type):
        """
        To judge if an item in directory is a directory
        :param directory: the item name
        :param dir_type: remote OR local
        :return: A boolean value if the item in directory is a directory
        """
        all_dir_info = []
        dir_info = ''
        if dir_type == 'remote':
            self.ftp.retrlines('LIST', all_dir_info.append)
            for item in all_dir_info:
                if directory in item:
                    dir_info = item
                    break

            dir_arr = dir_info.split()
            if len(dir_arr) == 0:
                return False
            # print('dir_arr:', dir_arr)
            if len(dir_arr) != 0 and dir_arr[0][0] == 'd':
                return True
            else:
                return False
        elif dir_type == 'local':
            file_mode = filehelper.gen_file_mode(directory)
            if file_mode[0] == 'd':
                return True
            else:
                return False


if __name__ == '__main__':
    client = FTPClient()
    client.cli_parse(sys.argv)
