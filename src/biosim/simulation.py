# -*- coding: utf-8 -*-
from biosim.animals import Herbivore, Carnivore
from biosim.map import Map
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
"""

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"


class BioSim:
    rgb_value = {
        "O": (0.0, 0.0, 1.0),
        "M": (0.5, 0.5, 0.5),
        "J": (0.0, 0.6, 0.0),
        "S": (0.5, 1.0, 0.5),
        "D": (1.0, 1.0, 0.5),
    }

    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.map_rgb = [
            [self.rgb_value[column] for column in row]
            for row in island_map.splitlines
        ]

        self._map = Map(island_map)
        self._map.add_animals(ini_pop)
        np.random.seed(seed)

        self._year = 0
        self._final_year = None
        self._num_animals = 0
        self._num_animals_per_species = {}
        self._animal_distribution = None

        self._fig = None
        self._map_ax = None
        self._mean_ax = None
        self._mean_line = None
        self.img_axis = None

        if ymax_animals is None:
            self.ymax_animals = None
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is not None:
            self.cmax_animals = cmax_animals
        else:
            self.cmax_animals = {"Herbivore": 50, "Carnivore": 20}

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        self._map.update_animal_params_all_cells(species, params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        self._map.update_param_all_cells(landscape, params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """

        if img_years is None:
            img_years = vis_years

        self._final_year = self._year + img_years

        while self._year < self._final_year:

            if self._year % vis_years == 0:
                self._update_graphics()

            self._map.cycle()
            self._year += 1

    def _setup_graphics(self):

        if self._fig is None:
            self._fig = plt.figure()

        if self._map_ax is None:
            self._max_ax = self._fig.add_subplot(1, 2, 1)
            self._img_axis = None

        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(1, 2, 2)
            if self.ymax_animals is not None:
                self._mean_ax.set_ylim(self.ymax_animals)
            else:
                self._mean_ax.set_ylim(auto=True)

        self._mean_ax.set_xlim(0, self._final_year + 1)

        if self._mean_line is None:
            mean_plot = self._mean_ax.plot(
                np.arange(0, self._final_year),
                np.full(self._final_year, np.nan),
            )
        else:
            xdata, ydata = self._mean_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._mean_line.set_data(
                    np.hstack((xdata, xnew)), np.hstack((ydata, ynew))
                )

    def _update_graphics(self):
        pass

    def _update_system_map(self):
        pass

    def _update_mean_graph(self, mean):

    def _save_graphics(self):
        pass

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

        self._map.add_animals(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        self._num_animals = self._map.num_animals_on_map()
        return self._num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        tot_herbivore, tot_carnivore = self._map.num_species_on_map()
        self._num_animals_per_species["Herbivores"] = tot_herbivore
        self._num_animals_per_species["Carnivores"] = tot_carnivore

        return self._num_animals_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""
        list_of_dicts = []
        for y, cell_list in enumerate(self._map.map):
            for x, cells in enumerate(cell_list):
                curr_herbivores, curr_carnivores = (
                    cells.num_animals_per_species()
                )
                curr_dict = {
                    "x": x,
                    "y": y,
                    "herbivores": curr_herbivores,
                    "carnivores": curr_carnivores,
                }
                list_of_dicts.append(curr_dict)

        return pd.DataFrame(
            list_of_dicts, columns=["x", "y", "herbivores", "carnivores"]
        )

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
