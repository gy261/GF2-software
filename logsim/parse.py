"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""

from names import Names

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

        self.cur_symbol = None



    def test(self, str=""):
        print(str, self.cur_symbol.type, self.cur_symbol.id)
        if self.cur_symbol.id:
            print(self.names.get_name_string(self.cur_symbol.id))
    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        expect_device = False
        expect_connection = False
        expect_monitor = False

        line_num = 0
        # initialization
        self.read()
        while True:
            if line_num > 0:
                self.read()
            self.test("big loop:")

            if self.cur_symbol.type == self.scanner.EOF:
                return not self.scanner.error_count

            if self.cur_symbol.type == self.scanner.HEADING:
                # check the order: must be Devices, Connections, Monitors
                if self.cur_symbol.id == self.scanner.DEVICE_ID:
                    self.read()
                    if self.cur_symbol.type != self.scanner.COLON:
                        self.error("colon expected")

                    if (not expect_device) and (not expect_connection) and (not expect_monitor):
                        expect_device = True
                        pass

                    else:
                        # multiple device?
                        # device after connection/monitor?
                        # self.scanner.error_count += 1
                        self.error("")

                        # ignore the whole Device section

                elif self.cur_symbol.id == self.scanner.CONNECTION_ID:
                    ...
                else:
                    ...
                # check if colon exists: ":"

            elif self.cur_symbol.type == self.scanner.KEYWORD:
                # check expect or not
                if (self.cur_symbol.id in self.devices.gate_types) or (self.cur_symbol.id in self.devices.device_types):
                    if expect_device:
                        self.build_device()

                elif self.cur_symbol.id == self.scanner.CON_ID:
                    if expect_connection:
                        self.build_connect()
                        ...

                elif self.cur_symbol.id == self.scanner.MON_ID:
                    if expect_monitor:
                        #self.build_monitor()
                        ...

                else:
                    ...



            else:
                self.error("Invalid assignment")

            line_num += 1




    def build_device(self):
        # CLOCK / SWITCH a = 0;
        # Gate g1;

        if self.cur_symbol.id == self.devices.CLOCK:
            print("building clock")
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                self.error("A name expected")
                # return
            id = self.cur_symbol.id
            #self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                self.error("Expect equal sign")
            #self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                self.error("Expect period to be number")
            num = int(self.names.get_name_string(self.cur_symbol.id))
            #self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                self.error("Expect stopping sign")
            #self.test()

            return_error = self.devices.make_device(id, self.devices.CLOCK, num)
            if return_error == self.devices.DEVICE_PRESENT:
                self.error("Name has been used")
            elif return_error == self.devices.INVALID_QUALIFIER:
                self.error("Expect period to be larger than 0")
            else:
                #successful
                return

        elif self.cur_symbol.id == self.devices.SWITCH:
            print("building switch")
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                self.error("A name expected")
                # return
            id = self.cur_symbol.id
            # self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                self.error("Expect equal sign")
            # self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                self.error("Expect period to be number")
            num = int(self.names.get_name_string(self.cur_symbol.id))
            # self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                self.error("Expect stopping sign")
            # self.test()

            return_error = self.devices.make_device(id, self.devices.SWITCH, num)
            if return_error == self.devices.DEVICE_PRESENT:
                self.error("Name has been used")
            elif return_error == self.devices.INVALID_QUALIFIER:
                self.error("Expect state should be 0(low) 1(high)")
            else:
                # successful
                return

        elif self.cur_symbol.id == self.devices.D_TYPE:
            print("building dtype")
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                self.error("A name expected")
                # return
            id = self.cur_symbol.id
            # self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                self.error("Expect stopping sign")
            # self.test()

            return_error = self.devices.make_device(id, self.devices.D_TYPE)
            if return_error == self.devices.DEVICE_PRESENT:
                self.error("Name has been used")
            else:
                # successful
                return

        elif self.cur_symbol.id == self.devices.XOR:
            print("building XOR")
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                self.error("A name expected")
                # return
            id = self.cur_symbol.id
            # self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                self.error("Expect stopping sign")
            # self.test()

            return_error = self.devices.make_device(id, self.devices.XOR)
            if return_error == self.devices.DEVICE_PRESENT:
                self.error("Name has been used")
            else:
                # successful
                return

        elif self.cur_symbol.id in self.devices.gate_types:
            print("building", self.names.get_name_string(self.cur_symbol.id))
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                self.error("A name expected")
                # return
            id = self.cur_symbol.id
            # self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                self.error("Expect equal sign")
            # self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                self.error("Expect number of input pins to be number")
            num = int(self.names.get_name_string(self.cur_symbol.id))
            # self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                self.error("Expect stopping sign")
            # self.test()

            return_error = self.devices.make_device(id, self.cur_symbol.id, num)
            if return_error == self.devices.DEVICE_PRESENT:
                self.error("Name has been used")
            elif return_error == self.devices.INVALID_QUALIFIER:
                self.error("number of pins out of range")
            else:
                # successful
                return


    def build_connect(self):
        # CON g1[.Q] -> g2.I2;
        print("build connection...")
        self.read()
        if self.cur_symbol.type != self.scanner.NAME:
            self.error("output device name required")
        output_device = self.devices.get_device(self.cur_symbol.id)
        if output_device is None:
            self.error("Device called not defined")

        if output_device.device_kind == self.devices.D_TYPE:
            self.exact_read()
            if self.cur_symbol.type != self.scanner.DOT:
                self.error("dot required here")

            self.exact_read()
            if self.cur_symbol.id not in self.devices.dtype_output_ids:
                self.error("Q/QBAR required for DTYPE")

            outputpin = self.cur_symbol.id
        else:
            outputpin = None

        self.read()
        if self.cur_symbol.type != self.scanner.ARROW:
            self.error("Arrow expected")

        self.read()
        if self.cur_symbol.type != self.scanner.NAME:
            self.error("input device name required")
        input_device = self.devices.get_device(self.cur_symbol.id)

        self.exact_read()
        if self.cur_symbol.type != self.scanner.DOT:
            self.error("pin name required: need dot here")

        self.exact_read()
        if self.cur_symbol.type not in self.scanner.pin_list:
            self.error("pin name required: need a pinname here")
        if self.cur_symbol.id not in input_device.inputs:
            self.error("pin name not valid for this device")
        inputpin = self.cur_symbol.id

        self.read()
        if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
            self.error("Expect stopping sign")

        return_error = self.network.make_connection(output_device.device_id, outputpin, input_device.device_id, inputpin)
        if return_error == self.network.INPUT_CONNECTED:
            self.error("input already connected")
        elif return_error == self.network.NO_ERROR:
            # successful
            return
        else:
            self.error("check this error")


    def build_monitor(self):
        # MON g1[.Q/QBAR];
        print("build monitor...")
        self.read()
        if self.cur_symbol.type != self.scanner.NAME:
            self.error("monitor device name required")
        monitor_device = self.devices.get_device(self.cur_symbol.id)
        if monitor_device is None:
            self.error("Device called not defined")

        if monitor_device.device_kind == self.devices.D_TYPE:
            self.exact_read()
            if self.cur_symbol.type != self.scanner.DOT:
                self.error("dot required here")

            self.exact_read()
            if self.cur_symbol.id not in self.devices.dtype_output_ids:
                self.error("Q/QBAR required for DTYPE")

            outputpin = self.cur_symbol.id
        else:
            outputpin = None

        self.read()
        if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
            self.error("Expect stopping sign")

        return_error = self.monitors.make_monitor(monitor_device.device_id, outputpin)
        if return_error == self.monitors.NOT_OUTPUT:
            self.error("output pin not valid")
        elif return_error == self.monitors.MONITOR_PRESENT:
            self.error("monitor already in")
        else:
            return

    def skip_error_line(self):
        pass
    def error(self, eromsg):
        print(eromsg)

    def read(self):
        self.cur_symbol = self.scanner.get_symbol()

    def exact_read(self):
        self.cur_symbol = self.scanner.get_symbol()


















