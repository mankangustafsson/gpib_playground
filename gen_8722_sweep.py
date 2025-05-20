print("@echo OFF")
for n in range(40):
    print(f".\\vna.py -f {n + 1}G -d -10.0 -p 1")
    print("timeut 1 >nul")
    print(f".\\m6960.py -f {n + 1}G read")
    print()
print("remember to change character encoding to non-UTF")
