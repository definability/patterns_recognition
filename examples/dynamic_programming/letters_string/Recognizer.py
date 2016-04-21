def img_to_matrix(img, band=0, inverse=False):
    matrix = []
    data = list(img.getdata())
    for offset in range(img.size[0]):
        matrix.append([abs((255*inverse) - x[band])
                       for x in data[offset::img.size[0]]])
    return matrix


def get_patterns_matrices(patterns):
    patterns_matrices = {}
    for p in patterns:
        patterns_matrices[p] = img_to_matrix(patterns[p], 3, True)
    return patterns_matrices


class Recognizer:


    def __init__(self, image, patterns, probabilities):
        self.image = image
        self.patterns = patterns
        self.probabilities = probabilities

        self.image_matrix = img_to_matrix(self.image)
        self.patterns_matrices = get_patterns_matrices(self.patterns)


    def get_image_fragment(self, offset, width):
        return self.image_matrix[offset:offset+width]


    def gather_penalties(self, domains, offset, add, zero, one):
        if offset <= 0:
            return one
        return reduce(add, [v for v in domains[offset].values()], zero)


    def fit_pattern(self, offset, key, add, mul, zero, one, get_penalty):
        return get_penalty(
                self.get_image_fragment(offset, self.patterns[key].size[0]),
                self.patterns_matrices[key], self.probabilities[key])


    def process_domain(self, domains, domain_offset, add, mul, zero, one, get_penalty):
        domain = {}
        for key, pattern in self.patterns.iteritems():
            offset = domain_offset - pattern.size[0]
            if offset < 0:
                penalty = zero
                continue
            domain[key] = mul(
                    self.fit_pattern(offset, key, add, mul, zero, one,
                                     get_penalty),
                    self.gather_penalties(domains, offset, add, zero, one))
        return domain


    def calculate(self, add, mul, zero, one, get_penalty):
        domains = [{} for i in range(self.image.size[0]+1)]
        for i, domain in enumerate(domains):
            domains[i] = self.process_domain(domains, i, add, mul, zero, one,
                                             get_penalty)

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

