import tests.classes.semiring
import tests.classes.graph
import tests.classes.solver
import tests.classes.image
import tests.classes.random

test_cases = sum([semiring.test_cases, graph.test_cases, solver.test_cases,
                  image.test_cases, random.test_cases], [])

