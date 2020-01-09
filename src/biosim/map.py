class Cell:
    param = {}

    def __init__(self, map):
        self.map = map # Fjerne map?
        self.cell_pop = {}
    def propensity(self,relevant_fodder):
        pass

    def generate_fodder(self):
        pass


class Ocean(Cell):
    def __init__(self):
        self.relevant_fodder = None
        pass

class Mountain(Cell):
    def __init__(self):
        self.relevant_fodder = None
        pass

class Desert(Cell):
    # Herbivores kan ikke spise her, dvs at hvis de spiser er det feil
    def __init__(self):
        pass


class Savannah(Cell):
    param = {'f_max': 300, 'alpha': 0.3}

    def __init__(self):
        self.fodder_max = self.param['f_max']
        pass


class Jungle(Cell):
    param = {'f_max': 800, 'alpha': 0}

    def __init__(self):
        self.fodder_max = self.param["f_max"]
        pass


# Må kanskje tenke på at hver CELLE er en type og ikke området?