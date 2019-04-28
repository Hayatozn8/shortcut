import json
from .. import pathOp

@pathOp.path_normal
def json_save(path, data):
    """
    将数据保存为json文件。如果文件已经存在，则将文件内容清空后写入

    :Args:
    - path 保存的文件路径
    """
    with open(path, 'w') as f:
        json.dump(data, f)

@pathOp.path_normal
def json_continue_save(path, data):
    """
    将数据保存为json文件。如果文件已经存在，则在文件的最后进行写入

    :Args:
    - path 保存的文件路径
    """
    with open(path, 'w+') as f:
        json.dump(data, f)