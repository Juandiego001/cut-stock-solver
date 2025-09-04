import sys
import copy
import math
import random
import numpy as np
from scipy.stats import norm
from classes import Solution, SubEs, Item


def hacer_corte(sub_esp: SubEs, T: int = 0, H: float = 0.0):
    '''Función hacer corte que retorna dos items posterior al corte'''

    ancho: int = sub_esp.ancho
    largo: int = sub_esp.largo
    if T == 0:  # Corte Horizontal -> Se modifica el largo
        largo1: int = largo*H
        largo2: int = largo*(1-H)
        sub_esp1: SubEs = SubEs(ancho, largo1)
        sub_esp2: SubEs = SubEs(ancho, largo2)
    else:  # Corte Vertical -> Se modifica el ancho
        ancho1: int = ancho*H
        ancho2: int = ancho*(1-H)
        sub_esp1: SubEs = SubEs(ancho1, largo)
        sub_esp2: SubEs = SubEs(ancho2, largo)

    return sub_esp1, sub_esp2


def generacion_subespacios(s: Solution, c: int, corte: int = 0, cola: list[SubEs] = [], cortes: list = []):
    '''Función para generar los subespacios'''

    if len(cola) == 2**c:
        return cola, cortes
    else:
        copia_cola = []
        for sub_esp in cola:
            T: int = s.T[corte]
            H: float = s.H[corte]
            sub_esp1, sub_esp2 = hacer_corte(sub_esp, T, H)
            corte += 1
            cortes.append({'h': (sub_esp.largo)*100,
                          'w': (sub_esp.ancho)*100, 'c': {'t': T, 'h': H}})
            copia_cola.append(sub_esp1)
            copia_cola.append(sub_esp2)

        cola = copy.deepcopy(copia_cola)
        return generacion_subespacios(s, c, corte, cola, cortes)


def recorrer_ancho(matrix: list[list], j: int, item: Item):
    '''
    Se recorre como tal cada fila de la matrix, es decir, k será cada elemento de 0's o 1's de la fila
    '''

    c = 0
    ultimo_cero = -1
    primer_cero = -1
    ancho_completado = False

    for i, k in enumerate(matrix[j]):
        if k != 0:
            primer_cero = -1
            c = 0
            continue
        if k == 0 and primer_cero == -1:
            primer_cero = (i, j)
        if k == 0:
            c += 1
        if c == item.ancho:
            ancho_completado = True
            ultimo_cero = (i, j)
            return ancho_completado, primer_cero, ultimo_cero

    return ancho_completado, primer_cero, ultimo_cero


def completar_x_ancho(matrix: list[list], primer_cero: tuple[int, int], ultimo_cero: tuple[int, int], ancho: int, largo: int):
    '''
    Se completa el item en el subespacio recorriendo x ancho a lo largo.

    --->
    [
     xxx  |
     xxx  |
     xxx  v
    ]
    '''

    largo_completado = False
    largos_todos_completados = 0
    for j in range(primer_cero[1] + 1, len(matrix)):
        c = 0
        for i, k in enumerate(matrix[j][primer_cero[0]:]):
            '''
            Si en el proceso de rellenado de la segunda fase se llega a encontrar un 1, no se puede completar la figura con
            la base establecida y se debe continuar con otra posición de ancho/base.
            '''
            if k != 0:
                largo_completado = False
                return largo_completado, ultimo_cero
            c += 1
            if c == ancho:
                largos_todos_completados += 1
                ultimo_cero = (i + primer_cero[0], j)
                break

        if largos_todos_completados == largo - 1:
            largo_completado = True
            return largo_completado, ultimo_cero

    return largo_completado, ultimo_cero


def ubicar_x_dimension(matrix: list[list], j: int, item: Item, dimension: int):
    '''
    Ubicar ya sea por largo o por ancho.
    dimension = 0 -> x ancho.
    dimension = 1 -> x largo.
    '''

    c = 0
    completado = False
    primer_cero = -1
    ultimo_cero = -1

    for i, k in enumerate(matrix[j]):
        if k != 0:
            primer_cero = -1
            c = 0
            continue
        if k == 0 and primer_cero == -1:
            primer_cero = (i, j)
        if k == 0:
            c += 1
        if (dimension == 0 and c == item.ancho) or (dimension == 1 and c == item.largo):
            completado = True
            ultimo_cero = (i, j)
            return completado, primer_cero, ultimo_cero

    return completado, primer_cero, ultimo_cero


def decode11(s: Solution, items: list[Item]):
    '''Función para decodificar las soluciones 1 - 1'''

    for sub_esp in s.v_sub:
        ancho: int = sub_esp.ancho
        largo: int = sub_esp.largo

        # Se aproxima al entero más cercano
        new_ancho = math.floor(ancho)
        new_largo = math.floor(largo)

        # Se crea la matriz con base en el ancho y largo definidos
        matrix = [[0 for _ in range(new_ancho)] for _ in range(new_largo)]

        sorted_items = sorted(
            items, key=lambda i: i.ancho*i.largo, reverse=True)

        for item in sorted_items:
            '''
            ¿Ancho es igual al largo?
            '''
            ancho_eq_largo = item.ancho == item.largo

            '''
            Recorrer cada item por su demanda faltante
            '''
            for i in range(s.dem_fal[item.id]):
                '''
                ¿Se debe incluir el item en el subespacio?
                '''
                incluir_item = False

                # Si ancho es igual al largo, la validación es normal y no se debe
                # validar por ambos lados.
                if ancho_eq_largo:
                    '''
                    Fase inicial.
                    Se determina primero la ubicación del ancho base del item.
                    '''
                    for j in range(len(matrix)):
                        ancho_completado, primer_cero, ultimo_cero = recorrer_ancho(
                            matrix, j, item)

                        '''
                        Si no se logró establecer el ancho, se debe continuar buscando en otras filas de la matriz
                        '''
                        if not ancho_completado:
                            continue

                        '''
                        Validación de si el item es de largo 1.
                        Si el item es de largo 1 y el ancho ya fue completado, entonces el item puede ser incluido en el subespacio.
                        '''
                        if item.largo == 1:
                            incluir_item = True
                            s.dem_com[item.id] += 1
                            sub_esp.items_capacidad[item.id] += 1
                            s.dem_fal[item.id] -= 1
                            break

                        '''
                        Fase posterior.
                        Se rellena el item. Se completa el item para verificar si es posible ubicarlo.
                        Validación inicial. len(matriz) - (j + 1) >= largo_item
                        '''
                        largo_permitido = len(matrix) - primer_cero[1]
                        '''
                        No se puede completar el item, continuar con el siguiente
                        '''
                        if largo_permitido < item.largo:
                            break

                        largo_completado, ultimo_cero = completar_x_ancho(
                            matrix, primer_cero, ultimo_cero, item.ancho, item.largo)

                        if largo_completado and ancho_completado:
                            incluir_item = True
                            s.dem_com[item.id] += 1
                            sub_esp.items_capacidad[item.id] += 1
                            s.dem_fal[item.id] -= 1
                            break

                # Si ancho es igual al largo, la validación es normal y no se debe
                # validar por ambos lados.
                else:
                    '''
                    Fase inicial.
                    Se intenta colocar por ancho el item.
                    '''
                    for j in range(len(matrix)):
                        largo_completado = False
                        ancho_completado, primer_cero, ultimo_cero = ubicar_x_dimension(
                            matrix, j, item, 0)
                        if ancho_completado:
                            '''
                            Validación de si el item es de largo 1.
                            Si el item es de largo 1 y el ancho ya fue completado, entonces el item puede ser incluido en el subespacio.
                            '''
                            if item.largo == 1:
                              incluir_item = True
                              s.dem_com[item.id] += 1
                              sub_esp.items_capacidad[item.id] += 1
                              s.dem_fal[item.id] -= 1
                              break
                        
                            '''
                            Fase posterior.
                            Se rellena el item. Se completa el item para verificar si es posible ubicarlo.
                            Validación inicial. len(matriz) - (j + 1) >= largo_item
                            '''
                            largo_permitido = len(matrix) - primer_cero[1]

                            '''
                            No se puede completar el item, intentar GIRANDOLO!
                            '''
                            if largo_permitido >= item.largo:
                              largo_completado, ultimo_cero = completar_x_ancho(
                                  matrix, primer_cero, ultimo_cero, item.ancho, item.largo)


                        if largo_completado and ancho_completado:
                            incluir_item = True
                            s.dem_com[item.id] += 1
                            sub_esp.items_capacidad[item.id] += 1
                            s.dem_fal[item.id] -= 1
                            break

                        largo_completado, primer_cero, ultimo_cero = ubicar_x_dimension(
                            matrix, j, item, 1)
                        if largo_completado:
                            '''
                            Validación de si el item es de ancho 1.
                            Si el item es de ancho 1 y el largo ya fue completado, entonces el item puede ser incluido en el subespacio.
                            '''
                            if item.ancho == 1:
                              incluir_item = True
                              s.dem_com[item.id] += 1
                              sub_esp.items_capacidad[item.id] += 1
                              s.dem_fal[item.id] -= 1
                              break

                            '''
                            Fase posterior.
                            Se rellena el item. Se completa el item para verificar si es posible ubicarlo.
                            Validación inicial. len(matriz) - (j + 1) >= largo_item
                            '''
                            largo_permitido = len(
                                matrix) - (primer_cero[1] + 1)
                            '''
                            No se puede completar el item, continuar con el siguiente
                            '''
                            if largo_permitido < item.ancho:
                                break
                            ancho_completado, ultimo_cero = completar_x_ancho(
                                matrix, primer_cero, ultimo_cero, item.largo, item.ancho)

                        if largo_completado and ancho_completado:
                            incluir_item = True
                            s.dem_com[item.id] += 1
                            sub_esp.items_capacidad[item.id] += 1
                            s.dem_fal[item.id] -= 1
                            break

                '''
                Proceso para incluir el item
                '''
                if incluir_item:
                    for j in range(primer_cero[1], ultimo_cero[1] + 1):
                        for k in range(primer_cero[0], ultimo_cero[0] + 1):
                            matrix[j][k] = item

        # Se calcula la cantidad de items que fueron satisfechos
        cantidad_items = 0
        for j in matrix:
            for k in j:
                if type(k) != int:
                    cantidad_items += 1

        # Se suman esos desperdicios de largo y ancho iniciales
        sub_esp.area_disponible -= cantidad_items
        sub_esp.matrix = matrix

    '''Se calcula el desperdicio como el área disponible de cada subespacio'''
    for sub_es in s.v_sub:
        s.desperdicio += sub_es.area_disponible

    '''Se calcula el fitness como la suma del desperdicio + una constante por la demanda faltante'''
    s.fitness = s.desperdicio + 2 * \
        sum([dem_fal for dem_fal in s.dem_fal.values()])


def print_list(the_list: list):
    '''Función para imprimir las listas'''

    for each_element in the_list:
        print(str(each_element))


def decode12(s: Solution, c, items: list[Item]):
    '''Función para decodificar las soluciones 1 - 2'''

    aux_v_sub = aux_items = 0

    '''Organizar items por area de mayor a menor'''
    items = sorted(items, key=lambda item: item.ancho *
                   item.largo, reverse=True)

    '''Organizar subespacios por area de mayor a menor'''
    s.v_sub = sorted(s.v_sub, key=lambda sub: sub.ancho *
                     sub.largo, reverse=True)

    while (True):
        if aux_v_sub == 2**c:  # Si ya pasé por todos los subespacios
            aux_v_sub = 0
            aux_items += 1

        if aux_items == len(items):  # Si ya pasé por todos los items
            break

        item = items[aux_items]
        if s.dem_fal[item.id] == 0:  # Si la demanda del item ya fue completada
            aux_items += 1
            continue

        area_disponible = s.v_sub[aux_v_sub].area_disponible
        area_item = item.ancho * item.largo
        area_entera: int = math.floor(area_disponible / area_item)

        if area_entera == 0:
            aux_v_sub += 1
            continue
        else:
            dem_item = s.dem_fal[item.id]
            # Se determina el mínimmo entre el área de parte entera y la demanda
            capacidad: int = area_entera if area_entera < dem_item else dem_item
            s.dem_com[item.id] = capacidad

            '''Se actualiza la capacidad de cada item en el subespacio'''
            s.v_sub[aux_v_sub].items_capacidad[item.id] = capacidad

            if capacidad < dem_item:
                '''Se actualiza la demanda del item'''
                s.dem_fal[item.id] -= capacidad

                '''Se actualiza el área disponible del subespacio'''
                s.v_sub[aux_v_sub].area_disponible = area_disponible - \
                    area_item*capacidad

                '''Se pasa al siguiente subespacio'''
                aux_v_sub += 1
            else:
                '''Se actualiza la demanda del item'''
                s.dem_fal[item.id] = 0

                '''Se actualiza el área disponible del subespacio'''
                s.v_sub[aux_v_sub].area_disponible = area_disponible - \
                    area_item*capacidad

                '''Se pasa al siguiente item'''
                aux_items += 1

    '''Se calcula el desperdicio como el área disponible de cada subespacio'''
    '''El desperdicio se suma solamente si el subespacio fue utilizado para satisfacer la demanda de un item'''
    for sub_es in s.v_sub:
        s.desperdicio += sub_es.area_disponible

    '''Se calcula el fitness como la suma del desperdicio + una constante por la demanda faltante'''
    s.fitness = s.desperdicio + 2 * \
        sum([dem_fal for dem_fal in s.dem_fal.values()])


def generate_h_value():
    '''
    Función para generar un valor de H.

    Se valida que H no sea 1 ni 0.
    Random reference: https://docs.python.org/3/library/random.html#random.random
    '''

    H = round(random.random(), 2)
    while H == 0.0 or H == 1.0:
        H = round(random.random(), 2)
    return H


def sol_inicial(ancho_grande, largo_grande, c, items: list[Item]):
    '''Definición de solución inicial'''

    s = Solution()
    for i in range(2**c - 1):
        s.T.append(random.randrange(0, 2))
        s.H.append(generate_h_value())

    '''Vector iniciales de demandas completadas y faltantes'''
    for item in items:
        s.dem_com[item.id] = 0  # Ej: [0, 0, 0, 0]
        s.dem_fal[item.id] = item.dem  # Ej: [12, 15, 16, 18]

    '''Se agrega el item base como un subespacio inicial'''
    sub_inicial: SubEs = SubEs(ancho_grande, largo_grande)
    sub_esp1, sub_esp2 = hacer_corte(sub_inicial, s.T[0], s.H[0])
    cortes = [{'h': sub_inicial.largo*100, 'w': sub_inicial.ancho *
               100, 'c': {'t': s.T[0], 'h': s.H[0]}}]
    cola = [sub_esp1, sub_esp2]

    '''Se generan subespacios con una copia de la solución con T y H generados'''
    s.v_sub, cortes = generacion_subespacios(
        copy.deepcopy(s), c, 1, cola, cortes)

    '''Se asignan los cortes realizados a la solución para el reporte web'''
    s.cortes = cortes

    '''Se calculan las áreas disponibles de los subespacios y
    se inicializan en 0 las capacidades de cada item en cada subespacio
    '''
    v_sub_copy = copy.deepcopy(s.v_sub)
    for i, sub_es in enumerate(v_sub_copy):
        s.v_sub[i].items_capacidad = {item.id: 0 for item in items}
        s.v_sub[i].area_disponible = sub_es.ancho * sub_es.largo

    return s


def generar_solucion_vecino(s: Solution, ancho_grande, largo_grande, c, items: list[Item]):
    '''Función para generar la solución vecino'''

    '''Vector iniciales de demandas completadas y faltantes'''
    for item in items:
        s.dem_com[item.id] = 0
        s.dem_fal[item.id] = item.dem

    '''Se agrega el item base como un subespacio inicial'''
    sub_inicial: SubEs = SubEs(ancho_grande, largo_grande)
    sub_esp1, sub_esp2 = hacer_corte(sub_inicial, s.T[0], s.H[0])
    cortes = [{'h': sub_inicial.largo*100, 'w': sub_inicial.ancho *
               100, 'c': {'t': s.T[0], 'h': s.H[0]}}]
    cola = [sub_esp1, sub_esp2]

    '''Se generan subespacios con una copia de la solución con T y H generados'''
    s.v_sub, cortes = generacion_subespacios(
        copy.deepcopy(s), c, 1, cola, cortes)

    '''Se asignan los cortes realizados a la solución para el reporte web'''
    s.cortes = cortes

    '''Se calculan las áreas disponibles de los subespacios y
    se inicializan en 0 las capacidades de cada item en cada subespacio
    '''
    v_sub_copy = copy.deepcopy(s.v_sub)
    for i, sub_es in enumerate(v_sub_copy):
        s.v_sub[i].items_capacidad = {item.id: 0 for item in items}
        s.v_sub[i].area_disponible = sub_es.ancho * sub_es.largo

    '''Se reinicia el desperdicio a 0 para el vecino'''
    s.desperdicio = 0.0
    return s


def vecindario_t(s: Solution, ancho_grande, largo_grande, c, items: list[Item]):
    '''Crear un vecino basandose en el vector T'''

    best_fitness = sys.maxsize
    s_copy = copy.deepcopy(s)
    vecinos = []
    for i in range(len(s.T)):
        vector_t = copy.deepcopy(s.T)

        '''Invertir valor de T'''
        vector_t[i] = 0 if s.T[i] == 1 else 1

        s_copy.T = vector_t
        s_vecino = generar_solucion_vecino(
            s_copy, ancho_grande, largo_grande, c, items)
        decode11(s_vecino, items)
        vecinos.append(copy.deepcopy(s_vecino))

        '''Actualizar mejor solución'''
        if s_vecino.fitness < best_fitness:
            best_fitness = s_vecino.fitness
            s_mejor = copy.deepcopy(s_vecino)

    return s_mejor, vecinos


def vecindario_h(s: Solution, ancho_grande, largo_grande, c, items: list[Item]):
    '''Crear un vecino basandose en el vector H'''

    best_fitness = sys.maxsize
    s_copy = copy.deepcopy(s)
    vecinos = []
    for i in range(len(s.H)):
        vector_h = copy.deepcopy(s.H)

        '''Hacer 5 perturbaciones'''
        for j in range(5):
            '''Probabilidad aleatoria'''
            p = np.random.rand()

            '''Distribución Normal Inversa'''
            inverse_normal = float(round(norm.ppf(p, loc=0, scale=0.3), 4))

            '''Hacer un H temporal con la perturbación'''
            temp_h = round(vector_h[i] + inverse_normal, 2)

            if temp_h >= 1.0 or temp_h <= 0.0:
                vector_h[i] = generate_h_value()
            else:
                vector_h[i] = temp_h

        s_copy.H = vector_h
        s_vecino = generar_solucion_vecino(
            s_copy, ancho_grande, largo_grande, c, items)
        decode11(s_vecino, items)
        vecinos.append(copy.deepcopy(s_vecino))

        '''Actualizar mejor solución'''
        if s_vecino.fitness < best_fitness:
            best_fitness = s_vecino.fitness
            s_mejor = copy.deepcopy(s_vecino)

    return s_mejor, vecinos
