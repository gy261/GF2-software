from scanner import Scanner, Symbol
from names import Names

names = Names()
scanner = Scanner("testfile.txt", names)

b = scanner.get_symbol()
print("The symbol type and id are",b.type, b.id)
print(names.get_name_string(b.id))

for i in range(60):
    a = scanner.get_symbol()
    print("The symbol type and id are", a.type, a.id)
    if a.id:
        print(names.get_name_string(a.id))
