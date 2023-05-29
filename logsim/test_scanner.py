from scanner import Scanner, Symbol
from names import Names
import pytest

@pytest.fixture
def new_names():
    """Return a new names instance."""
    return Names()

def test_invalid_sacnner_intialisation_raises_exception(new_names):
    """Test if the scanner raises exceptions when incorrectly initialised."""
    with pytest.raises(TypeError):
        scanner = Scanner("text.txt", "names")
    with pytest.raises(TypeError):
        scanner = Scanner(1.2, "names")
    with pytest.raises(SystemExit):
        scanner = Scanner("randomfile.txt", new_names)

@pytest.fixture
def scanner_one(new_names):
    """Return a new scanner instance."""
    path_one = "test1.txt"
    scanner = Scanner(path_one, new_names)
    return scanner

def test_get_symbol(scanner_one):
    """Test if the get_symbols function works correctly in getting all symbols"""
    # DEVICE, ensures that the scanner would normally work for HEADING
    sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.HEADING
    assert sym.id == scanner_one.names.query("DEVICE")
    # :, ensures that the scanner would normally work for COLON and skips spaces
    sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.COLON
    assert sym.id == None
    # SWITCH, ensures that the scanner would properly to skip newlines
    sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.KEYWORD
    assert sym.id == scanner_one.names.query("SWITCH")
    # SW1, ensures that the scanner would work properly for NAME and for storing new names
    sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.NAME
    assert sym.id == len(scanner_one.names.names) - 1
    # =, ensures that the scanner would work properly for EQUAL
    sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.EQUAL
    assert sym.id == None
    # 1, ensures that the scanner would work properly for NUMBER
    sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.NUMBER
    assert sym.id == len(scanner_one.names.names) - 1
    # SWITCH, ensures that the scanner would work properly for skipping comments
    for i in range(2):
        sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.KEYWORD
    assert sym.id == scanner_one.names.query("SWITCH")
    # ;, ensures that the scanner would work properly for SEMICOLON
    for i in range(10):
        sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.SEMICOLON
    assert sym.id == None
    # ->, ensures that the scanner would work properly for ARROW
    for i in range(5):
        sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.ARROW
    assert sym.id == None
    # I1 ensures that the scanner would work properly for PIN
    for i in range(3):
        sym = scanner_one.get_symbol() 
    assert sym.type == scanner_one.PIN
    assert sym.id == scanner_one.names.query("I1")

names = Names()
scanner = Scanner("test2.txt", names)
"""
# Testing for get_symbol function

for i in range(10):
    a = scanner.get_symbol()
    print("The symbol type and id are", a.type, a.id)
    if a.id:
        print(names.get_name_string(a.id))

scanner.names.display_list()

"""

# Testing for error display 
message = "This is a testing error message!"

error_place = 2
for i in range(error_place):
    a = scanner.get_symbol()
    print("Symbol",i+1)
    if a.id != None:
        print(names.get_name_string(a.id))

scanner.display_error(message,a)


