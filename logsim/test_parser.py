
from parse import Parser
import names, devices, network, monitors, scanner
from userint import UserInterface
names = names.Names()
devices = devices.Devices(names)
network = network.Network(names, devices)
monitors = monitors.Monitors(names, devices, network)

scanner = scanner.Scanner("testfile.txt", names)
p = Parser(names, devices, network, monitors, scanner)

p.parse_network()
