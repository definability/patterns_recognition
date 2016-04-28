neighbourhoods = {}

def generate_layer(r):
    left = [(lambda x, y: (x-r, y-r+i)) for i in xrange(2*r+1)]
    right = [(lambda x, y: (x+r, y-r+i)) for i in xrange(2*r+1)]
    top = [(lambda x, y: (x-r+1+i, y+r)) for i in xrange(2*r-1)]
    bottom = [(lambda x, y: (x-r+1+i, y-r)) for i in xrange(2*r-1)]
    #x, y = 0, 0
    #left = [((x-r, y-r+i)) for i in xrange(2*r+1)]
    #right = [((x+r, y-r+i)) for i in xrange(2*r+1)]
    #top = [((x-r+1+i, y+r)) for i in xrange(2*r-1)]
    #bottom = [((x-r+1+i, y-r)) for i in xrange(2*r-1)]
    #print left+top+right+bottom
    return left+right+top+bottom

neighbourhoods[0] = [lambda x, y: (x+1, y), lambda x, y: (x, y+1)]
neighbourhoods[1] = neighbourhoods[0] + \
                    [lambda x, y: (x-1, y), lambda x, y: (x, y-1)]
neighbourhoods[2] = neighbourhoods[1] + \
                    [lambda x, y: (x-1, y-1), lambda x, y: (x+1, y+1),
                     lambda x, y: (x-1, y+1), lambda x, y: (x+1, y-1)]
neighbourhoods[3] = neighbourhoods[2] + generate_layer(2)

for i in xrange(4, 50):
    neighbourhoods[i] = neighbourhoods[i-1] + generate_layer(i-1)

