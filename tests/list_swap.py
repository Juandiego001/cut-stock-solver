numeros_originales = [7, 12, 3, 4, 5, 6]
n = len(numeros_originales)

for i in range(n - 1):
    numero_a_intercambiar = numeros_originales[i]
    print(
        f"--- Intercambios para el número {numero_a_intercambiar} (posición {i+1}) ---\n")

    for j in range(i + 1, n):
        arreglo_temporal = list(numeros_originales)
        arreglo_temporal[i], arreglo_temporal[j] = arreglo_temporal[j], arreglo_temporal[i]
        print(arreglo_temporal)

    print("\n" + "="*45 + "\n")
