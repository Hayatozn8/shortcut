from platform import uname

SYS_INFO = uname()
SYS_NAME = SYS_INFO[0]

if SYS_NAME == 'Windows':
    #路径分割符
    PATH_SEQ = '\\'

else:
    #路径分割符
    PATH_SEQ = '/'