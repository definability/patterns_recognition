from unittest import defaultTestLoader
import classes

test_cases = classes.test_cases

tests = [defaultTestLoader.loadTestsFromTestCase(test) for test in test_cases]

