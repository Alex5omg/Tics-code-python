def doble_factorial(n):
    if n < 0:
        raise ValueError("El número no puede ser negativo")
    resultado = 1
    
    while n > 0:
        resultado *= n
        n -= 2
    
    return resultado

def main():
    try:
        numero = int(input("Introduce un número para calcular su doble factorial: "))
        print(f"El doble factorial de {numero} es: {doble_factorial(numero)}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()