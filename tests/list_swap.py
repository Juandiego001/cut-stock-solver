# Tu arreglo original
numeros_originales = [7, 12, 3, 4, 5, 6]
n = len(numeros_originales)

# Iteramos a través de cada número del arreglo (excepto el último)
for i in range(n - 1):
    numero_a_intercambiar = numeros_originales[i]
    print(f"--- Intercambios para el número {numero_a_intercambiar} (posición {i+1}) ---\n")
    
    # Iteramos a través de los números que están a la DERECHA del actual
    for j in range(i + 1, n):
        # Creamos una copia del arreglo original para no modificarlo
        arreglo_temporal = list(numeros_originales)
        
        # Realizamos el intercambio (swap)
        arreglo_temporal[i], arreglo_temporal[j] = arreglo_temporal[j], arreglo_temporal[i]
        
        # Imprimimos el resultado de este intercambio
        print(arreglo_temporal)
        
    print("\n" + "="*45 + "\n")