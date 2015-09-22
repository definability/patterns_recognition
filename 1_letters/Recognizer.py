def img_to_matrix(img, band=0, inverse=False):
    matrix = []
    data = list(img.getdata())
    for offset in range(img.size[0]):
        matrix.append([x[band]^(255*inverse) for x in data[offset::img.size[0]]])
    return matrix

class Recognizer:

    def __init__(self, patterns, image):
        self.patterns = patterns
        self.image = image
        self.image_matrix = img_to_matrix(self.image)
        self.patterns_matrices = {}
        for p in self.patterns:
            self.patterns_matrices[p] = img_to_matrix(self.patterns[p], 3, True)
        self.fragments = {}

    def get_penalty(self, pattern, offset, zero):
        if offset < 0:
            return zero
        pattern_data = self.patterns_matrices[pattern]
        image_data = self.image_matrix[offset:offset+self.patterns[pattern].size[0]]
        result = 0
        for xv, kv in zip(image_data, pattern_data):
            for x, k in zip(xv, kv):
                result += (x-k)**2
        return result

    def gather_penalties(self, domains, offset, add, zero, one):
        if offset <= 0:
            return one
        return reduce(add, [v for v in domains[offset].values()], zero)


    def calculate(self, add, mul, zero, one):
        domains = [dict() for i in range(self.image.size[0]+1)]
        for i, domain in enumerate(domains):
            for key, pattern in self.patterns.iteritems():
                offset = i - pattern.size[0]
                penalty = self.get_penalty(key, offset, zero)
                penalties = self.gather_penalties(domains, offset, add, zero, one)
                domain[key] = mul(penalty, penalties)
        penalties = self.gather_penalties(domains, len(domains)-1, add, zero, one)
        return (domains, penalties)

    def argmin(self, obj):
        result = obj.keys()[0]
        for key in obj:
            if obj[key] < obj[result]:
                result = key
        return result

    def find_path(self, domains):
        i = len(domains)-1
        result = []
        while i > 0:
            result.append(self.argmin(domains[i]))
            i -= self.patterns[self.argmin(domains[i])].size[0]
        return result[::-1]
