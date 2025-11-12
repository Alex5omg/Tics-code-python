def calcular_pi(iteraciones):
    pi_aprox = 0
    for n in range(iteraciones):
        termino = (-1) ** n / (2 * n + 1)
        pi_aprox += termino
    return 4 * pi_aprox

if __name__ == "__main__":
    iteraciones = int(input("Ingrese el número de iteraciones: "))
    pi = calcular_pi(iteraciones)
    print(f"Aproximación de π con {iteraciones} iteraciones: {pi}")
