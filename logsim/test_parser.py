import pytest
from parse import Parser
from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner


def initialization(text_file):
    names = Names()
    devices = Devices(names)
    network = Network(names, devices)
    monitors = Monitors(names, devices, network)
    scanner = Scanner(text_file, names)
    p = Parser(names, devices, network, monitors, scanner)
    return p


# start to test every separate function in parser
# test skip_line
@pytest.mark.parametrize("inputs, outputs", [("pytest_file/t1.txt", "skipped")])
def test_skip_line(inputs, outputs):
    p = initialization(inputs)
    p.read()
    rt_value = p.skip_line()
    assert rt_value == outputs


# test build clock with 0 period
@pytest.mark.parametrize("inputs, outputs", [("pytest_file/t2.txt", 'Expect period to be larger than 0')])
def test_clock(inputs, outputs):
    p = initialization(inputs)
    p.read()
    rt_value = p.build_device()
    assert rt_value[0] == outputs


# test build switch with invalid state
@pytest.mark.parametrize("inputs, outputs", [("pytest_file/t3.txt", "Expect state should be 0(low) 1(high)")])
def test_switch(inputs, outputs):
    p = initialization(inputs)
    p.read()
    rt_value = p.build_device()
    assert rt_value[0] == outputs


# test build device syntax
@pytest.mark.parametrize("inputs, outputs",
                         [("pytest_file/t4.txt", "Expect stopping sign"), ("pytest_file/t5.txt", "A name expected"),
                          ("pytest_file/t6.txt", "Expect equal sign")])
def test_build_device_syntax(inputs, outputs):
    p = initialization(inputs)
    p.read()
    rt_value = p.build_device()
    assert rt_value[0] == outputs


# test build_connect
@pytest.mark.parametrize("inputs, outputs", [("pytest_file/t7.txt", "Device called not defined")])
def test_build_connect(inputs, outputs):
    p = initialization(inputs)
    p.read()
    rt_value = p.build_connect()
    assert rt_value[0] == outputs


# test build_monitor
@pytest.mark.parametrize("inputs, outputs", [("pytest_file/t8.txt", "Device called not defined")])
def test_build_monitor(inputs, outputs):
    p = initialization(inputs)
    p.read()
    rt_value = p.build_connect()
    assert rt_value[0] == outputs


# Overall testing:
@pytest.mark.parametrize("inputs, outputs",
                         [("pytest_file/t9.txt", 0), ("pytest_file/t10.txt", 5), ("pytest_file/t11.txt", 7)])
def test_file(inputs, outputs):
    p = initialization(inputs)
    p.parse_network()
    rt_value = p.scanner.error_count
    assert rt_value == outputs


# Joint testing with team:
@pytest.mark.parametrize("inputs, outputs",
                         [("pytest_file/definition_file_1.txt", 0), ("pytest_file/definition_file_2.txt", 0)])
def test_joint(inputs, outputs):
    p = initialization(inputs)
    p.parse_network()
    rt_value = p.scanner.error_count
    assert rt_value == outputs


