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
        # mute:
        pass
        '''
        if self.cur_symbol.id:
            print(str, self.cur_symbol.type, self.cur_symbol.id, ":", self.names.get_name_string(self.cur_symbol.id))
        else:
            print(str, self.cur_symbol.type, self.cur_symbol.id)
'''
    def skip_section(self):
        while self.cur_symbol.type != self.scanner.SEMICOLON:
            if self.cur_symbol.type == self.scanner.EOF:
                return
            self.read()

    def skip_line(self):
        while (self.cur_symbol.type != self.scanner.SEMICOLON) and (self.cur_symbol.type != self.scanner.COMMA):
            if self.cur_symbol.type == self.scanner.EOF:
                return
            self.read()


    def parse_network(self):
        """Parse the circuit definition file."""
        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        expect_device = False
        expect_connection = False
        expect_monitor = False

        device_section = False
        connection_section = False
        monitor_section = False

        line_num = 0
        # initialization
        self.read()
        while True:
            if line_num > 0:
                self.read()
            self.test("big loop:")

            if self.cur_symbol.type == self.scanner.EOF:
                if not self.network.check_network():
                    self.scanner.display_global_error("Exist inputs not connected")
                return not self.scanner.error_count

            if self.cur_symbol.type == self.scanner.HEADING:
                # check the order: must be Devices, Connections, Monitors
                if self.cur_symbol.id == self.scanner.DEVICE_ID:
                    self.read()
                    if self.cur_symbol.type != self.scanner.COLON:
                        self.error("colon expected")
                        self.skip_section()
                        line_num += 1
                        continue

                    expect_device = True
                    expect_connection = False
                    expect_monitor = False
                    if (not device_section) and (not connection_section) and (not monitor_section):
                        device_section = True

                    else:
                        if device_section:
                            self.error("multiple DEVICE")

                        else:
                            self.error("CONNECTION/MONITOR before DEVICE")
                        self.skip_section()
                        line_num += 1
                        continue

                elif self.cur_symbol.id == self.scanner.CONNECTION_ID:
                    self.read()
                    if self.cur_symbol.type != self.scanner.COLON:
                        self.error("colon expected")
                        self.skip_section()
                        line_num += 1
                        continue

                    expect_device = False
                    expect_connection = True
                    expect_monitor = False
                    if (device_section) and (not connection_section) and (not monitor_section):
                        connection_section = True

                    else:
                        if not device_section:
                            self.error("No DEVICE stated before")
                        elif connection_section:
                            self.error("multiple CONNECTION")
                        else:
                            self.error("MONITOR before CONNECTION")
                        self.skip_section()
                        line_num += 1
                        continue

                elif self.cur_symbol.id == self.scanner.MONITOR_ID:
                    self.read()
                    if self.cur_symbol.type != self.scanner.COLON:
                        self.error("colon expected")
                        self.skip_section()
                        line_num += 1
                        continue

                    expect_device = False
                    expect_connection = False
                    expect_monitor = True
                    if (device_section) and (connection_section) and (not monitor_section):
                        monitor_section = True

                    else:
                        if not device_section:
                            self.error("No DEVICE stated before")
                        elif not connection_section:
                            self.error("No CONNECTION stated before")
                        else:
                            self.error("multiple MONITOR")
                        self.skip_section()
                        line_num += 1
                        continue

            elif self.cur_symbol.type == self.scanner.KEYWORD:
                # check expect or not
                if (self.cur_symbol.id in self.devices.gate_types) or (self.cur_symbol.id in self.devices.device_types):
                    if expect_device:
                        eromsg = self.build_device()
                        if eromsg:
                            self.error(eromsg)
                            self.skip_line()
                            line_num += 1
                            continue
                    else:
                        self.error("device assignment not in DEVICE section")
                        self.skip_line()
                        line_num += 1
                        continue

                elif self.cur_symbol.id == self.scanner.CON_ID:
                    if expect_connection:
                        eromsg = self.build_connect()
                        if eromsg:
                            self.error(eromsg)
                            self.skip_line()
                            line_num += 1
                            continue
                    else:
                        self.error("con assignment not in CONNECTION section")
                        self.skip_line()
                        line_num += 1
                        continue

                elif self.cur_symbol.id == self.scanner.MON_ID:
                    if expect_monitor:
                        eromsg = self.build_monitor()
                        if eromsg:
                            self.error(eromsg)
                            self.skip_line()
                            line_num += 1
                            continue
                    else:
                        self.error("mon assignment not in MONITOR section")
                        self.skip_line()
                        line_num += 1
                        continue


                else:
                    ...



            else:
                self.error("Invalid keyword")
                self.skip_line()
                line_num += 1
                continue

            line_num += 1

    def build_device(self):
        # CLOCK / SWITCH a = 0;
        # Gate g1;

        eromsg = None
        if self.cur_symbol.id == self.devices.CLOCK:
            #print("building clock")
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                eromsg = "A name expected"
                return eromsg
            id = self.cur_symbol.id
            #self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                eromsg = "Expect equal sign"
                return eromsg
            #self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                eromsg = "Expect period to be number"
                return eromsg
            num = int(self.names.get_name_string(self.cur_symbol.id))
            #self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                eromsg = "Expect stopping sign"
                return eromsg
            #self.test()

            return_error = self.devices.make_device(id, self.devices.CLOCK, num)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg
            elif return_error == self.devices.INVALID_QUALIFIER:
                eromsg = "Expect period to be larger than 0"
                return eromsg
            else:
                #successful
                return eromsg

        elif self.cur_symbol.id == self.devices.SWITCH:
            #print("building switch")
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                eromsg = "A name expected"
                return eromsg
            id = self.cur_symbol.id
            # self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                eromsg = "Expect equal sign"
                return eromsg
            # self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                eromsg = "Expect period to be number"
                return eromsg
            num = int(self.names.get_name_string(self.cur_symbol.id))
            # self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                eromsg = "Expect stopping sign"
                return eromsg
            # self.test()

            return_error = self.devices.make_device(id, self.devices.SWITCH, num)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg
            elif return_error == self.devices.INVALID_QUALIFIER:
                eromsg = "Expect state should be 0(low) 1(high)"
                return eromsg
            else:
                # successful
                return eromsg

        elif self.cur_symbol.id == self.devices.D_TYPE:
            #print("building dtype")
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                eromsg = "A name expected"
                return eromsg
            id = self.cur_symbol.id
            # self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                eromsg = "Expect stopping sign"
                return eromsg
            # self.test()

            return_error = self.devices.make_device(id, self.devices.D_TYPE)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsgc = "Name has been used"
                return eromsg
            else:
                # successful
                return eromsg

        elif self.cur_symbol.id == self.devices.XOR:
            #print("building XOR")
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                eromsg = "A name expected"
                return eromsg
            id = self.cur_symbol.id
            # self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                eromsg = "Expect stopping sign"
                return eromsg
            # self.test()

            return_error = self.devices.make_device(id, self.devices.XOR)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg
            else:
                # successful
                return eromsg

        elif self.cur_symbol.id in self.devices.gate_types:
            type = self.cur_symbol.id
            #print("building", self.names.get_name_string(type))
            self.read()
            if self.cur_symbol.type != self.scanner.NAME:
                # check if name has already been used
                eromsg = "A name expected"
                return eromsg
            id = self.cur_symbol.id
            # self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.EQUAL:
                eromsg = "Expect equal sign"
                return eromsg
            # self.test()

            self.read()
            if self.cur_symbol.type != self.scanner.NUMBER:
                eromsg = "Expect number of input pins to be number"
                return eromsg
            num = int(self.names.get_name_string(self.cur_symbol.id))
            # self.test()

            self.read()
            if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
                eromsg = "Expect stopping sign"
                return eromsg
            # self.test()

            return_error = self.devices.make_device(id, type, num)
            if return_error == self.devices.DEVICE_PRESENT:
                eromsg = "Name has been used"
                return eromsg
            elif return_error == self.devices.INVALID_QUALIFIER:
                eromsg = "number of pins out of range"
                return eromsg
            else:
                # successful
                #print(self.devices.devices_list)
                return eromsg


    def build_connect(self):
        # CON g1[.Q] -> g2.I2;
        #print("build connection...")
        eromsg = None
        self.read()
        if self.cur_symbol.type != self.scanner.NAME:
            eromsg = "output device name required"
            return eromsg
        output_device = self.devices.get_device(self.cur_symbol.id)
        if output_device is None:
            eromsg = "Device called not defined"
            return eromsg

        if output_device.device_kind == self.devices.D_TYPE:
            self.exact_read()
            if self.cur_symbol.type != self.scanner.DOT:
                eromsg = "dot required here"
                return eromsg

            self.exact_read()
            if self.cur_symbol.id not in self.devices.dtype_output_ids:
                eromsg = "Q/QBAR required for DTYPE"
                return eromsg

            outputpin = self.cur_symbol.id
        else:
            outputpin = None

        self.read()
        if self.cur_symbol.type != self.scanner.ARROW:
            eromsg = "Arrow expected"
            return eromsg

        self.read()
        self.test()
        if self.cur_symbol.type != self.scanner.NAME:
            eromsg = "input device name required"
            return eromsg

        input_device = self.devices.get_device(self.cur_symbol.id)
        #print(input_device.device_id)

        self.exact_read()
        if self.cur_symbol.type != self.scanner.DOT:
            eromsg = "pin name required: need dot here"
            return eromsg

        self.exact_read()
        if self.cur_symbol.type not in self.scanner.pin_id:
            eromsg = "pin name required: need a pinname here"
            return eromsg
        if self.cur_symbol.id not in input_device.inputs:
            eromsg = "pin name not valid for this device"
            return eromsg
        inputpin = self.cur_symbol.id

        self.read()
        if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
            eromsg = "Expect stopping sign"
            return eromsg

        return_error = self.network.make_connection(output_device.device_id, outputpin, input_device.device_id, inputpin)
        if return_error == self.network.INPUT_CONNECTED:
            eromsg = "input already connected"
            return eromsg
        elif return_error == self.network.NO_ERROR:
            # successful
            return eromsg
        else:
            eromsg = "check this error"
            return eromsg


    def build_monitor(self):
        # MON g1[.Q/QBAR];
        eromsg = None
        #print("build monitor...")
        self.read()
        if self.cur_symbol.type != self.scanner.NAME:
            eromsg = "monitor device name required"
            return eromsg
        monitor_device = self.devices.get_device(self.cur_symbol.id)
        if monitor_device is None:
            eromsg = "Device called not defined"
            return eromsg

        if monitor_device.device_kind == self.devices.D_TYPE:
            self.exact_read()
            if self.cur_symbol.type != self.scanner.DOT:
                eromsg = "dot required here"
                return eromsg

            self.exact_read()
            if self.cur_symbol.id not in self.devices.dtype_output_ids:
                eromsg = "Q/QBAR required for DTYPE"
                return eromsg

            outputpin = self.cur_symbol.id
        else:
            outputpin = None

        self.read()
        if (self.cur_symbol.type != self.scanner.COMMA) and (self.cur_symbol.type != self.scanner.SEMICOLON):
            eromsg = "Expect stopping sign"
            return eromsg

        return_error = self.monitors.make_monitor(monitor_device.device_id, outputpin)
        if return_error == self.monitors.NOT_OUTPUT:
            eromsg = "output pin not valid"
            return eromsg
        elif return_error == self.monitors.MONITOR_PRESENT:
            eromsg = "monitor already in"
            return eromsg
        else:
            return eromsg

    def error(self, eromsg):
        self.scanner.display_error(eromsg, self.cur_symbol)

    def read(self):
        self.cur_symbol = self.scanner.get_symbol()

    def exact_read(self):
        self.cur_symbol = self.scanner.get_exact_symbol()


















