"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""

class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() cldevicesass.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names, devices, network, monitors, scanner):
        """Initialise constants."""
        self.names = names
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.scanner = scanner

        """Initialise cur_symbol for recording the current symbol
        ; initialise devices_list to keep track of any unused devices"""
        self.cur_symbol = None
        self.devices_list = set()



    def test(self, str=""):
        """Print out the current symbol for debug using."""
        if self.cur_symbol.id:
            print(str, self.cur_symbol.type, self.cur_symbol.id, ":", self.names.get_name_string(self.cur_symbol.id))
        else:
            print(str, self.cur_symbol.type, self.cur_symbol.id)

    def skip_line(self):
        """Skip symbols until the next semicolon is found or until the end of the file.
        This function is called when an error is detected."""
        while self.cur_symbol.type != self.scanner.SEMICOLON:
            if self.cur_symbol.type == self.scanner.EOF:
                return
            #  print(self.cur_symbol.id, self.cur_symbol.type)
            self.read()
        return "skipped"


    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        """Initialise some logic check boolean values."""
        """expect_xxx is used to check which assignments are valid in the current section"""
        expect_device = False
        expect_connection = False
        expect_monitor = False

        """xxx_section is used to check the order of headings;
        The headings must be in the order: DEVICE, CONNECTION, MONITOR according to the EBNF file"""
        device_section = False
        connection_section = False
        monitor_section = False

        """xxx_wrong_place is used to record if any heading is out of order;
        These booleans value will help print out the correct global error message"""
        device_wrong_place = False
        connection_wrong_place = False
        monitor_wrong_place = False

        """Initialisation of the main loop"""
        line_num = 0
        self.read()
        while True:
            if line_num > 0:
                self.read()

            #self.test("big loop:")

            """If symbol type is the End of File, then detect global error and return a boolean value"""
            if self.cur_symbol.type == self.scanner.EOF:
                #print(self.devices_list)

                """Check if any heading is missing"""
                if not device_section:
                    if not device_wrong_place:
                        self.global_error("No valid DEVICE section is input in the definition file")
                else:
                    if not connection_section:
                        if not connection_wrong_place:
                            self.global_error("No valid CONNECTION section is input in the definition file")
                    else:
                        if not monitor_section:
                            if not monitor_wrong_place:
                                self.global_error("No valid MONITOR section is input in the definition file")

                """Check if there are any inputs/devices not connected/used"""
                if not self.network.check_network():
                    self.global_error("Exist inputs that are not connected")
                if len(self.devices_list)>0:
                    self.global_error("Exist devices that are not used")

                """Return boolean value: if no error -> True; else -> False"""
                return not self.scanner.error_count


            if self.cur_symbol.type == self.scanner.HEADING:
                """If a heading is read in"""

                if self.cur_symbol.id == self.scanner.DEVICE_ID:
                    """DEVICE"""
                    self.read()
                    """Check for colon"""
                    if self.cur_symbol.type != self.scanner.COLON:
                        self.error("A colon is expected after DEVICE", self.cur_symbol)
                        self.skip_line()
                        line_num += 1
                        continue

                    """Expect device assignments in this section"""
                    expect_device = True
                    expect_connection = False
                    expect_monitor = False

                    """Check the order: DEVICE should be placed before CONNECTION and MONITOR"""
                    if (not device_section) and (not connection_section) and (not monitor_section):
                        device_section = True

                    else:
                        device_wrong_place = True


                        if device_section:
                            """Check for repeat declaration of DEVICE"""
                            self.error("There are multiple DEVICE sections detected in the file", self.cur_symbol)

                        else:
                            self.error("Exist CONNECTION/MONITOR section before DEVICE", self.cur_symbol)

                        line_num += 1
                        continue

                elif self.cur_symbol.id == self.scanner.CONNECTION_ID:
                    """CONNECTION"""
                    self.read()
                    """Check for colon"""
                    if self.cur_symbol.type != self.scanner.COLON:
                        self.error("A colon is expected after CONNECTION", self.cur_symbol)
                        self.skip_line()
                        line_num += 1
                        continue

                    """Expect connection assignments in this section"""
                    expect_device = False
                    expect_connection = True
                    expect_monitor = False

                    """Check the order: CONNECTION should be placed between DEVICE and MONITOR"""
                    if (device_section) and (not connection_section) and (not monitor_section):
                        connection_section = True

                    else:
                        connection_wrong_place = True

                        if not device_section:
                            """Check whether DEVICE exist"""
                            self.error("There is no DEVICE stated before CONNECTION", self.cur_symbol)

                        elif connection_section:
                            """Check for repeat declaration of CONNECTION"""
                            self.error("There are multiple CONNECTION sections detected in the file", self.cur_symbol)

                        else:
                            """The only possibility is that MONITOR is placed before CONNECTION"""
                            self.error("Exist MONITOR section before CONNECTION", self.cur_symbol)

                        line_num += 1
                        continue

                elif self.cur_symbol.id == self.scanner.MONITOR_ID:
                    """MONITOR"""
                    self.read()
                    """Check for colon"""
                    if self.cur_symbol.type != self.scanner.COLON:
                        self.error("A colon is expected after MONITOR", self.cur_symbol)
                        self.skip_line()
                        line_num += 1
                        continue

                    """Expect monitor assignments in this section"""
                    expect_device = False
                    expect_connection = False
                    expect_monitor = True

                    """Check the order: MONITOR should be placed after DEVICE and CONNECTION"""
                    if (device_section) and (connection_section) and (not monitor_section):
                        monitor_section = True

                    else:
                        monitor_wrong_place = True

                        if not device_section:
                            """Check whether DEVICE exist"""
                            self.error("There is no DEVICE stated before MONITOR", self.cur_symbol)
                        elif not connection_section:
                            """Check whether CONNECTION exist"""
                            self.error("There is no CONNECTION stated before MONITOR", self.cur_symbol)
                        else:
                            """Check for repeat declaration of MONITOR"""
                            self.error("There are multiple MONITOR sections detected in the file", self.cur_symbol)

                        line_num += 1
                        continue


            elif self.cur_symbol.type == self.scanner.KEYWORD:
                """If a keyword is read in"""


                if (self.cur_symbol.id in self.devices.gate_types) or (self.cur_symbol.id in self.devices.device_types):
                    """Device assignment"""

                    if expect_device:
                        """Check whether the device assignment is in DEVICE section"""

                        eromsg, symbol = self.build_device()
                        """If there is error when building the device, skip line"""
                        if eromsg:
                            self.error(eromsg, symbol)
                            self.skip_line()
                            line_num += 1
                            continue
                        #print(self.devices_list)
                    else:
                        self.error("The device assignment is not in a valid DEVICE section", self.cur_symbol)
                        self.skip_line()
                        line_num += 1
                        continue

                elif self.cur_symbol.id == self.scanner.CON_ID:
                    """Connection assignment"""

                    if expect_connection:
                        """Check whether the connection assignment is in CONNECTION section"""

                        eromsg, symbol = self.build_connect()
                        """If there is error when building the connection, skip line"""
                        if eromsg:
                            self.error(eromsg, symbol)
                            self.skip_line()
                            line_num += 1
                            continue
                    else:
                        self.error("The con assignment is not in a valid CONNECTION section", self.cur_symbol)
                        self.skip_line()
                        line_num += 1
                        continue

                elif self.cur_symbol.id == self.scanner.MON_ID:
                    """Monitor assignment"""

                    if expect_monitor:
                        """Check whether the monitor assignment is in MONITOR section"""

                        eromsg, symbol = self.build_monitor()
                        """If there is error when building the monitor, skip line"""
                        if eromsg:
                            self.error(eromsg, symbol)
                            self.skip_line()
                            line_num += 1
                            continue
                    else:
                        self.error("The mon assignment is not in a valid MONITOR section", self.cur_symbol)
                        self.skip_line()
                        line_num += 1
                        continue

            else:
                self.error("Detect an invalid keyword is input, please input a HEADING or a KEYWORD", self.cur_symbol)
                self.skip_line()
                line_num += 1
                continue

            line_num += 1

    def build_device(self):
        """Start building device"""
        """Initialise error message"""
        eromsg = None

        if self.cur_symbol.id == self.devices.CLOCK:
            """Building CLOCK"""

            """Matching syntax with EBNF"""
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
                return eromsg, self.cur_symbol
            name_symbol = self.cur_symbol
            id = self.cur_symbol.id

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                eromsg = "Expect equal sign"
                return eromsg, self.cur_symbol

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                eromsg = "Expect a clock period here, which should be a number"
                return eromsg, self.cur_symbol
            num_symbol = self.cur_symbol
            num = int(self.names.get_name_string(self.cur_symbol.id))

            self.read()
            if self.cur_symbol.type != self.scanner.SEMICOLON:
                eromsg = "Expect stopping sign"
                return eromsg, self.cur_symbol

            """Start building CLOCK, ready to handle any errors raised by devices"""
            return_error = self.devices.make_device(id, self.devices.CLOCK, num)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg, name_symbol
            elif return_error == self.devices.INVALID_QUALIFIER:
                eromsg = "Expect clock period to be larger than 0"
                return eromsg, num_symbol
            else:
                """Successfully built"""
                self.devices_list.add(id)
                return eromsg, self.cur_symbol

        elif self.cur_symbol.id == self.devices.SWITCH:
            """Building SWITCH"""

            """Matching syntax with EBNF"""
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
                return eromsg, self.cur_symbol
            name_symbol = self.cur_symbol
            id = self.cur_symbol.id

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                eromsg = "Expect equal sign"
                return eromsg, self.cur_symbol

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                eromsg = "Expect a switch state here, which should be a number"
                return eromsg, self.cur_symbol
            num_symbol = self.cur_symbol
            num = int(self.names.get_name_string(self.cur_symbol.id))

            self.read()
            if self.cur_symbol.type != self.scanner.SEMICOLON:
                eromsg = "Expect stopping sign"
                return eromsg, self.cur_symbol

            """Start building SWITCH, ready to handle any errors raised by devices"""
            return_error = self.devices.make_device(id, self.devices.SWITCH, num)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg, name_symbol
            elif return_error == self.devices.INVALID_QUALIFIER:
                eromsg = "Expect switch state should be 0(low) 1(high)"
                return eromsg, num_symbol
            else:
                """Successfully built"""
                # test: print(self.devices.get_device(id).switch_state)
                self.devices_list.add(id)
                return eromsg, self.cur_symbol

        elif self.cur_symbol.id == self.devices.D_TYPE:
            """Building DTYPE"""

            """Matching syntax with EBNF"""
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
                return eromsg, self.cur_symbol
            name_symbol = self.cur_symbol
            id = self.cur_symbol.id

            self.read()
            if self.cur_symbol.type != self.scanner.SEMICOLON:
                eromsg = "Expect stopping sign"
                return eromsg, self.cur_symbol

            """Start building DTYPE, ready to handle any errors raised by devices"""
            return_error = self.devices.make_device(id, self.devices.D_TYPE)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg, name_symbol
            else:
                """Successfully built"""
                self.devices_list.add(id)
                return eromsg, self.cur_symbol

        elif self.cur_symbol.id == self.devices.SIGGEN:
            """Building SIGGEN"""

            """Matching syntax with EBNF"""
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
                return eromsg, self.cur_symbol
            name_symbol = self.cur_symbol
            id = self.cur_symbol.id

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                eromsg = "Expect equal sign"
                return eromsg, self.cur_symbol

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                eromsg = "Expect a sequence of signal values composed of 0(low) and/or 1(high), which should be a number, example: 110011"
                return eromsg, self.cur_symbol
            signal_list = str(int(self.names.get_name_string(self.cur_symbol.id)))
            for signal in signal_list:
                if int(signal) > 1:
                    eromsg = "Invalid signal value, please enter 0 for low and 1 for high signal"
                    return eromsg, self.cur_symbol

            self.read()
            if self.cur_symbol.type != self.scanner.SEMICOLON:
                eromsg = "Expect stopping sign"
                return eromsg, self.cur_symbol

            """Start building SIGGEN, ready to handle any errors raised by devices"""
            return_error = self.devices.make_device(id, self.devices.SIGGEN, signal_list)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg, name_symbol
            else:
                """Successfully built"""
                self.devices_list.add(id)
                return eromsg, self.cur_symbol

        elif self.cur_symbol.id == self.devices.RC:
            """Building RC"""

            """Matching syntax with EBNF"""
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
                return eromsg, self.cur_symbol
            name_symbol = self.cur_symbol
            id = self.cur_symbol.id

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                eromsg = "Expect equal sign"
                return eromsg, self.cur_symbol

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                eromsg = "Expect RC period to be a number"
                return eromsg, self.cur_symbol
            num_symbol = self.cur_symbol
            num = int(self.names.get_name_string(self.cur_symbol.id))

            self.read()
            if self.cur_symbol.type != self.scanner.SEMICOLON:
                eromsg = "Expect stopping sign"
                return eromsg, self.cur_symbol

            """Start building RC, ready to handle any errors raised by devices"""
            return_error = self.devices.make_device(id, self.devices.RC, num)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg, name_symbol
            elif return_error == self.devices.INVALID_QUALIFIER:
                eromsg = "Expect RC period should be larger than 0"
                return eromsg, num_symbol
            else:
                """Successfully built"""
                self.devices_list.add(id)
                return eromsg, self.cur_symbol

        elif self.cur_symbol.id == self.devices.XOR:
            """Building XOR"""

            """Matching syntax with EBNF"""
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
                return eromsg, self.cur_symbol
            name_symbol = self.cur_symbol
            id = self.cur_symbol.id

            self.read()
            if self.cur_symbol.type != self.scanner.SEMICOLON:
                eromsg = "Expect stopping sign"
                return eromsg, self.cur_symbol

            """Start building XOR, ready to handle any errors raised by devices"""
            return_error = self.devices.make_device(id, self.devices.XOR)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg, name_symbol
            else:
                """Successfully built"""
                self.devices_list.add(id)
                return eromsg, self.cur_symbol

        elif self.cur_symbol.id in self.devices.gate_types:
            """Building other gates"""

            """Matching syntax with EBNF"""
            """Find gate type"""
            type = self.cur_symbol.id

            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
                return eromsg, self.cur_symbol
            name_symbol = self.cur_symbol
            id = self.cur_symbol.id

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                eromsg = "Expect equal sign"
                return eromsg, self.cur_symbol

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                eromsg = "Expect number of input pins to be number"
                return eromsg, self.cur_symbol
            num_symbol = self.cur_symbol
            num = int(self.names.get_name_string(self.cur_symbol.id))

            self.read()
            if self.cur_symbol.type != self.scanner.SEMICOLON:
                eromsg = "Expect stopping sign"
                return eromsg, self.cur_symbol

            """Start building gates, ready to handle any errors raised by devices"""
            return_error = self.devices.make_device(id, type, num)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg, name_symbol
            elif return_error == self.devices.INVALID_QUALIFIER:
                eromsg = "Number of pins out of range"
                return eromsg, num_symbol
            else:
                """Successfully built"""
                self.devices_list.add(id)
                return eromsg, self.cur_symbol

    def build_connect(self):
        """Start building connect"""
        """Initialise error message"""
        eromsg = None

        self.read()
        if self.cur_symbol.type != self.scanner.NAME:
            eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
            return eromsg, self.cur_symbol
        output_device = self.devices.get_device(self.cur_symbol.id)
        if output_device is None:
            eromsg = "The device to be connected is not defined"
            return eromsg, self.cur_symbol

        if output_device.device_kind == self.devices.D_TYPE:
            """Check if the output device is DTYPE"""

            """exact_read because white spaces cannot be ignored here"""
            self.exact_read()
            if self.cur_symbol.type != self.scanner.DOT:
                eromsg = "DTYPE is used as the output device, a dot (followed by a pinname) is expected here"
                return eromsg, self.cur_symbol

            self.exact_read()
            if self.cur_symbol.id not in self.devices.dtype_output_ids:
                eromsg = "DTYPE is used as the output device, a pinname Q/QBAR is required here"
                return eromsg, self.cur_symbol

            outputpin = self.cur_symbol.id

        else:
            """Output device does not have a output pinname"""
            outputpin = None

        self.read()
        if self.cur_symbol.type != self.scanner.ARROW:
            eromsg = "An arrow is expected after the output device/pin"
            return eromsg, self.cur_symbol

        self.read()
        if self.cur_symbol.type != self.scanner.NAME:
            eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
            return eromsg, self.cur_symbol

        input_device = self.devices.get_device(self.cur_symbol.id)
        if input_device is None:
            eromsg = "The device to be connected is not defined"
            return eromsg, self.cur_symbol

        self.exact_read()
        if self.cur_symbol.type != self.scanner.DOT:
            eromsg = "For input device, a dot (followed by a pinname) is expected here"
            return eromsg, self.cur_symbol

        """Check whether the pinname is valid"""
        self.exact_read()
        if self.cur_symbol.type not in self.scanner.pin_id:
            eromsg = "For input device, a valid pinname is expected here"
            return eromsg, self.cur_symbol
        if self.cur_symbol.id not in input_device.inputs:
            eromsg = "This pin name is not valid for this device"
            return eromsg, self.cur_symbol
        inputpin_symbol = self.cur_symbol
        inputpin = self.cur_symbol.id

        self.read()
        if self.cur_symbol.type != self.scanner.SEMICOLON:
            eromsg = "Expect stopping sign"
            return eromsg, self.cur_symbol

        return_error = self.network.make_connection(output_device.device_id, outputpin, input_device.device_id, inputpin)
        if return_error == self.network.INPUT_CONNECTED:
            eromsg = "An input is already connected"
            return eromsg, inputpin_symbol
        elif return_error == self.network.NO_ERROR:
            """Successfully built"""
            self.devices_list.discard(output_device.device_id)
            return eromsg, self.cur_symbol

    def build_monitor(self):
        """Start building monitor"""
        """Initialise error message"""
        eromsg = None

        self.read()
        if self.cur_symbol.type != self.scanner.NAME:
            eromsg = "The input is not a valid name, a valid name is of the form letter, {letter | digit}, and cannot be a PINNAME, KEYWORD, HEADING"
            return eromsg, self.cur_symbol
        monitor_device = self.devices.get_device(self.cur_symbol.id)
        if monitor_device is None:
            eromsg = "The device to be monitored is not defined"
            return eromsg, self.cur_symbol

        if monitor_device.device_kind == self.devices.D_TYPE:
            """exact_read because white spaces cannot be ignored here"""
            self.exact_read()
            if self.cur_symbol.type != self.scanner.DOT:
                eromsg = "DTYPE is to be monitored, a dot (followed by a pinname) is expected here"
                return eromsg, self.cur_symbol

            self.exact_read()
            if self.cur_symbol.id not in self.devices.dtype_output_ids:
                eromsg = "DTYPE is to be monitored, a pinname Q/QBAR is required here"
                return eromsg, self.cur_symbol

            outputpin = self.cur_symbol.id
        else:
            outputpin = None
        outputpin_symbol = self.cur_symbol

        self.read()
        if self.cur_symbol.type != self.scanner.SEMICOLON:
            eromsg = "Expect stopping sign"
            return eromsg, self.cur_symbol

        return_error = self.monitors.make_monitor(monitor_device.device_id, outputpin)
        if return_error == self.monitors.NOT_OUTPUT:
            eromsg = "The pinname to be monitored is not valid for this device"
            return eromsg, outputpin_symbol
        elif return_error == self.monitors.MONITOR_PRESENT:
            eromsg = "The device/pin is already monitored"
            return eromsg, outputpin_symbol
        else:
            """Successfully built"""
            self.devices_list.discard(monitor_device.device_id)
            return eromsg, self.cur_symbol

    def global_error(self, eromsg):
        """return the global error (no error pointer in error message)"""
        print("Error", self.scanner.error_count+1, ":")
        self.scanner.display_global_error(eromsg)

    def error(self, eromsg, symbol):
        """return the common error (error pointer in error message)"""
        print("Error", self.scanner.error_count+1, ":")
        self.scanner.display_error(eromsg, symbol)

    def read(self):
        """get the next non-white space/comment symbol"""
        self.cur_symbol = self.scanner.get_symbol()

    def exact_read(self):
        """get the next non-comment symbol"""
        self.cur_symbol = self.scanner.get_exact_symbol()
