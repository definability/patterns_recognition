from unittest import TestSuite, TextTestRunner
from tests import tests


if __name__ == '__main__':
    TextTestRunner().run(TestSuite(tests))

