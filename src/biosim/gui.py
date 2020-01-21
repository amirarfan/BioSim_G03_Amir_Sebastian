import PySimpleGUI as sg

sg.ChangeLookAndFeel("SystemDefault")

sg.SetOptions(text_justification="right")

layout = [
    [sg.Text("BioSim Parameters", font=("Helvetica", 16))],
    [
        sg.Text("Years to simulate", size=(15, 1)),
        sg.Spin(
            values=[i for i in range(1, 1000)], initial_value=100, size=(6, 1)
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
    ],
    [sg.Submit(), sg.Cancel()],
]

window = sg.Window("BioSim", layout, font=("Helvetica", 12))

event, values = window.read()
print(values)
num_herbs = values[0]
num_carns = values[1]
