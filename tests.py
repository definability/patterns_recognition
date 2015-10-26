import argparse
import cProfile, pstats, StringIO
from unittest import TestSuite, TextTestRunner

from tests import tests

pr = cProfile.Profile()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Testing arguments')
    parser.add_argument('-p', '--profile', help='Gather and show profiler information', action='store_true')
    args = parser.parse_args()

    if args.profile:
        pr.enable()

    TextTestRunner().run(TestSuite(tests))

    if args.profile:
        pr.disable()
        s = StringIO.StringIO()
        pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats()
        print s.getvalue()

