import logging
from wordson.bashlog import getlogger
from wordson.__main__ import main

if __name__ == "__main__":
    getlogger("wordson", logging.DEBUG)
    main()
