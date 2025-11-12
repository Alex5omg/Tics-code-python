ano = int(input("Introduce un año: "))

if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
    print(f"El año {ano} si es bisiesto.")
else:
    print(f"El año {ano} no es bisiesto.")
