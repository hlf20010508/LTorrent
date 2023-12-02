from traceback import print_exc
from io import StringIO

class LoggerMustException(Exception):
    pass

class LoggerBase:
    def __init__(self, *args):
        pass

    def ERROR(self, *args):
        pass

    def WARNING(self, *args):
        pass

    def INFO(self, *args):
        pass

    def DEBUG(self, *args):
        pass

    def MUST(self, *args):
        raise LoggerMustException


class Logger(LoggerBase):
    def __init__(self):
        LoggerBase.__init__(self)
    
    def ERROR(self, *args):
        buffer = StringIO()
        print_exc(file=buffer)
        print("ERROR:", *args)
        print(buffer.getvalue())
    
    def WARNING(self, *args):
        print("WARNING:", *args)
        
    def INFO(self, *args):
        print("INFO:", *args)

    def DEBUG(self, *args):
        print("DEBUG:", *args)

    def MUST(self, *args):
        print(*args)
