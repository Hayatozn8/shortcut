import imghdr
from PIL import Image
from .. import pathOp

#像素和磅值的转换比率
PIXEL_TO_POINT_RATIO = 0.75

@pathOp.path_normal
def imgPixelSize(path):
    """
    返回图片文件的像素大小

    :Args:
    - path 图片路径

    :Returns:
    - (width, height)
    """
    if pathOp.isExists(path) and isImg(path):
        im = Image.open(path)
        return im.size
    else:
        raise Exception(f'图片文件不存在\nimg path = {path}')

@pathOp.path_normal
def imgPointSize(path):
    """
    返回图片文件的磅值大小

    :Args:
    - path 图片路径

    :Returns:
    - (width, height)
    """
    w, h = imgPixelSize(path)
    return (w*PIXEL_TO_POINT_RATIO, h*PIXEL_TO_POINT_RATIO)

@pathOp.path_normal
def isImg(path):
    """
    判断是否为图像文件

    如果不是文件，或不存在则返回`False`

    :Args:
    - path 文件路径

    :Return:
    - True/False
    """
    if not pathOp.isFile(path):
        return False
    
    return imghdr.what(path) is not None