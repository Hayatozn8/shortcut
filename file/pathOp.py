import os, re
from functools import wraps
# from shortcut.sysop import SYS_NAME, PATH_SEQ
SYS_NAME = None #TODO
PATH_SEQ = '/' #TODO
# __all__ = [
#     'cwd',
#     'isFile',
#     'isAbs',
#     'isExists',
#     'isType',
#     'get_file_fullname',
#     'get_file_name',
#     'get_extension',
#     'getDir',
#     'getAbs',
#     'getPySpace',
#     'path_join'
#     'cut_ectension',
#     'get_files_fullname_from_dir',
#     'path_normal',
#     'walkdir_search_file',
#     'walkdir_get_file_path'
# ]

path_seq_normalizer = None
if SYS_NAME == 'Windows':
    def _windows_path_seq_normalizer(path, normalizer=PATH_SEQ):
        """
        路径标准化

        如果path=None，自动转化为‘’

        :Args:
        - path 路径
        - normalizer 路径分割符

        :Returns:
        - normal_path 标准路径

        :Usage:
        ```python
        #1 
        pathA = 'C:\\\\Users\\\\user\\\\Desktop\\\\'
        pathB = _windows_path_seq_normalizer(pathA)
        # pathaB = 'C:\\Users\\user\\Desktop\\'

        #2
        pathA = None
        pathB = _windows_path_seq_normalizer(pathA)
        # pathaB = ''
        ```
        """
        if path is None:
            return ''
        else:
            return path.replace('/', normalizer).replace('\\\\', normalizer)

    path_seq_normalizer = _windows_path_seq_normalizer

else:
    def _othersys_path_seq_normalizer(path, normalizer=PATH_SEQ):
        if path is None:
            return ''
        else:
            return path.replace('\\', normalizer).replace('\\\\', normalizer)

    path_seq_normalizer = _othersys_path_seq_normalizer


def path_normal(func):
    """
    装饰器：路径标准化

    `第一参数必须使用路径`
    """
    @wraps(func)
    def wrapper(path, *args, **kwargs):
        normal_path = path_seq_normalizer(path)
        return func(normal_path, *args, **kwargs)
    return wrapper

def cwd():
    """
    返回当前的工作路径（绝对路径）
    """
    return path_seq_normalizer(os.getcwd())

@path_normal
def isFile(path, extension=None):
    """
    判断指定路径是否为文件(包含检查路径是否存在)

    :Args:
    - path 路径
    - extension 文件后缀`（如txt，前面不加点号）`。 default=None， 文件检查后，继续检查文件的扩展名，如果是None则跳过
    
    :Returns:
    - 检查结果 True/False

    :Usage:
    ```python
    ######使用绝对路径########
    #1
    pathA = 'C:/Users/user/Desktop'
    result = isFile(pathA)
    #result = False
    ```

    #2 文件[xxx.txt]存在
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    result = isFile(pathA)
    #result = True

    #3 文件[xxx.txt] 不存在
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    result = isFile(pathA)
    #result = False

    #4 特殊情况：文件[xxx]没有扩展名
    pathA = 'C:/Users/user/Desktop/xxx'
    result = isFile(pathA)
    #result = True

    #5 特殊情况：文件[xxx] 不存在
    pathA = 'C:/Users/user/Desktop/xxx'
    result = isFile(pathA)
    #result = False

    #########使用相对路径#########
    #1
    pathA = './user/Desktop'
    result = isFile(pathA)
    #result = False

    #2 文件[xxx.txt]存在
    pathA = './user/Desktop/xxx.txt'
    result = isFile(pathA)
    #result = True

    #3 文件[xxx.txt] 不存在
    pathA = './user/Desktop/xxx.txt'
    result = isFile(pathA)
    #result = False

    #4 特殊情况：文件[xxx]没有扩展名
    pathA = './user/Desktop/xxx'
    result = isFile(pathA)
    #result = True

    #5 特殊情况：文件[xxx] 不存在
    pathA = './user/Desktop/xxx'
    result = isFile(pathA)
    #result = False

    #########文件类型（扩展名）检查############
    #1 文件不存在
    pathA = './user/Desktop/xxx.txt'
    result = isFile(pathA, extension='txt')
    #result = True

    #1 文件不存在
    pathA = './user/Desktop/xxx.txt'
    result = isFile(pathA, extension='txt')
    #result = False
    """
    if os.path.isfile(path):
        if extension is None:
            return True
        else:
            #检查文件扩展名
            return isType(path, extension)
    else:
        return False

@path_normal
def isAbs(path):
    """
    检查路径是否为绝对路径(包含检查路径是否存在)

    :Args:
    - path 路径

    :Returns:
    - 检查结果 True/False
    """
    return os.path.isabs(path)

@path_normal
def isDir(path):
    """
    检查路径是否为目录(包含检查路径是否存在)

    :Args:
    - path 路径

    :Returns:
    - 检查结果 True/False

    :Usage:
    ```python
    ########## 使用绝对路径 且路径存在 ##########
    #1
    pathA = 'C:/Users/user/Desktop'
    result = isDir(pathA)
    #result = True

    #2
    pathA = 'C:/Users/user/Desktop/'
    result = isDir(pathA)
    #result = True

    #3
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    result = isDir(pathA)
    #result = False

    ########### 使用相对路径 且路径存在 ###############
    #1
    pathA = './user/Desktop'
    result = isDir(pathA)
    #result = True

    #2
    pathA = './user/Desktop/'
    result = isDir(pathA)
    #result = True

    #3
    pathA = './user/Desktop/xxx.txt'
    result = isDir(pathA)
    #result = False

    ########### 使用相对路径 且路径不存在 ###############
    #1
    pathA = './user/Desktop'
    result = isDir(pathA)
    #result = False

    #2
    pathA = './user/Desktop/'
    result = isDir(pathA)
    #result = False

    #3
    pathA = './user/Desktop/xxx.txt'
    result = isDir(pathA)
    #result = False
    ```
    """
    return os.path.isdir(path)

@path_normal
def isExists(path):
    """
    检查路径是否存在

    :Args:
    - path 路径

    :Returns:
    - 检查结果 True/False
    """
    return os.path.exists(path)

@path_normal
def isType(path, extension):
    """
    检查文件类型（文件扩展名）

    :Args:
    - path 路径
    - extension 扩展名

    :Returns:
    - 检查结果 True/False

    :Usage:
    ```python
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    result = isType(pathA, 'txt')
    #result = True
    ```
    """
    return Extension(path) == extension

@path_normal
def pJoin(main_path, *others):
    """
    路径连接

    :Args:
    - main_path 主路径
    - 子路径
    """
    #如果未输入子路径，则直接返回
    if len(others) == 0:
        return main_path
    else:
        #将子路径开始部分的[.]或[.\]或[./]或[\\]删除
        pattern = re.compile(r'^(\.)*(\\|/)*')
        others = map(lambda x: re.sub(pattern, '', path_seq_normalizer(x)), others)
        #将主路径与子路径进行连接
        return path_seq_normalizer(os.path.join(main_path, *others))

@path_normal
def cut_extension(path):
    """
    将路径中的文件扩展名删除

    :Args:
    - path 路径

    :Returns:
    ```python
    #######使用绝对路径#######
    #1
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    result = cut_extension(pathA)
    #result = 'C:/Users/user/Desktop/xxx'

    #2
    pathA = 'C:/Users/user/Desktop/xxx'
    result = cut_extension(pathA)
    #result = 'C:/Users/user/Desktop/xxx'

    #3
    pathA = 'C:/Users/user/Desktop/xxx/'
    result = cut_extension(pathA)
    #result = 'C:/Users/user/Desktop/xxx/'

    #######使用相对路径#######
    #1
    pathA = './user/Desktop/xxx.txt'
    result = cut_extension(pathA)
    #result = './user/Desktop/xxx'

    #2
    pathA = './user/Desktop/xxx'
    result = cut_extension(pathA)
    #result = './user/Desktop/xxx'

    #3
    pathA = './user/Desktop/xxx/'
    result = cut_extension(pathA)
    #result = './user/Desktop/xxx/'
    ```
    """
    #（路径，扩展名）
    # 'xxx/yy.txt' -->>> ('xxx/yy', '.txt')
    return os.path.splitext(path)[0]

@path_normal
def Extension(path):
    """
    从路径中获取扩展名，如果没有扩展名则返回[‘’]

    不对路径进行检查，直接获取

    :Args:
    - path 路径

    :Returns:
    - extension 文件的扩展名

    :Usage:
    ```python
    ########使用绝对路径###########
    #1
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    result = Extension(pathA)
    #result = 'txt'

    #2
    pathA = 'C:/Users/user/Desktop/xxx'
    result = Extension(pathA)
    #result = ''

    #3
    pathA = 'C:/Users/user/Desktop/'
    result = Extension(pathA)
    #result = ''

    ########使用相对路径###########
    #1
    pathA = './user/Desktop/xxx.txt'
    result = Extension(pathA)
    #result = 'txt'

    #2
    pathA = './user/Desktop/xxx'
    result = Extension(pathA)
    #result = ''

    #3
    pathA = 'C:/Users/user/Desktop/'
    result = Extension(pathA)
    #result = ''
    ```
    """
    #（路径，扩展名）
    # 'xxx/yy.txt' -->>> ('xxx/yy', '.txt')
    # 去掉[.]
    return os.path.splitext(path)[1][1:]

@path_normal
def Dir(path):
    """
    从路径中获取目录

    不对路径进行检查，直接获取

    :Args:
    - path 路径

    :Returns:
    - dir 文件目录

    :Usage:
    ```python
    #########使用绝对路径#########
    #1
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    d = Dir(pathA)
    #d = 'C:/Users/user/Desktop'

    #2
    pathA = 'C:/Users/user/Desktop/xxx'
    d = Dir(pathA)
    #d = 'C:/Users/user/Desktop'
    
    #3
    pathA = 'C:/Users/user/Desktop/'
    d = Dir(pathA)
    #d = 'C:/Users/user/Desktop'

    ##########使用相对路径##########
    #1
    pathA = './user/Desktop/xxx.txt'
    d = Dir(pathA)
    #d = './user/Desktop'

    #2
    pathA = './user/Desktop/xxx'
    d = Dir(pathA)
    #d = './user/Desktop'
    
    #3
    pathA = './user/Desktop/'
    d = Dir(pathA)
    #d = './user/Desktop'

    #4
    pathA = 'xxx.txt'
    d = Dir(pathA)
    #d = ''
    ```
    """
    return os.path.dirname(path)

@path_normal
def Abs(path):
    """
    返回绝对路径

    :Args:
    - path 路径

    :Returns:
    - abs 绝对路径
    """
    return os.path.abspath(path)

@path_normal
def PySpace(path):
    """
    将目录变为python代码空间（只适用于相对路径）

    路径包含扩展名时，将扩展名去除后进行变换

    :Args:
    - path 路径

    :Returns:
    - python src space (aa.bb.cc)

    :Usage:
    ```python
    pathA = './aaa/bb/cc.txt'
    result PySpace(pathA)
    #result = 'aaa.bb.cc'
    """
    temp = cut_extension(path)
    #替换路径分隔符 TODO
    space = temp.replace(PATH_SEQ, '.')
    #如果路径是：’./a/b‘的形式，将第一个[.]和[/]或[\]去掉
    pattern = re.compile(r'^\.*()')
    return re.sub(pattern, '', space)


@path_normal
def Basename(path):
    """
    从路径中获取文件全名（文件名.扩展名 或 最后一级目录名）

    不对路径进行检查，直接获取

    :Args:
    - path 路径

    :Returns:
    - 文件全名

    :Usage:
    ```python
    #1 文件名
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    result = Basename(pathA)
    #result = 'xxx.txt'

    #2 目录名
    pathA = 'C:/Users/user/Desktop/xxx'
    result = Basename(pathA)
    #result = 'xxx'

    #3 特殊情况
    pathA = 'C:/Users/user/Desktop/xxx/'
    result = Basename(pathA)
    #result = ''
    ```
    """
    # #TODO
    # #获取目录 
    # d = Dir(path)
    # #从路径中产出目录
    # return path.repalce(d+PATH_SEQ, '')

    # return path.split(PATH_SEQ)[-1]
    return os.path.basename(path)

@path_normal
def Simplename(path):
    """
    从路径中获取文件名（不包含扩展名）或最后一级目录名
    
    不对路径进行任何检查

    :Args:
    - path 路径

    :Returns:
    - file_name 文件名

    :Usage:
    ```python
    #1 文件名
    pathA = 'C:/Users/user/Desktop/xxx.txt'
    result = Simplename(pathA)
    #result = 'xxx'

    #2 最后一级目录名
    pathA = 'C:/Users/user/Desktop'
    result = Simplename(pathA)
    #result = 'Desktop'

    #3 特殊情况
    pathA = 'C:/Users/user/Desktop/'
    result = Simplename(pathA)
    #result = ''
    ```
    """
    #获取路径的文件/目录全名
    full_name = Basename(path)
    #删除扩展名
    # \..*$ 匹配文件/目录全名的结尾部分
    extension = re.compile(r'\..*$')
    return re.sub(extension, '', full_name)

@path_normal
def NameAndExtension(path):
    """
    获取文件的名称和扩展名

    不堆路径进行检查直接获取

    :Args:
    - path 路径
    """
    return Simplename(path), Extension(path)

@path_normal
def BasenameFromDir(d, extension=None):
    """
    从指定目录下获取文件名（不搜索子目录）。
    
    指定扩展名时，只获取指定类型文件的文件名

    :Args:
    - d 目录
    - extension 文件扩展名 
    """
    if isDir(d):
        files_name = os.listdir(d)

        if extension:
            return files_name
        else:
            return list(filter(lambda x: isType(x, extension), files_name))
    else:
        #如果目录不存在，返回空数组
        return []
        

@path_normal
# walkdir_get_file_path
def file_of_dir(dir, extension=None):
    """
    获取目录下的所有文件路径

    :Args:
    - dir 目录
    - extension 扩展名

    :Returns:
    - paths 所有文件的路径list
    """
    file_paths = []
    if extension:
        #优先遍历子目录
        for root, _, files_full_name in os.walk(dir, topdown=False):
            file_paths.extend(
                map(
                    lambda x:pJoin(root, x)
                    ,filter(lambda x:Extension(x) == extension, files_full_name)
                )
            )
    else:
        #优先遍历子目录
        for root, _, files_full_name in os.walk(dir, topdown=False):
            file_paths.extend(
                map(lambda x:pJoin(root, x), files_full_name)
            )

    return file_paths

@path_normal
def search_file(dir, fname, extension=None, level='a', all_walk=False):
    """
    从目录下的各子目录中检索文件，并返回文件的路径

    :Args:
    - dir 目录
    - fname 文件名
    - extension 扩展名
    - level a:==, b:like    , c==name, d:like name
    - all_walk default=False `False`检索到目标后立即返回, `True`全部子目录检索完毕后返回
    """
    # 如果不是一个有效目录，则返回空数组
    if not isDir(dir):
        return []

    # 生成比较方法    
    if extension:
        #同时比较扩展名
        if level == 'a':
            def _compare(target, bn):
                sn, ext = NameAndExtension(bn)
                return target==sn and extension==ext
        else:
            def _compare(target, bn):
                sn, ext = NameAndExtension(bn)
                return target in sn and extension==ext
    else:
        if level == 'a':
            def _compare(target, bn):
                return target == Simplename(bn)
        else:
            def _compare(target, bn):
                return target in Simplename(bn)
        

    #遍历这个目录并进行比较
    if all_walk:
        fps = []
        #全检索模式
        for root, _, basenames in os.walk(dir, topdown=False):
            for bn in basenames:
                if _compare(fname, bn):
                    fps.append(pJoin(root, bn))
        return fps
    else:
        for root, _, basenames in os.walk(dir, topdown=False):
            for bn in basenames:
                # 搜索到之后立刻返回
                if _compare(fname, bn):
                    return [pJoin(root, bn)]
                    
        #如果没有检索到直接返回空数组
        return []