class Atlas:
    def __init__(self, map):
        self.map = map

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
    def __init__(self, fodder_max):
        self.fodder_max = fodder_max
        pass

class Jungle(Atlas):
    def __init__(self, fodder_max):
        self.fodder_max = fodder_max
        pass




