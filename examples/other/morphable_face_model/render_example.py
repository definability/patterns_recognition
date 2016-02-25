from load_model import *
from render_picture import *


model = load_model()

coorinates = model['shapeMU']
vertices = coorinates.reshape(coorinates.shape[0]/3, 3)

workflow(vertices).show()

