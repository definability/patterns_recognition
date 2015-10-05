coverage run -m unittest tests.classes.semiring.SemiringMinPlusElement
mv .coverage .coverage.SemiringMinPlusElement
coverage combine
coverage report --show-missing
