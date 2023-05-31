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
    path_one = "testfile.txt"
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
    for i in range(14):
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

# This uses testfile.txt, for normal cases
@pytest.mark.parametrize("error_symbol_location, expected_arrow_pos, expected_line", [
    (4, 7 ,3),      # middle of line
    (2, 6, 1),      # end of line
    (8, 0, 4),      # start of new line
])

def test_display_error(error_symbol_location, expected_arrow_pos, expected_line):
    names = Names()
    scanner = Scanner("testfile.txt", names)
    for i in range(error_symbol_location):
        a = scanner.get_symbol()
    assert a.pos - 1 == expected_arrow_pos
    assert a.line_num == expected_line


# This uses testfile2.txt, for extreme boundary cases
@pytest.mark.parametrize("error_symbol_location, expected_arrow_pos, expected_line", [
    (1, 1 ,1),      # start of file
    (2, 1, 3),      # end of line with symbol missing
    (5, 0, 4),      # middle of line with symbol missing
    (9, 7, 5)       # end of file error
])

def more_test_display_error(error_symbol_location, expected_arrow_pos, expected_line):
    names = Names()
    scanner = Scanner("testfile2.txt", names)
    for i in range(error_symbol_location):
        a = scanner.get_symbol()
    assert a.pos - 1 == expected_arrow_pos
    assert a.line_num == expected_line


location = 3
names = Names()
scanner = Scanner("testfile_error_1.txt", names)
message = "This is a testing error message!"
for i in range(location):
    a = scanner.get_symbol()
print(a.line_num)
scanner.display_error(message,a)

