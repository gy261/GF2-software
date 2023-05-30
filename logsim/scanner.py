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
        """Initialize symbol properties."""
        self.type = None
        self.id = None
        self.line_num = 0  # The line number of the text file where the symbol is found
        self.pos = 0     # The column number of the text file where the symbol is found at its first chracter


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
                      and returns the symbol, with white spaces skipped.

    get_exact_symbol(self): Translate the next sequence of characters into a symbol.
                            Without skipping any spaces. So a SPACE type symbol is
                            possible.

    display_error(self, error_message, error_symbol): Prints out the error_message when 
                    an error occurs, along with the text line and the exact position of 
                    the symbol that causes the error.
    
    display_global_error(self, error_message): Prints out the error_message when a global 
                    error occurs, usually for the logic error of the whole circuit.
    """

    def __init__(self, path, names):
        """Open specified file and initialize reserved words and IDs."""
        if not isinstance(names, Names):
            raise TypeError("Expected names to be an instance of the Names class.")
        self.names = names

        if not isinstance(path, str):
            raise TypeError("Expected path name to be a string.")
        try:
            file = open(path, "r")
        except FileNotFoundError:
            print("The path provided is not found.")
            sys.exit()
        else:
            self.file_lines = file.readlines()  # Stores all the lines of the text file
            file.seek(0,0)
            self.file = file

        self.symbol_type_list = [
            self.KEYWORD, self.NUMBER, self.HEADING, self.NAME, self.COMMA, self.ARROW,
            self.SEMICOLON, self.COLON, self.DOT, self.EQUAL, self.PIN, self.SPACE, self.EOF
        ] = range(13)

        self.heading_list = ["DEVICE", "CONNECTION", "MONITOR"]

        [
            self.DEVICE_ID, self.CONNECTION_ID, self.MONITOR_ID
        ] = self.names.lookup(self.heading_list)

        self.keyword_list = [
            "NAND", "AND", "OR", "NOR", "XOR", "DTYPE", "SWITCH", "CLOCK", "CON", "MON"
        ]

        [
            self.NAND_ID, self.AND_ID, self.OR_ID, self.NOR_ID, self.XOR_ID, self.DTYPE_ID,
            self.SWITCH_ID, self.CLOCK_ID, self.CON_ID, self.MON_ID
        ] = self.names.lookup(self.keyword_list)

        self.pin_list = [
            "I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "I10", "I11", "I12", "I13", "I14",
            "I15", "I16", "Q", "QBAR", "DATA", "CLK", "SET", "CLEAR"
        ]

        self.pin_id = [
            self.I1_ID, self.I2_ID, self.I3_ID, self.I4_ID, self.I5_ID, self.I6_ID, self.I7_ID,
            self.I8_ID, self.I9_ID, self.I10_ID, self.I11_ID, self.I12_ID, self.I13_ID, self.I14_ID,
            self.I15_ID, self.I16_ID, self.Q_ID, self.QBAR_ID, self.DATA_ID, self.CLK_ID,
            self.SET_ID, self.CLEAR_ID
        ] = self.names.lookup(self.pin_list)

        self.cur_character = " "
        self.cur_line = 1
        self.cur_pos = 0
        self.prev_pos = -1      # Used for error message pointer '^'
        self.error_count = 0
        # self.names.display_list()

    def skip_comments(self):
        """Skip through all the comments following the sign # until a new line is reached."""
        while self.cur_character != "\n":
            self.advance()
        self.advance()

    def skip_spaces(self):
        """Skip through all the spaces and newlines until reaching a non-space character."""
        # print("current cha skip_space:")
        while self.cur_character.isspace():
            self.advance()

    def advance(self):
        """Read the next character from the definition file and place it in cur_character."""
        # print("ADVANCING:",self.cur_character)
        self.prev_pos = self.cur_pos
        self.cur_pos += 1
        self.cur_character = self.file.read(1)
        # print("AFTER ADVANCING:",self.cur_character)
        if self.cur_character == "\n":
            self.cur_line += 1
            self.cur_pos = 0

    def get_name(self):
        """Return the name string (or None)."""
        name = self.cur_character  # By default, self.cur_character must be a letter initially

        while True:
            self.advance()
            if self.cur_character.isalnum():
                name += self.cur_character
            else:
                return name

    def get_number(self):
        """Return the next number."""
        number = self.cur_character  # By default, self.cur_character must be a digit initially

        while True:
            self.advance()
            if self.cur_character.isdigit():
                number = number + self.cur_character
            else:
                return number

    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""
        symbol = Symbol()
        self.skip_spaces()
        if self.cur_character == "#":
            self.skip_comments()
            # print("A comment has been encountered.")

        # print("################ NEW SYMBOL ##################")
        # print("current cha:", self.cur_character)

        symbol.pos = self.cur_pos
        if self.cur_character.isalpha():  # name
            name_string = self.get_name()
            # print("The symbol is:", name_string)
            if name_string in self.keyword_list:
                symbol.type = self.KEYWORD
            elif name_string in self.heading_list:
                symbol.type = self.HEADING
            elif name_string in self.pin_list:
                symbol.type = self.PIN
            else:
                symbol.type = self.NAME

            [symbol.id] = self.names.lookup([name_string])


        elif self.cur_character.isdigit():
            num_string = self.get_number()
            [symbol.id] = self.names.lookup([num_string])
            symbol.type = self.NUMBER
            # print("The symbol is a number:", symbol.id)

        elif self.cur_character == ",":
            symbol.type = self.COMMA
            self.advance()
            # print("The symbol is a comma")

        elif self.cur_character == ";":
            symbol.type = self.SEMICOLON
            self.advance()
            # print("The symbol is a semicolon")

        elif self.cur_character == ":":
            symbol.type = self.COLON
            self.advance()
            # print("The symbol is a colon")

        elif self.cur_character == ".":
            symbol.type = self.DOT
            self.advance()
            # print("The symbol is a dot")

        elif self.cur_character == "=":
            symbol.type = self.EQUAL
            self.advance()
            # print("The symbol is a equal")

        elif self.cur_character == "-":
            self.advance()
            if self.cur_character == ">":
                symbol.type = self.ARROW
                self.advance()
                # print("The symbol is an arrow")
            else:
                self.advance()
                return symbol

        elif self.cur_character == "":
            symbol.type = self.EOF
            # print("The symbol is a EOF")

        else:
            self.advance()
            return symbol

        symbol.line_num = self.cur_line
        # print("Current position:",self.cur_pos)
        return symbol

    def get_exact_symbol(self):
        """Translate the next sequence of characters into a symbol.
        Without skipping any spaces. So a SPACE type symbol is possible.
        """
        symbol = Symbol()
        if self.cur_character == "#":
            self.skip_comments()
            # print("A comment has been encountered.")

        # print("################ NEW SYMBOL ##################")
        # print("current cha:", self.cur_character)
        symbol.pos = self.cur_pos
        if self.cur_character.isalpha():  # name
            name_string = self.get_name()
            # print("The symbol is:", name_string)
            if name_string in self.keyword_list:
                symbol.type = self.KEYWORD
            elif name_string in self.heading_list:
                symbol.type = self.HEADING
            elif name_string in self.pin_list:
                symbol.type = self.PIN
            else:
                symbol.type = self.NAME

            [symbol.id] = self.names.lookup([name_string])

        elif self.cur_character.isspace():
            symbol.type = self.SPACE
            self.advance()
            # print("The symbol is a space")

        elif self.cur_character.isdigit():
            num_string = self.get_number()
            [symbol.id] = self.names.lookup([num_string])
            symbol.type = self.NUMBER
            # print("The symbol is a number:", symbol.id)

        elif self.cur_character == ",":
            symbol.type = self.COMMA
            self.advance()
            # print("The symbol is a comma")

        elif self.cur_character == ";":
            symbol.type = self.SEMICOLON
            self.advance()
            # print("The symbol is a semicolon")

        elif self.cur_character == ":":
            symbol.type = self.COLON
            self.advance()
            # print("The symbol is a colon")

        elif self.cur_character == ".":
            symbol.type = self.DOT
            self.advance()
            # print("The symbol is a dot")

        elif self.cur_character == "=":
            symbol.type = self.EQUAL
            self.advance()
            # print("The symbol is a equal")

        elif self.cur_character == "-":
            self.advance()
            if self.cur_character == ">":
                symbol.type = self.ARROW
                self.advance()
                # print("The symbol is an arrow")
            else:
                return symbol

        elif self.cur_character == "":
            symbol.type = self.EOF
            # print("The symbol is a EOF")

        else:
            return symbol

        symbol.line_num = self.cur_line

        return symbol

    def display_error(self, error_message, error_symbol):
        """Display an error message whenever the parser encounters an error."""
        self.error_count += 1

        if not isinstance(error_message, str):
            raise TypeError("error_message must be a string!")
        
        if not isinstance(error_symbol, Symbol):
            raise TypeError("error_symbol must be a Symbol!")
        
        if error_symbol.type == self.EOF:
            i = -1
            while self.file_lines[i] == "\n":
                i -= 1
            line_of_text = self.file_lines[i]
            error_line_num = str(self.cur_line + i)
            error_pos = len(self.file_lines[int(error_line_num)-1])

        elif self.cur_pos == 0:
            line_of_text = self.file_lines[self.cur_line - 2]
            error_line_num = str(self.cur_line - 1)
            error_pos = error_symbol.pos - 1

        else:
            line_of_text = self.file_lines[self.cur_line - 1]
            error_line_num = str(self.cur_line)
            error_pos = error_symbol.pos - 1

        if not line_of_text.endswith("\n"):
            line_of_text = line_of_text + "\n"
        output_message = (
            "ERROR on line " + error_line_num + ": " + error_message + "\n" +
            line_of_text + " " * error_pos + "^"
        )

        print(output_message)
    
    def display_global_error(self, error_message):
        """Display a global error message, usually when there is a logic error"""
        self.error_count += 1

        if not isinstance(error_message, str):
            raise TypeError("error_message must be a string!")

        print(error_message)
