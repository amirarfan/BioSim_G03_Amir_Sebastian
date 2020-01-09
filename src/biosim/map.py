class Atlas:
    param = {}

    def __init__(self, map):
        self.map = map # Fjerne map?

        # Legge til en dictionary som sier hva slags og hvor mange dyr det er i hver celle?

    def generate_fodder(self):
        pass


class OceanMountain(Atlas):
    def __init__(self):
        pass


class Desert(Atlas):
    # Herbivores kan ikke spise her, dvs at hvis de spiser er det feil
    def __init__(self):
        pass


class Savannah(Atlas):
    param = {'f_max': 300, 'alpha': 0.3}

    def __init__(self):
        self.fodder_max = self.param['f_max']
        pass


class Jungle(Atlas):
    def __init__(self, fodder_max):
        self.fodder_max = fodder_max
        pass


# Må kanskje tenke på at hver CELLE er en type og ikke området?