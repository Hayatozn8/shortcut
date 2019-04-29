import pandas as pd
from .. import pathOp

class CSVReadear(object):
    """
    CSV文件读取器

    :Args:
    - path 文件路径
    - sep 列分割符
    - header_rowno header的行号。默认为`0`，即第一行。`None`,不适用header
    """
    def __init__(self, path, sep=',', header_rowno=0, 
        engine='python', dtype=None, encoding='utf-8'
    ):
        self.path = path
        self.sep = sep
        self.header_rowno = header_rowno
        self.engine = engine
        self.dtype = dtype
        self.encoding = encoding

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, v):
        self._path = v

    @property
    def sep(self):
        return self._sep
    
    @sep.setter
    def sep(self, v):
        self._sep = v
 
    @property
    def header_rowno(self):
        return self._pd_param_header

    @header_rowno.setter
    def header_rowno(self, v):
        if v is None or isinstance(v, int):
            self._pd_param_header = v
        else:
            self._pd_param_header = 0

    @property
    def engine(self):
        return self._pd_param_engine
    
    @engine.setter
    def engine(self, v):
        if not v in ('python', 'c'):
            v = 'python'
        self._pd_param_engine = v

    @property
    def dtype(self):
        return self._pd_param_dtype
    
    @dtype.setter
    def dtype(self, v):
        self._pd_param_dtype = v

    @property
    def encoding(self):
        return self._pd_param_encoding

    @encoding.setter
    def encoding(self, v):
        self._pd_param_encoding = v

    def all(self):
        if not pathOp.isExists(self.path):
            raise Exception(f'文件不存在\npath={self.path}')
        elif not pathOp.isFile(self.path):
            raise Exception(f'不是一个有效的文件目录\npath={self.path}')
        
        return pd.read_csv(
            self.path, encoding=self.encoding, engine=self.engine,
            header=self.header_rowno, sep=self.sep, dtype=self.dtype
        )
