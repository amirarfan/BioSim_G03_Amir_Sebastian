# -*- coding: utf-8 -*-

__author__ = "Amir Arfan, Sebastian Becker"
__email__ = "amar@nmbu.no, sebabeck@nmbu.no"

"""

Very simple GUI, that needs work. Created to illustrate how a GUI could be used
with this project. One could also add parameters, and other options.

"""

import PySimpleGUI as sg
from biosim.simulation import BioSim
import matplotlib.pyplot as plt
import textwrap

if __name__ == "__main__":
    sg.ChangeLookAndFeel("SystemDefault")

    sg.SetOptions(text_justification="right")

    layout = [
        [sg.Text("BioSim Parameters", font=("Helvetica", 16))],
        [
            sg.Text("Years to simulate", size=(15, 1)),
            sg.Spin(
                values=[i for i in range(150, 1000)],
                initial_value=200,
                size=(6, 1),
            ),
            sg.Text("Seed", size=(18, 1)),
            sg.Spin(
                values=[i for i in range(1, 10000)],
                initial_value=123456,
                size=(6, 1),
            ),
        ],
        [
            sg.Text("Number of Herbivores", size=(20, 1)),
            sg.In(default_text=150, size=(5, 1)),
            sg.Text("Number of Carnivores", size=(20, 1)),
            sg.In(default_text=150, size=(5, 1)),
        ],
        [sg.Text("_" * 100, size=(65, 1))],
        [sg.Text("Map Type", font=("Helvetica", 15), justification="left")],
        [
            sg.Text("Map", size=(15, 1)),
            sg.Drop(
                values=("Standard", "Only Desert", "Only Jungle"),
                auto_size_text=True,
            ),
            sg.Text("When to add Carnivores", size=(15, 1)),
            sg.Drop(values=(100, 200, 300)),
        ],
        [sg.Submit(), sg.Cancel()],
    ]

    window = sg.Window("BioSim", layout, font=("Helvetica", 12))

    event, values = window.read()

    window.close()

    if event == "Cancel":
        raise ValueError("Program was canceled")

    if event == "Submit":
        print("Starting program")

    (
        num_years,
        spec_seed,
        num_herbs,
        num_carns,
        map_type,
        delay,
    ) = values.values()

    if num_years < delay:
        raise ValueError("Carnivores cant be added after end of simulation")

    if map_type is None:
        raise ValueError("You must choose a map type!")

    if map_type == "Standard":
        geogr = """\
                      OOOOOOOOOOOOOOOOOOOOO
                      OOOOOOOOSMMMMJJJJJJJO
                      OSSSSSJJJJMMJJJJJJJOO
                      OSSSSSSSSSMMJJJJJJOOO
                      OSSSSSJJJJJJJJJJJJOOO
                      OSSSSSJJJDDJJJSJJJOOO
                      OSSJJJJJDDDJJJSSSSOOO
                      OOSSSSJJJDDJJJSOOOOOO
                      OSSSJJJJJDDJJJJJJJOOO
                      OSSSSJJJJDDJJJJOOOOOO
                      OOSSSSJJJJJJJJOOOOOOO
                      OOOSSSSJJJJJJJOOOOOOO
                      OOOOOOOOOOOOOOOOOOOOO"""

        geogr = textwrap.dedent(geogr)

    if map_type == "Only Desert":
        geogr = """\
                    OOOOOOOOOOOOOOOOOOOOO
                    OOOOOOOODDDDDDDDDDDDO
                    ODDDDDDDDDDDDDDDDDDOO
                    ODDDDDDDDDDDDDDDDDOOO
                    ODDDDDDDDDDDDDDDDDOOO
                    OODDDDDDDDDDDDDDDDOOO
                    OODDDDDDDDDDDDDDDDOOO
                    OODDDDDDDDDDDDDDDDOOO
                    ODDDDDDDDDDDDDDDDDDOO
                    OOOODDDDDDDDDDDDDDDOO
                    ODDDDDDDDDDDDDDDDDDOO
                    ODDDDDDDDDDDDDDDDDDOO
                    OOOOOOOOOOOOOOOOOOOOO"""

        geogr = textwrap.dedent(geogr)

    if map_type == "Only Jungle":
        plt.ion()

        geogr = """\
                      OOOOOOOOOOOOOOOOOOOOO
                      OOOOOOOOSMMMMJJJJJJJO
                      OSSSSSJJJJMMJJJJJJJOO
                      OSSSSSSSSSMMJJJJJJOOO
                      OSSSSSJJJJJJJJJJJJOOO
                      OSSSSSJJJDDJJJSJJJOOO
                      OSSJJJJJDDDJJJSSSSOOO
                      OOSSSSJJJDDJJJSOOOOOO
                      OSSSJJJJJDDJJJJJJJOOO
                      OSSSSJJJJDDJJJJOOOOOO
                      OOSSSSJJJJJJJJOOOOOOO
                      OOOSSSSJJJJJJJOOOOOOO
                      OOOOOOOOOOOOOOOOOOOOO"""
        geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(eval(num_herbs))
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(eval(num_carns))
            ],
        }
    ]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=eval(spec_seed))

    sim.simulate(num_years=delay, vis_years=1, img_years=2000)

    sim.add_population(population=ini_carns)

    sim.simulate(num_years=num_years - delay, vis_years=1, img_years=2000)

    plt.savefig("gui_sim.pdf")

    input("Press ENTER to save figure as 'gui_sim.pdf'")
