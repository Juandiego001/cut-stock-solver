import sys
import copy
import math
import random
import numpy as np
from scipy.stats import norm


class ItemCapacidad:
    def __init__(self, id: int = 0, capacidad: int = 0, area: int = 0):  # Constructor
        self.id = id
        self.capacidad = capacidad
        self.area = area

    def __str__(self):
        return f'Item #{self.id}: Capacidad: {self.capacidad} Área: {self.area}'


class SubEs:
    def __init__(self, ancho: int = 0, largo: int = 0, items_capacidad: dict = {}):  # Constructor
        self.ancho = ancho  # Ancho del subespacio
        self.largo = largo  # Largo del subespacio
        self.area_disponible = ancho*largo
        # Capacidad de cada item dentro del subespacio
        self.items_capacidad = {}

    def __str__(self):
        return f'Ancho: {self.ancho}\nLargo: {self.largo}\nÁrea disponible: {self.area_disponible}\n' +\
            'Items capacidad:\n' +\
            f'{"\n".join([f'Item #{id}: {val}' for id,
                         val in self.items_capacidad.items()])}\n'


class Solution:
    def __init__(self):  # Constructor
        self.T = []  # 0 -> Corte Horizontal, 1 -> Corte Vertial
        self.H = []  # Decimal: Porcentaje de corte
        self.v_sub = []  # Vector de subespacios
        self.dem_com = {}  # Demanda completada
        self.dem_fal = {}  # Demanda faltante
        self.desperdicio = 0.0  # Desperdicio final
        self.fitness = 0  # Puntuación de que tan buena es la solución
        self.cortes = []  # Guardar los cortes de la solución para la representación gráfica

    def __str__(self):
        return f'''T: {self.T}
H: {self.H}
Subespacios:\n{'\n'.join([str(sub_es) for sub_es in self.v_sub])}
Demanda completada: {self.dem_com}
Demanda faltante: {self.dem_fal}
Desperdicio: {self.desperdicio}
Fitness: {self.fitness}
'''
    
    def to_dict(self):
        temp_sub_es = [{'id': i, 'h': (sub_es.largo)*100, 'w': (sub_es.ancho)*100, 'r': sub_es.items_capacidad} for i, sub_es in enumerate(self.v_sub)]
        return {
            't': self.T,
            'h': self.H,
            'subSpaces': temp_sub_es,
            'demComp': self.dem_com,
            'demFal': self.dem_fal,
            'desperdicio': self.desperdicio,
            'fitness': self.fitness,
            'cortes': self.cortes + temp_sub_es
        }


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


def generacion_subespacios(s: Solution, c: int, corte: int = 0, cola: list = [], cortes: list = []):
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
            cortes.append({'h': (sub_esp.largo)*100, 'w': (sub_esp.ancho)*100, 'c': { 't': T, 'h': H }})
            copia_cola.append(sub_esp1)
            copia_cola.append(sub_esp2)

        cola = copy.deepcopy(copia_cola)
        return generacion_subespacios(s, c, corte, cola, cortes)


def decode11(s: Solution, items):
    '''Función para decodificar las soluciones 1 - 1'''

    for sub_esp in s.v_sub:
        ancho: int = sub_esp.ancho
        largo: int = sub_esp.largo
        area_disponible: int = ancho*largo
        items_capacidad: list[ItemCapacidad] = []

        '''Se calcula la capacidad por cada item'''
        for item in items:
            area_item: int = item.ancho * item.largo  # Ai: Área del item
            area_entera: int = math.floor(area_disponible / area_item)
            demanda = s.dem_fal[item.id]
            # Se determina el mínimmo entre el área de parte entera y la demanda
            capacidad: int = area_entera if area_entera < demanda else demanda
            items_capacidad.append(ItemCapacidad(
                item.id, capacidad, area_item))

        '''Se ordena de mayor a menor capacidad'''
        items_capacidad = sorted(
            items_capacidad, key=lambda ic: ic.capacidad, reverse=True)

        '''Se recorre la lista de items ordenados por capacidad'''
        for item in items_capacidad:
            area_entera: int = math.floor(area_disponible / item.area)
            demanda = s.dem_fal[item.id]
            capacidad: int = area_entera if area_entera < demanda else demanda
            s.dem_fal[item.id] -= capacidad
            area_disponible -= item.area*capacidad
            s.dem_com[item.id] += capacidad
            sub_esp.items_capacidad[item.id] += capacidad

        sub_esp.area_disponible = area_disponible

    '''Se calcula el desperdicio como el área disponible de cada subespacio'''
    '''El desperdicio se suma solamente si el subespacio fue utilizado para satisfacer la demanda de un item'''
    for sub_es in s.v_sub:
        s.desperdicio += sub_es.area_disponible
        # if sum(sub_es.items_capacidad.values()) > 0:

    '''Se calcula el fitness como la suma del desperdicio + una constante por la demanda faltante'''
    s.fitness = s.desperdicio + 2 * \
        sum([dem_fal for dem_fal in s.dem_fal.values()])


def print_list(the_list: list):
    '''Función para imprimir las listas'''

    for each_element in the_list:
        print(str(each_element))


def decode12(s: Solution, c, items):
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
        # if sum(sub_es.items_capacidad.values()) > 0:

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


def sol_inicial(ancho_grande, largo_grande, c, items):
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
    cortes = [{'h': sub_inicial.largo*100, 'w': sub_inicial.ancho*100, 'c': {'t': s.T[0], 'h': s.H[0]}}]
    cola = [sub_esp1, sub_esp2]

    '''Se generan subespacios con una copia de la solución con T y H generados'''
    s.v_sub, cortes = generacion_subespacios(copy.deepcopy(s), c, 1, cola, cortes)

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


def generar_solucion_vecino(s: Solution, ancho_grande, largo_grande, c, items):
    '''Función para generar la solución vecino'''

    '''Vector iniciales de demandas completadas y faltantes'''
    for item in items:
        s.dem_com[item.id] = 0
        s.dem_fal[item.id] = item.dem

    '''Se agrega el item base como un subespacio inicial'''
    sub_inicial: SubEs = SubEs(ancho_grande, largo_grande)
    sub_esp1, sub_esp2 = hacer_corte(sub_inicial, s.T[0], s.H[0])
    cortes = [{'h': sub_inicial.largo*100, 'w': sub_inicial.ancho*100, 'c': {'t': s.T[0], 'h': s.H[0]}}]
    cola = [sub_esp1, sub_esp2]

    '''Se generan subespacios con una copia de la solución con T y H generados'''
    s.v_sub, cortes = generacion_subespacios(copy.deepcopy(s), c, 1, cola, cortes)

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


def vecindario_t(s: Solution, ancho_grande, largo_grande, c, items):
    '''Crear un vecino basandose en el vector T'''

    best_fitness = sys.maxsize
    s_copy = copy.deepcopy(s)
    vecinos = []
    for i in range(len(s.T)):
        vector_t = copy.deepcopy(s.T)

        '''Invertir valor de T'''
        vector_t[i] = 0 if s.T[i] == 1 else 1

        s_copy.T = vector_t
        s_vecino = generar_solucion_vecino(s_copy, ancho_grande, largo_grande, c, items)
        decode11(s_vecino, items)
        vecinos.append(copy.deepcopy(s_vecino))

        '''Actualizar mejor solución'''
        if s_vecino.fitness < best_fitness:
            best_fitness = s_vecino.fitness
            s_mejor = copy.deepcopy(s_vecino)

    return s_mejor, vecinos


def vecindario_h(s: Solution, ancho_grande, largo_grande, c, items):
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
        s_vecino = generar_solucion_vecino(s_copy, ancho_grande, largo_grande, c, items)
        decode11(s_vecino, items)
        vecinos.append(copy.deepcopy(s_vecino))

        '''Actualizar mejor solución'''
        if s_vecino.fitness < best_fitness:
            best_fitness = s_vecino.fitness
            s_mejor = copy.deepcopy(s_vecino)

    return s_mejor, vecinos
