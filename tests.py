from argparse import ArgumentParser
from cProfile import Profile
from pstats import Stats
from unittest import TestSuite, TextTestRunner

from tests import tests


if __name__ == '__main__':

    profile = None

    parser = ArgumentParser(description='Testing arguments')
    parser.add_argument('-p', '--profile',
            help='Gather and show profiler information', action='store_true')
    args = parser.parse_args()

    if args.profile:
        profile = Profile()
        profile.enable()

    TextTestRunner().run(TestSuite(tests))

    if args.profile:
        profile.disable()
        Stats(profile).sort_stats('cumulative').print_stats()

