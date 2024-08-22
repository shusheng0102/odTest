import os
import sys
import warnings

warnings.filterwarnings('ignore')

try:
    import imp
except ImportError:

    def imp_is_frozen():  # python > 3 that has no imp lib already
        return hasattr(sys._MEIPASS)

else:

    def imp_is_frozen():
        return imp.is_frozen('__main__')

finally:
    warnings.filterwarnings('default')


def is_frozen():
    return (
        hasattr(sys, "frozen") or  # new py2exe
        hasattr(sys, "importers") or  # old py2exe
        imp_is_frozen()
    )


if is_frozen():
    ROOTDIR = os.path.normpath(os.path.abspath(os.path.dirname(sys.executable)))
    PROJECTDIR = ROOTDIR
else:
    ROOTDIR = os.path.normpath(os.path.abspath(os.path.join(__file__, '..', '..')))
    PROJECTDIR = os.path.join(ROOTDIR, 'wordson')


if __name__ == '__main__':
    print('root={}'.format(ROOTDIR))
    print('project={}'.format(PROJECTDIR))
