"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""
from names import Names
import sys

class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None
        self.line_num = 0  # The line number of the text file where the symbol is found
        # self.pos = 0     # The column number of the text file where the symbol is found at its first chracter


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""

        # Check that the names provided is valid 
        if isinstance(names, Names):
            self.names = names
        else:
            raise TypeError("Expected names to be a instance of the Names class.")
        
        # Check that the path provided is valid
        if isinstance(path, str):
            raise TypeError("Expected path name tobe a string.")
        else:
            try:
                file = open(path, "r")
            except FileNotFoundError:
                print("The path provided is not found.")
                sys.exit()
            else:
                self.file = file    

                """This file_lines stores all the lines of the text file, which we will use for printing error messages, 
                 so that we do not have to move the scanner cursor""" 
                self.file_lines = file.readlines() 

        self.symbol_type_list = [self.KEYWORD, self.NUMBER, self.HEADING,\
                    self.NAME, self.COMMA, self.ARROW, self.SEMICOLON, self.COLON, self.DOT,\
                    self.EQUAL,self.PIN, self.EOF] = range(11)
        
        self.heading_list = ["DEVICE","CONNECTION","MONITOR"]
        [self.DEVICE_ID, self.CONNECTION_ID, self.MONITOR_ID] = self.names.lookup(self.heading_list)

        self.keyword_list = ["NAND", "AND", "OR", "NOR", "XOR", "DTYPE","SWICTH", "CLOCK", "CON", "MON"]
        [self.NAND_ID, self.AND_ID, self.OR_ID, self.NOR_ID, self.XOR_ID, self.DTYPE_ID, \
         self.SWITCH_ID, self.CLOCK_ID, self.CON_ID, self.MON_ID] = self.names.lookup(self.keyword_list)

        self.pin_list = ["I1","I2","I3","I4","I5","I6","I7","I8","I9","I10","I11","I12","I13","I14",\
                        "I15", "I16", "Q", "QBAR", "DATA", "CLK", "SET", "CLEAR"]
        [self.I1_ID, self.I2_ID, self.I3_ID, self.I4_ID, self.I5_ID, self.I6_ID, self.I7_ID, self.I8_ID, self.I9_ID, self.I10_ID, self.I11_ID, self.I12_ID, \
         self.I13_ID, self.I14_ID, self.I15_ID, self.I16_ID, self.Q_ID, self.QBAR_ID, self.DATA_ID, self.CLK_ID, self.SET_ID, self.CLEAR_ID] = self.names.lookup(self.pin_list)

        self.num_error = 0
        self.cur_character = ""
        self.cur_line = 1
        self.cur_pos = 0

        # The below variables are used to store errors, the parser would call the 
        self.num_error = 0
        self.error_list = []
    
    def skip_spaces(self):
        # Skip through all the spaces and newlines until reaching a non-space character
        while self.cur_character.isspace():
            self.cur_character = self.advance()
    
    def advance(self):
        # Read the next character from the definition file and places it in cur_character
        self.cur_pos += 1
        self.cur_character = self.file.read(1)
        if self.cur_character == "\n":
            self.cur_line += 1
            self.cur_pos = 0

    def get_name(self):
        """ Return the name string (or None) and the next non-alphanumeric character. """
        name = self.cur_character   # By default, self.cur_character must be a letter initially

        while True:
            self.advance()
            if self.cur_character.isalnum():
                name = name + self.cur_character
            else:
                return [name, self.cur_character]
    
    def get_number(self):
        """ Return the number (or None) and the next non-alphanumeric character. """
        number = self.cur_character   # By default, self.cur_character must be a digit initially

        while True:
            self.advance()
            if self.cur_character.isdigit():
                number = number + self.cur_character
            else:
                return [int(number), self.cur_character]

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol
        self.skip_spaces()

        if self.cur_character.isalpha(): # name
            name_string = self.get_name()
            if name_string in self.keywords_list:
                symbol.type = self.KEYWORD
            elif name_string in self.heading_list:
                symbol.type = self.HEADING
            elif name_string in self.pin_list:
                symbol.type = self.PIN
            else:
                symbol.type = self.NAME

            [symbol.id] = self.names.lookup([name_string])

        elif self.cur_character.isdigit():
            symbol.id = self.get_number()
            symbol.type = self.NUMBER
        
        elif self.cur_character == ",":
            symbol.type = self.COMMA
            self.advance()
        
        elif self.cur_character == ";":
            symbol.type = self.SEMICOLON
            self.advance()
        
        elif self.cur_character == ":":
            symbol.type = self.COLON
            self.advance()
        
        elif self.cur_character == ".":
            symbol.type = self.DOT
            self.advance()

        elif self.cur_character == "=":
            symbol.type = self.EQUAL
            self.advance()
        
        elif self.cur_character == "":
            symbol.type = self.EOF
        
        else:
            raise SyntaxError("Invalid character encountered!")

        symbol.line_num = self.cur_line

        return symbol

def display_error(self, error_message):
    """ This function displays an error message whenever the parser encounters an error;
        Prints the current text line and a ^ symbol on the next line to highlight the location of the error.
        Then prints the error message. This function is repeatedly called by the parser. """    
    
    self.num_error += 1
    
    if not isinstance(error_message, str):
        raise TypeError("error_message must be a string!")

    line_of_text = self.file_lines[self.cur_line - 1]
    output_message = "ERROR on line " + str(self.cur_line) + ": " + error_message + "\n" + \
                    line_of_text + " "*self.cur_pos + "^"
    
    print(output_message)
    
    


    
    