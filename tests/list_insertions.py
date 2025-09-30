def obtener_inserciones_posibles(arreglo_original):
    """
    Genera todos los arreglos resultantes de tomar cada elemento 
    del arreglo original y reinsertarlo en todas las posiciones posibles.
    """
    
    # Usamos un diccionario para almacenar los resultados, donde la clave es el índice del elemento 
    # movido y el valor es una lista de los arreglos resultantes.
    resultados_totales = {}
    
    n = len(arreglo_original)
    
    # 1. Iterar sobre cada elemento del arreglo original para moverlo
    for i in range(n):
        
        elemento_a_mover = arreglo_original[i]
        
        # 2. Crear un arreglo temporal que es el original sin el elemento en la posición 'i'
        # Esto es la lista base donde se insertará el elemento_a_mover
        arreglo_sin_elemento = arreglo_original[:i] + arreglo_original[i+1:]
        
        inserciones_para_elemento = []
        
        # 3. Iterar sobre todas las posibles posiciones de inserción (índices de 0 a n)
        # El tamaño final del arreglo es n, por lo que las posiciones de inserción van de 0 a n
        for j in range(n):
            # Creamos una copia del arreglo_sin_elemento para la inserción
            nuevo_arreglo = arreglo_sin_elemento[:] 
            
            # Insertar el elemento extraído en la posición 'j'
            # Esta es la parte clave: list.insert(índice, valor)
            nuevo_arreglo.insert(j, elemento_a_mover)
            
            # Guardamos el nuevo arreglo resultante
            inserciones_para_elemento.append(nuevo_arreglo)
        
        # 4. Guardar todos los resultados para el elemento que se movió, identificando por su índice original
        resultados_totales[i] = inserciones_para_elemento
            
    return resultados_totales

# Arreglo de ejemplo
mi_arreglo = [7, 12, 3, 4, 5]

# Ejecutar el algoritmo
resultados_completos = obtener_inserciones_posibles(mi_arreglo)

# Imprimir los resultados de forma estructurada
for indice, arreglos in resultados_completos.items():
    print(f"\n--- Elemento movido: {mi_arreglo[indice]} (Índice original: {indice}) ---")
    for arreglo in arreglos:
        print(f"  {arreglo}")