import semiring
import graph
import solver
import image

test_cases = sum([semiring.test_cases, graph.test_cases, solver.test_cases,
                  image.test_cases], [])

