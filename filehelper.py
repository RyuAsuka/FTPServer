import os
import time


def gen_file_mode(file):
    flag_isdir = '-'
    flag_file = ''
    file_mode = oct(os.stat(file).st_mode)
    if len(file_mode) == 8:
        flag_isdir = '-'
    elif len(file_mode) == 7:
        flag_isdir = 'd'
    for m in range(-3, 0):
        flag_file += gen_mode_string(file_mode[m])
    return flag_isdir + flag_file


def gen_mode_string(file_mode_number):
    flag_file = ''
    binary = bin(int(file_mode_number))
    if binary[-1] == '1':
        flag_file += 'x'
    else:
        flag_file += '-'
    if binary[-2] == '1':
        flag_file += 'w'
    else:
        flag_file += '-'
    if binary[-3] == '1':
        flag_file += 'r'
    else:
        flag_file += '-'
    return flag_file[::-1]


def lslocal(directory):
    file_list = os.listdir(directory)
    print('Mode      \tLastWriteTime   \tSize    \tFileName')
    print('----------\t----------------\t--------\t--------')
    for file in file_list:
        filemode = gen_file_mode(directory + file)
        if filemode[0] == 'd':
            file_size = ''
        else:
            file_size = os.stat(directory + file).st_size
        print(filemode + '\t' + time.strftime('%Y/%m/%d %H:%M', time.localtime(os.stat(directory + file).st_mtime)) +
              '\t' + str(file_size) + '\t\t' + file)


def dir_is_exist(directory):
    target = directory.split('\\')[-1]
    try:
        file_list = os.listdir(directory + '\\..')
    except FileNotFoundError:
        return False
    if target in file_list:
        return True
    else:
        return False


def split_command(command):
    split_string = command.split()
    ret_val = []
    state = 0
    i = -1
    for word in split_string:
        if state == 0:
            if '"' in word:
                i = split_string.index(word)
                state = 1
            else:
                ret_val.append(word)
        elif state == 1:
            if '"' in word:
                j = split_string.index(word)
                st = ''
                for k in range(i, j + 1):
                    if k < j + 1:
                        st += split_string[k] + ' '
                    else:
                        st += split_string[k]

                ret_val.append(st)
                state = 0
    return ret_val
