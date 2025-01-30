from enum import Enum

class CryptoType(Enum):
    ASYMMETRIC = 'asymmetric'
    SYMMETRIC = 'symmetric'

class AsymmetricAlgo(Enum):
    RSA = 'rsa'
    DSA = 'dsa'
    ECC = 'ecc'
    DH = 'dh'

class SymmetricAlgo(Enum):
    AES = 'aes'
    DES = 'des'
    TRIPLE_DES = '3des'
    RC2 = 'rc2'
    RC4 = 'rc4'
    BLOWFISH = 'blowfish'

class MetricType(Enum):
    FILESIZE_TIME = 'filesize_time'
    KEYSIZE_TIME = 'keysize_time'

class VisualizationType(Enum):
    BAR = 'bar'
    LINE = 'line'

class BarChartType(Enum):
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'
    STACKED = 'stacked'
    GROUPED = 'grouped'
