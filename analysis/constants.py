from enum import Enum

class CryptoType(Enum):
    SYMMETRIC = 'symmetric'
    ASYMMETRIC = 'asymmetric'
    HASH = 'hash'

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

class HashingAlgo(Enum):
    SHA1 = 'sha-1'  # Match the values with what's in the CSV
    SHA224 = 'sha-224'
    SHA256 = 'sha-256'
    SHA384 = 'sha-384'
    SHA512 = 'sha-512'
    MD5 = 'md5'
    HMAC = 'hmac'

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
