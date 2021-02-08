

"""
    自定义的错误类

"""
class EmptyError(Exception):
    def __init__(self):
        Exception.__init__()

    def __str__(self):
        return repr('代理池已经满了')