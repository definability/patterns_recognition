import tests.classes.semiring
import tests.classes.graph
import tests.classes.solver
import tests.classes.image

test_cases = sum([semiring.test_cases, graph.test_cases, solver.test_cases,
                  image.test_cases], [])

