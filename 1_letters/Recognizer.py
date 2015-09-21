def get_penalty(image1, image2):
    image1_data = list(image1.getdata())
    image2_data = list(image2.getdata())
    result = sum((image1_data[i][3] - image2_data[i][3])**2 for i in range(len(image1_data)))
    return result

class Recognizer:

    def __init__(self, patterns, image):
        self.patterns = patterns
        self.image = image

    def get_penalty(self, pattern, offset):
        part_data = list(self.image.crop((offset, 0, offset + pattern.size[0], pattern.size[1])).getdata())
        pattern_data = list(pattern.getdata())
        result = sum((part_data[i][0] - (255-pattern_data[i][3]))**2 for i in range(len(part_data)))
        return result

    def calculate(self, add, mul, zero):
        domains = [dict() for i in range(self.image.size[0]+1)]
        for i, domain in enumerate(domains):
            for key in self.patterns:
                value = self.patterns[key]
                if value.size[0] > i:
                    domain[key] = zero
                elif value.size[0] == i:
                    domain[key] = self.get_penalty(value, 0)
                else:
                    domain[key] = mul(self.get_penalty(value, i-value.size[0]), reduce(add, [v for v in domains[i-value.size[0]].values()], zero))
        return (domains, reduce(add, [v for v in domains[len(domains)-1].values()], zero))

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
