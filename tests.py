import cProfile, pstats, StringIO
from unittest import TestSuite, TextTestRunner
from tests import tests

pr = cProfile.Profile()

if __name__ == '__main__':
    pr.enable()
    TextTestRunner().run(TestSuite(tests))
    pr.disable()
    s = StringIO.StringIO()
    pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats()
    print s.getvalue()

