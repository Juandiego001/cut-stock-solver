class Item:
    def __init__(self, id: int = 0, dem: int = 0, ancho: int = 0, largo: int = 0):  # Constructor
        self.id = id
        self.dem = dem
        self.ancho = ancho
        self.largo = largo

    def __str__(self):
        return f'Item #{self.id}: Ancho: {self.ancho} Largo: {self.largo} Demanda: {self.dem}'


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
        self.matrix = [] # Matriz final de ubicación de cada item

    def __str__(self):
        return f'Ancho: {self.ancho}\nLargo: {self.largo}\nÁrea disponible: {self.area_disponible}\n' +\
            'Items capacidad:\n' +\
            f'{"\n".join([f'Item #{id}: {val}' for id,
                         val in self.items_capacidad.items()])}\n'


class Solution:
    def __init__(self):  # Constructor
        self.T = []  # 0 -> Corte Horizontal, 1 -> Corte Vertial
        self.H = []  # Decimal: Porcentaje de corte
        self.v_sub: list[SubEs] = []  # Vector de subespacios
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
        temp_sub_es = [{'id': i, 'h': (sub_es.largo)*100, 'w': (sub_es.ancho)*100,
                        'r': sub_es.items_capacidad, 'matrix': [[0 if i == 0 else i.id for i in j] for j in sub_es.matrix]} for i, sub_es in enumerate(self.v_sub)]
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
