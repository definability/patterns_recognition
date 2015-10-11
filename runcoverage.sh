coverage run -m unittest tests.classes.semiring.SemiringBasicProperties
mv .coverage .coverage.SemiringBasicProperties
coverage run -m unittest tests.classes.graph.GraphBasicProperties
mv .coverage .coverage.GraphBasicProperties
python -m unittest tests.classes.solver.DynamicProgrammingBasicProperties
mv .coverage .coverage.DynamicProgramming
coverage combine
coverage report --show-missing

