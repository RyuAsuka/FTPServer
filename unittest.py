import filehelper
import os
import time


if __name__ == '__main__':
    test_string = 'download "Landing action yeah" "program files"'
    splited = test_string.split()
    retVal = []
    print(splited)
    state = 0
    i = -1
    j = -1
    for word in splited:
        if state == 0:
            if '"' in word:
                i = splited.index(word)
                state = 1
            else:
                retVal.append(word)
        elif state == 1:
            if '"' in word:
                j = splited.index(word)
                print(i, j)
                st = ''
                for k in range(i, j+1):
                    if k < j+1:
                        st += splited[k] + ' '
                    else:
                        st += splited[k]

                retVal.append(st)
                state = 0
    print(retVal)
