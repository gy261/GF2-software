from scanner import Scanner, Symbol
from names import Names

names = Names()
scanner = Scanner("testfile.txt", names)

# Testing for get_symbol function
"""
for i in range(30):
    a = scanner.get_symbol()
    print("The symbol type and id are", a.type, a.id)
    if a.id:
        print(names.get_name_string(a.id))

scanner.names.display_list()
"""

# Testing for error display
message = "This is a testing error message!"

error_place = 10
for i in range(error_place):
    
    a = scanner.get_symbol()
    print("Symbol",i+1)
    if a.id != None:
        print(names.get_name_string(a.id))

scanner.display_error(message)


"""
for i in range(10):
    a = scanner.get_symbol()
    if a.id != None:
        print(names.get_name_string(a.id))

"""
