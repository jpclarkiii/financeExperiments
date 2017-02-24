import os
import logging

LOGDIR=os.getenv('LOGDIR')
logFN="/".join([LOGDIR,'fundamentals.log'])
logging.basicConfig(filename=logFN, level=logging.DEBUG,
                    format='%(levelname)s:%(asctime)s %(message)s')


class FundamentalsReader(object):
    def __init__(self, debug=False):
        FDIR=os.getenv('FDIR')
        assert FDIR is not None

        dataDir = "/".join([FDIR, "data"])

    def read(self):
        pass

if __name__ == '__main__':
    print "Running download of fundamentals"
    logging.debug("Running Download of Fundamentals")
