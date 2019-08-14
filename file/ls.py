import os, re, collections, functools
import common

PARAM_MATCH = r'[^ltr]'

ILLEGAL_OPS_MSG = '''
ls: illegal option -- {0}\n
usage: ls([file ...] [-ABCFGHLOPRSTUWabcdefghiklmnopqrstuwx1])
'''

LsInfo = collections.namedtuple('LsInfo', ['uid', 'gid', 'size', 'time', 'path'])
LsSampleInfo = collections.namedtuple('LsSampleInfo', ['time', 'path'])

def default_ops():
    return {
        't':False,
        'l':False,
        'r':False,
        'm':False
    }

import functools
import getopt
def get_opts(shortopts, longopts = []):
    def opts_decorator(func):
        @functools.wraps(func)
        def opts_wapper(*args):
            args
            opts, args = getopt.getopt(args, shortopts, longopts)
            return func(opts, args)
        return opts_wapper
    return opts_decorator
    

def ls2(opts, args):
    """
    ls('-aa', file)
    ls('-aa')
    ls()
    ls(file)

    以`-`开头的文件可以：1 cmd -xxx -- -filename; 2 cmd -xxx ./-filename
    """
    if len(params) == 0:
        #没有任何参数时，默认使用当前工作路径
        return handle_no_opts(os.getcwd())
    elif params[0].startswith('-'):
        #第一个参数是以'-'开始时，默认为指令的参数部分
        argvs = re.split(r'\s*', params[0])
        
        if len(params) > 1:
            files = params[1:]
        else:
            #如果没有指定[file...]，默认使用当前的工作路径
            files = os.getcwd()
    else:
        #所有参数全部是路径
        return handle_no_opts(*params)



def handle_no_opts(*files):
    result = None
    if len(files) == 1:
        if not common.isexist(f):
            # 如果该路径不存在，exception
            raise Exception('ls: {0}: No such file or directory'.format(f))

        if common.isdir(f):
            result=os.listdir(f)
        else:
            #如果该路径不是目录，则直接添加到result中
            result=[f]
    else:
        result = []
        for f in files:
            if not common.isexist(f):
                # 如果该路径不存在，exception
                raise Exception('ls: {0}: No such file or directory'.format(f))

            if common.isdir(f):
                result.append(os.listdir(f))
            else:
                #如果该路径不是目录，则直接添加到result中
                result.append([f])
    
    return result
            
        


def ls(file, options=None, time=None):
    """
    linux command: ls
    :Args:
    - file 路径
    - options 
    - time 列出文件的时间(`mtime`,`atime`,`ctime`)，默认显示的是`mtime`
    """
    if options is None:
       result = os.listdir(file)
       result.sort(key=str.lower)
       return result
    else:
        illegal_ops = re.findall(PARAM_MATCH, options)
        if len(illegal_ops) > 0:
            raise Exception(ILLEGAL_OPS_MSG.format(illegal_ops))

        ops = default_ops()
        for p in set(options):
            ops[p] = True
        
        result = []
        if ops['l']:
            for content in os.listdir(file):
                content_stat = os.stat(os.path.join(file, content))
                result.append(
                    LsInfo(
                        content_stat.st_uid,
                        content_stat.st_gid,
                        content_stat.st_size,
                        getattr(content_stat, f'st_{time or "mtime"}'),
                        content
                    )
                )
        elif ops['t']:
            for content in os.listdir(file):
                content_stat = os.stat(os.path.join(file, content))
                result.append(
                    LsSampleInfo(
                        getattr(content_stat, f'st_{time or "mtime"}'),
                        content
                    )
                )
        else:
            result = os.listdir(file)

        # 对结果进行排序
        if ops['t']:
            result.sort(key=lambda x:x.time, reverse=True)
        else:
            result.sort(key=lambda x:x[-1].lower())
        
        # r 以文件名反序排列并输出目录内容列表
        if ops['r']:
            result.reverse()
        
        if ops['l'] == False and ops['t'] == True:
            result = list(map(lambda x:x[-1], result))
        
        return result

# def ls(file, options=None, time=None):
#     """
#     linux command: ls
#     :Args:
#     - file 路径
#     - options 
#     - time 列出文件的时间(`mtime`,`atime`,`ctime`)，默认显示的是`mtime`
#     """
#     if options is None:
#        result = os.listdir(file)
#        result.sort(key=str.lower)
#        return result
#     else:
#         illegal_ops = re.findall(PARAM_MATCH, options)
#         if len(illegal_ops) > 0:
#             raise Exception(ILLEGAL_OPS_MSG.format(illegal_ops))

#         ops = default_ops()
#         for p in set(options):
#             ops[p] = True
        
#         result = []
#         if ops['l']:
#             for content in os.listdir(file):
#                 content_stat = os.stat(os.path.join(file, content))
#                 result.append(
#                     LsInfo(
#                         content_stat.st_uid,
#                         content_stat.st_gid,
#                         content_stat.st_size,
#                         getattr(content_stat, f'st_{time or "mtime"}'),
#                         content
#                     )
#                 )
#         elif ops['t']:
#             for content in os.listdir(file):
#                 content_stat = os.stat(os.path.join(file, content))
#                 result.append(
#                     LsSampleInfo(
#                         getattr(content_stat, f'st_{time or "mtime"}'),
#                         content
#                     )
#                 )
#         else:
#             result = os.listdir(file)

#         # 对结果进行排序
#         if ops['t']:
#             result.sort(key=lambda x:x.time, reverse=True)
#         else:
#             result.sort(key=lambda x:x[-1].lower())
        
#         # r 以文件名反序排列并输出目录内容列表
#         if ops['r']:
#             result.reverse()
        
#         if ops['l'] == False and ops['t'] == True:
#             result = list(map(lambda x:x[-1], result))
        
#         return result
