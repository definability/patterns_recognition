from classes.image import MatrixPointer
from classes.solver import EnergyMinimization


def process_image(model, raw, mask):
    return ([], [])


def build_problem(model_image, raw_image, model_image_mask=None):
    if model_image_mask is None:
        model_image_mask = [True] * len(model_image.getdata())
    model = MatrixPointer(list(model_image.getdata()),
                         (model_image.size[0], model_image.size[1]))
    mask  = MatrixPointer(model_image_mask,
                         (model_image.size[0], model_image.size[1]))
    raw   = MatrixPointer(list(raw_image.getdata()),
                         (raw_image.size[0], raw_image.size[1]))
    vertices, edges = process_image(model, raw, model_image_mask)
    problem = EnergyMinimization(vertices, edges)
    return problem

