import biosim.cell as cell

def test_fodder_Mountain():
    fodder = cell.Mountain()
    assert fodder.relevant_fodder == None

def test_add_animal():
    cell.Cell
    assert ValueError

def test_fodder_Ocean():
    fodder = cell.Ocean()
    assert fodder.relevant_fodder == None

def test_gen_fodder_jung():
    fodder = cell.Jungle()
    assert fodder.current_fodder == fodder.param["f_max"]
    assert fodder.current_fodder != None

def test_gen_fodder_Savannah():
    fodder = cell.Savannah()
    assert fodder.param["f_max"] == 300
    assert fodder.current_fodder != None
