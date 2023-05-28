from scanner import Scanner, Symbol
from names import Names

names = Names()
scanner = Scanner("testfile.txt", names)

for i in range(60):
    a = scanner.get_symbol()
    print("The symbol type and id are", a.type, a.id)
    if a.id:
        print(names.get_name_string(a.id))

scanner.names.display_list()