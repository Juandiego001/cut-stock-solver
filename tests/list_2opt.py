def generar_permutaciones_2opt(arreglo_original):
    """
    Genera todas las permutaciones posibles de 2-opt (inversión de segmento)
    a partir de un arreglo.

    Args:
        arreglo_original (list): La lista inicial de números.

    Returns:
        list: Una lista de todos los arreglos resultantes de aplicar la operación 2-opt.
    """
    
    n = len(arreglo_original)
    permutaciones = []
    
    # 1. 'i' es el inicio del segmento a invertir (excluyendo el primer elemento, i.e., de 0 a n-2)
    for i in range(n - 1):
        
        # 2. 'k' es el final del segmento a invertir. 
        # Debe ser mayor que 'i' y puede llegar hasta n-1 (el último elemento).
        for k in range(i + 1, n):
            
            # 3. Aplicar la operación 2-opt
            
            # a) Copiar el inicio del arreglo (desde el principio hasta i-1)
            # Si i es 0, esta parte es vacía.
            segmento_inicio = arreglo_original[:i]
            
            # b) Invertir el segmento (desde i hasta k, ambos inclusive)
            # Usamos slicing [::-1] para invertir la sub-lista.
            segmento_a_invertir = arreglo_original[i:k+1]
            segmento_invertido = segmento_a_invertir[::-1]
            
            # c) Copiar el final del arreglo (desde k+1 hasta el final)
            # Si k es n-1, esta parte es vacía.
            segmento_final = arreglo_original[k+1:]
            
            # 4. Construir el nuevo arreglo
            nuevo_arreglo = segmento_inicio + segmento_invertido + segmento_final
            
            # 5. Almacenar el resultado (si no es el mismo arreglo original)
            # Una inversión de 2 elementos ([i, i+1]) resulta en el mismo arreglo si se incluyen
            # los segmentos inicial y final. Por ejemplo, si i=0 y k=1: [A, B] -> [B, A].
            # Para evitar duplicados y el propio arreglo inicial, se puede añadir una verificación,
            # pero para generar TODAS las posibilidades, las incluiremos.
            
            # El caso trivial (i=0, k=n-1) es el arreglo invertido completamente.
            # Los casos donde i y k son adyacentes (k = i+1) son las transposiciones más simples.

            if nuevo_arreglo != arreglo_original:
                 permutaciones.append(nuevo_arreglo)
            
    # Además de las permutaciones generadas, podrías querer incluir el original 
    # como punto de partida si se estuviera buscando una mejora (como en TSP).
    # Sin embargo, siguiendo la lógica de generar *nuevos* arreglos, lo omitimos.
    
    return permutaciones

# Arreglo de ejemplo
mi_arreglo = [7, 12, 3, 4, 5, 6]

# Ejecutar el algoritmo
permutaciones_2opt = generar_permutaciones_2opt(mi_arreglo)

# Imprimir los resultados
print(f"Arreglo original: {mi_arreglo}")
print(f"Número total de permutaciones 2-opt: {len(permutaciones_2opt)}")
print("\n--- Primeras 10 permutaciones 2-opt generadas ---")
for i, arreglo in enumerate(permutaciones_2opt):
    print(f"  {i+1}: {arreglo}")