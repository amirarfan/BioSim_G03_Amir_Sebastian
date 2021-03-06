# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

"""
Simulation of the Island with visualization

"""

from .map import Map
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import subprocess
import random
import os
import textwrap

_FFMPEG_BINARY = "ffmpeg"
_CONVERT_BINARY = "magick"

_DEFAULT_GRAPHICS_DIR = os.path.join("..", "data")
_DEFAULT_GRAPHICS_NAME = "dv"
_DEFAULT_MOVIE_FORMAT = "mp4"  # alternatives: mp4, gif


class BioSim:
    """
    Simulation of biosim
    """

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

        self._map = Map(island_map)

        self.map_rgb = [
            [self.rgb_value[column] for column in row]
            for row in island_map.splitlines()
        ]

        self._map.add_animals(ini_pop)
        np.random.seed(seed)
        random.seed(seed)

        self._year = 0
        self._final_year = None
        self._num_animals = 0
        self._num_animals_per_species = {}
        self._animal_distribution = None

        self.img_fmt = img_fmt
        self.img_count = 0
        self.img_base = img_base

        self._island_map = None
        self._fig = None
        self._map_ax = None
        self._mean_ax = None
        self._herb_line = None
        self._carn_line = None

        self.herb_heat = None
        self.carn_heat = None

        self.herb_img_axis = None
        self.carn_img_axis = None

        self.year_counter_active = False

        if ymax_animals is None:
            self.ymax_animals = 20000
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

        self._final_year = self.year + num_years
        self._setup_graphics()

        while self._year < self._final_year:
            if self._year % vis_years == 0:
                self._update_graphics()

            if self._year % img_years == 0:
                self._save_graphics()

            self._map.cycle()

            self._year += 1

    def _setup_graphics(self):
        """

        Sets up plots and axes for the Simulation to be visualized

        """

        if self._fig is None:
            self._fig = plt.figure(figsize=(10, 8))

        if self._island_map is None:
            self._create_map()

        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(2, 2, 2)

        self._mean_ax.set_title("Herbivore and Carnivore Population")
        self._mean_ax.set_ylim(0, self.ymax_animals)
        self._mean_ax.set_xlim(0, self._final_year + 1)

        self._create_herb_line()
        self._create_carn_line()

        self.year_format = "Year: {:5d}"

        if not self.year_counter_active:
            self.txt = self._fig.text(
                0.09,
                0.97,
                self.year_format.format(0),
                ha="center",
                va="center",
                bbox=dict(boxstyle="round", ec=(0, 0, 0), fc="none",),
            )
            self.year_counter_active = True

        if self.herb_heat is None:
            self.herb_heat = self._fig.add_subplot(2, 2, 1)
            self.herb_heat.set_title("Herbivore Heat Map")
            self.herb_img_axis = None

        if self.carn_heat is None:
            self.carn_heat = self._fig.add_subplot(2, 2, 3)
            self.carn_heat.set_title("Carnivore Heat Map")
            self.carn_img_axis = None

        self._fig.tight_layout()

    def _update_graphics(self):
        """

        Updates the plots with new data

        """
        pop_df = self.animal_distribution

        rows, cols = np.shape(self._map.map)

        herb_count = pop_df.Herbivore
        herb_array = np.array(herb_count).reshape(rows, cols)

        carn_count = pop_df.Carnivore
        carn_array = np.array(carn_count).reshape(rows, cols)

        self._update_specie_lines()
        self._update_herb_heatmap(herb_array)
        self._update_carn_heatmap(carn_array)
        self.txt.set_text(self.year_format.format(self.year))
        plt.pause(1e-6)

    def _save_graphics(self):
        """

        Saves the plots as a specified file type.

        """

        if self.img_base is None:
            return

        print(
            "Saving to",
            "{base}_{num:05d}.{type}".format(
                base=self.img_base, num=self.img_count, type=self.img_fmt
            ),
        )

        plt.savefig(
            "{base}_{num:05d}.{type}".format(
                base=self.img_base, num=self.img_count, type=self.img_fmt
            )
        )

        self.img_count += 1

    def _create_map(self):
        """

        Creates map plot out of RGB colors and map string.

        """

        self._island_map = self._fig.add_subplot(2, 2, 4)
        self._island_map.set_title("Island Map")
        self._island_map.imshow(self.map_rgb)
        labels = ["Ocean", "Mountain", "Jungle", "Savannah", "Desert"]
        patches = [
            mpatches.Patch(color=self.rgb_value[i], label=labels[n])
            for n, i in enumerate(self.rgb_value.keys())
        ]
        self._island_map.legend(handles=patches, prop={"size": 5}, loc=4)

        self._island_map.set_xticks(range(len(self.map_rgb[0])))
        self._island_map.set_xticklabels(
            labels=(range(1, 1 + len(self.map_rgb[0]))),
            fontdict={"fontsize": 6},
        )
        self._island_map.set_yticks(range(len(self.map_rgb)))
        self._island_map.set_yticklabels(
            labels=range(1, 1 + len(self.map_rgb)), fontdict={"fontsize": 6}
        )

    def _create_herb_line(self):
        """

        Creates population graph for Herbivores

        """
        if self._herb_line is None:
            herb_plot = self._mean_ax.plot(
                np.arange(0, self._final_year),
                np.full(self._final_year, np.nan),
            )
            self._herb_line = herb_plot[0]
        else:
            xdata, ydata = self._herb_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._herb_line.set_data(
                    np.hstack((xdata, xnew)), np.hstack((ydata, ynew))
                )

    def _create_carn_line(self):
        """

        Creates population graph for Carnivores

        """
        if self._carn_line is None:
            carn_plot = self._mean_ax.plot(
                np.arange(0, self._final_year),
                np.full(self._final_year, np.nan),
            )
            self._carn_line = carn_plot[0]
        else:
            xdata, ydata = self._carn_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = np.full(xnew.shape, np.nan)
                self._carn_line.set_data(
                    np.hstack((xdata, xnew)), np.hstack((ydata, ynew))
                )

    def _update_herb_heatmap(self, herb_heat):
        """

        Updates the heatmap for Herbivores

        """

        if self.herb_img_axis is not None:
            self.herb_img_axis.set_data(herb_heat)
        else:
            self.herb_img_axis = self.herb_heat.imshow(
                herb_heat,
                interpolation="nearest",
                vmin=0,
                vmax=self.cmax_animals["Herbivore"],
            )
            cax = self._fig.add_axes([0.05, 0.5, 0.4, 0.02])
            cbar = self._fig.colorbar(
                self.herb_img_axis, cax=cax, orientation="horizontal"
            )
            cbar.set_ticks([])
            cbar.ax.text(0.5, 0, "Low", va="bottom", ha="left", color="white")
            cbar.ax.text(50, 0, "High", va="bottom", ha="right")

        self.herb_heat.set_xticks(range(len(self.map_rgb[0])))
        self.herb_heat.set_xticklabels(
            labels=(range(1, 1 + len(self.map_rgb[0]))),
            fontdict={"fontsize": 6},
        )
        self.herb_heat.set_yticks(range(len(self.map_rgb)))
        self.herb_heat.set_yticklabels(
            labels=range(1, 1 + len(self.map_rgb)), fontdict={"fontsize": 6}
        )

    def _update_carn_heatmap(self, carn_heat):
        """

        Updates the heaptmap for Carnivores


        """

        if self.carn_img_axis is not None:
            self.carn_img_axis.set_data(carn_heat)
        else:
            self.carn_img_axis = self.carn_heat.imshow(
                carn_heat,
                interpolation="nearest",
                vmin=0,
                vmax=self.cmax_animals["Carnivore"],
            )

        self.carn_heat.set_xticks(range(len(self.map_rgb[0])))
        self.carn_heat.set_xticklabels(
            labels=(range(1, 1 + len(self.map_rgb[0]))),
            fontdict={"fontsize": 6},
        )
        self.carn_heat.set_yticks(range(len(self.map_rgb)))
        self.carn_heat.set_yticklabels(
            labels=(range(1, 1 + len(self.map_rgb))), fontdict={"fontsize": 6}
        )

    def _update_specie_lines(self):
        """

        Updates the population lines for Herbivore and Carnivore

        """
        herb_amount = self.num_animals_per_species["Herbivore"]
        ydata_herb = self._herb_line.get_ydata()
        ydata_herb[self._year] = herb_amount
        self._herb_line.set_ydata(ydata_herb)

        carn_amount = self.num_animals_per_species["Carnivore"]
        ydata_carn = self._carn_line.get_ydata()
        ydata_carn[self._year] = carn_amount
        self._carn_line.set_ydata(ydata_carn)

        self._mean_ax.legend(["Herbivore", "Carnivore"], prop={"size": 6})

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
        self._num_animals = sum(self._map.num_species_on_map())
        print(self._num_animals)
        return self._num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        tot_herbivore, tot_carnivore = self._map.num_species_on_map()
        self._num_animals_per_species["Herbivore"] = tot_herbivore
        self._num_animals_per_species["Carnivore"] = tot_carnivore

        return self._num_animals_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on
        island. """
        list_of_dicts = []
        y_lim, x_lim = np.shape(self._map.map)
        for y in range(y_lim):
            for x in range(x_lim):
                curr_cell = self._map.map[(y, x)]
                (
                    curr_herbivores,
                    curr_carnivores,
                ) = curr_cell.num_species_per_cell()
                curr_dict = {
                    "Row": y,
                    "Col": x,
                    "Herbivore": curr_herbivores,
                    "Carnivore": curr_carnivores,
                }
                list_of_dicts.append(curr_dict)

        df = pd.DataFrame(
            list_of_dicts, columns=["Row", "Col", "Herbivore", "Carnivore"]
        )

        return df

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """Create MPEG4 movie from visualization images saved."""

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == "mp4":
            try:
                # Parameters chosen according to
                # http://trac.ffmpeg.org/wiki/Encode/H.264, section
                # "Compatibility"
                subprocess.check_call(
                    [
                        _FFMPEG_BINARY,
                        "-i",
                        "{}_%05d.png".format(self.img_base),
                        "-y",
                        "-profile:v",
                        "baseline",
                        "-level",
                        "3.0",
                        "-pix_fmt",
                        "yuv420p",
                        "{}.{}".format(self.img_base, movie_fmt),
                    ]
                )
            except subprocess.CalledProcessError as err:
                raise RuntimeError("ERROR: ffmpeg failed with: {}".format(err))
        elif movie_fmt == "gif":
            try:
                subprocess.check_call(
                    [
                        _CONVERT_BINARY,
                        "-delay",
                        "1",
                        "-loop",
                        "0",
                        "{}_*.png".format(self.img_base),
                        "{}.{}".format(self.img_base, movie_fmt),
                    ]
                )
            except subprocess.CalledProcessError as err:
                raise RuntimeError(
                    "ERROR: convert failed with: {}".format(err)
                )
        else:
            raise ValueError("Unknown movie format: " + movie_fmt)
