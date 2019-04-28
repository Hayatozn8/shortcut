from . import pathOp
import shutil
import os

__all__ = [
    'copyWithMode', 'clearDir',
    'makeDir'
]
def copyWithMode(old, new):
    """
    文件拷贝

    :Args:
    - path 文件路径
    - copy_dir 拷贝的目标
    """
    # #文件检查
    # if not pathOp.isExists(path):
    #     raise Exception(f'文件不存在，文件拷贝操作终止\nfile path = {path}')
    # if not pathOp.isFile(path):
    #     raise Exception(f'文件不存在，文件拷贝操作终止\nfile path = {path}')
    # #目录检查
    # if not pathOp.isDir
    shutil.copy(old, new)

@pathOp.path_normal
def clearDir(dir):
    """
    清空目录。如果参数不是有效目录，则忽略

    :Args:
    - dir 目录
    """
    if not pathOp.isDir(dir):
        return
    
    #从最内层目录开始遍历并进行文件删除
    for root ,dirs, files in os.walk(dir, topdown=False):
        #先删除文件
        for fn in files:
            os.remove(os.path.join(root, fn))
        #再删除目录
        for d in dirs:
            os.rmdir(os.path.join(root, d))

@pathOp.path_normal
def makeDir(newDir, err_try_iter=True):
    """
    创建目录。
    
    如果目录存在则跳过

    如果创建失败，则尝试进行递归目录创建

    :Args:
    - newDir 需要创建的目录
    - err_try_iter default=True，创建失败时，是否进行执行递归目录创建
    """
    if not pathOp.isDir(newDir):
        try:
            os.mkdir(newDir)
        except Exception as e:
            if err_try_iter:
                os.makedirs(newDir)
            else:
                raise e

        