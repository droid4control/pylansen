class ENAPIException(BaseException):
    """ ENAPIException """

class ENAPILenException(ENAPIException):
    """ ENAPILenException """

class ENAPICrcErrorException(ENAPIException):
    """ Frame CRC error """

class ENAPICommandTypeNotImplementedException(ENAPIException):
    """ CommandType not implemented """
