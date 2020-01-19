# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

from .cell import Ocean, Mountain, Desert, Savannah, Jungle
# noinspection PyUnresolvedReferences
from .animals import Herbivore, Carnivore
import numpy as np


class Map:
    """
    Map class which will represent a map containing different cells
    """

    dict_cells = {
        "O": Ocean,
        "M": Mountain,
        "D": Desert,
        "S": Savannah,
        "J": Jungle,
    }

    allowed_cells = ["Jungle", "Savannah", "Desert"]

    def __init__(self, map_string):
        """
        Initialises the map class instance

        Parameters
        ----------
        map_string: string
                    String representing a map of cells
        """

        self.check_even_string(map_string)

        self.map = np.array(
            [
                self.map_factory(curr_list)
                for curr_list in map_string.split("\n")
            ]
        )

        self.outer_limits = np.concatenate(
            [self.map[0], self.map[:, 0], self.map[:, -1], self.map[-1]]
        )

        for cell in self.outer_limits:
            if type(cell).__name__ != "Ocean":
                raise ValueError(f"Outer Cell is not Ocean")

    @staticmethod
    def check_even_string(map_string):
        prev_line_length = None
        for line in map_string.split("\n"):
            line_length = len(line)
            if prev_line_length is None:
                pass
            elif line_length != prev_line_length:
                raise ValueError("The lines are not uniform")
            prev_line_length = line_length

    @classmethod
    def map_factory(cls, list_to_alter):
        """
        A map factory function which transforms a list containing strings into
        a list containing cell instances.

        Parameters
        ----------
        list_to_alter: list
                    List containing different string letters, which need to be
                    transformed to class types.

        Returns
        -------
        list
            Contains cell class instances


        """
        temp_list = []
        for letter in list_to_alter:
            # Only cell types which are allowed can be transformed
            if letter not in cls.dict_cells.keys():
                raise ValueError(f"{letter} is not an allowed cell type")
            temp_list.append(cls.dict_cells[letter]())

        return temp_list

    def get_neighbour(self, loc):
        """

        Given a location loc, the get_neighbour function returns the
        4 neighbours someone or something can move to.

        Parameters
        ----------
        loc: tuple


        Returns
        -------
        neighbour_cells: list
                        Contains neighbour cells

        """
        y_lim, x_lim = np.shape(self.map)
        y, x = loc
        neighbour_cords = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        neighbour_cells = []
        for cords in neighbour_cords:
            curr_y, curr_x = cords
            if curr_y < 0 or curr_y >= y_lim:
                pass
            elif curr_x < 0 or curr_x >= x_lim:
                pass
            else:
                neighbour_cells.append(self.map[cords])

        return neighbour_cells

    def add_animals(self, ini_list):
        """
        Adds animals to the map using the specified location and specie type
        from ini_list

        Parameters
        ----------
        ini_list: list
                list which contains location and specie information


        """
        for dictionary in ini_list:
            try:
                loc = dictionary["loc"]
            except KeyError:
                print("No location specified")
                break
            pop_list = dictionary["pop"]

            cell_type = self.map[loc]

            if type(cell_type).__name__ not in self.allowed_cells:
                raise ValueError(f"This cell location is inhabitable")

            cell_type.add_animal(pop_list)

    def move_all_animals(self):
        """
        Moves all animals in the map, using the migration function from
        'cell.py'

        """

        y_lim, x_lim = np.shape(self.map)
        for y in range(y_lim):
            for x in range(x_lim):
                loc = y, x
                self.map[loc].migration(self.get_neighbour((y, x)))

    def all_animals_eat(self):
        """

        Feeds all animals on the map using eat_herbivore and eat_carnivore
        functions from 'cell.py'


        """
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.gen_fodder()
                    cell.eat_herbivore()
                    cell.eat_carnivore()

    def mate_all_animals(self):
        """
        Mates all animals on the map using the mating function from 'cell.py'


        """
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.mating()

    def age_all_animals(self):
        """

        Ages all animals with one year, using the aging function from 'cell.py'

        """
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.aging()

    def annual_weight_loss_all_animals(self):
        """

        Makes all animals lose their annual amount of weigh using
        the annual_weight_loss function from 'cell.py'

        """

        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.annual_weight_loss()

    def annual_death_all_animals(self):
        """

        Checks all animals annual death, by using annual_death from 'cell.py'

        """
        for list_loc in self.map:
            for cell in list_loc:
                if type(cell).__name__ in self.allowed_cells:
                    cell.annual_death()

    def num_animals_on_map(self):
        """

        Calculates the total amount of animals on the map, by entering
        each cell and checking how many animals are there.

        Returns
        -------
        int
            The amount of animals on the whole map
        """

        tot_animals = 0
        for cell_list in self.map:
            for cell in cell_list:
                tot_animals += cell.num_animals_per_cell()

        return tot_animals

    def num_species_on_map(self):
        """

        Calculates and returns the total amount of per specie on the map

        Returns
        -------
        int
            The amount of herbivores on the map
        int
            The amount of carnivores on the map

        """
        tot_herbivores = 0
        tot_carnivores = 0
        for cell_list in self.map:
            for cells in cell_list:
                curr_herbivore, curr_carnivore = cells.num_species_per_cell()
                tot_herbivores += curr_herbivore
                tot_carnivores += curr_carnivore

        return tot_herbivores, tot_carnivores

    @staticmethod
    def update_animal_params_all_cells(specie, params):
        """

        Updates parameters for specified specie in all cells.

        Parameters
        ----------
        specie: str
                The name of the specie which needs it's parameters updated
        params: dict
                Dictionary containing the updated values of the parameters.


        """

        eval(specie).update_parameters(params)

    def update_param_all_cells(self, landscape, params):
        """

        Updates parameters for all cells which are specified to be updated.

        Parameters
        ----------
        landscape: str
                 The cell type which needs its parameters updated
        params: dict
                Dictionary containing the new parameters


        """
        cell_type = self.dict_cells[landscape]
        cell_type.update_parameters(params)

    def cycle(self):
        """
        Simulates the annual cycle for all animals on the map

        """
        self.all_animals_eat()
        self.mate_all_animals()
        self.move_all_animals()
        self.age_all_animals()
        self.annual_weight_loss_all_animals()
        self.annual_death_all_animals()
