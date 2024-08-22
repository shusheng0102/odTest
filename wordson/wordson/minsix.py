import sys
# get version
py3 = (sys.version_info[0] >= 3)
py2 = (not py3)

# open function
if py2:
    import codecs
    import warnings
    def open(file, mode='r', buffering=-1, encoding=None,
             errors=None, newline=None, closefd=True, opener=None):
        if newline is not None:
            warnings.warn('newline is not supported in py2')
        if not closefd:
            warnings.warn('closefd is not supported in py2')
        if opener is not None:
            warnings.warn('opener is not supported in py2')
        return codecs.open(filename=file, mode=mode, encoding=encoding,
                    errors=errors, buffering=buffering)
else:
    open = open     # for import

# input function
if py2:
    input = raw_input
else:
    input = input    # for import

try:
    callable    # py3, 3.1
except NameError:
    def callable(object):
        return hasattr(object, '__call__')
else:
    callable = callable    # for import


try:
    Str = basestring
except NameError:
    Str = str
