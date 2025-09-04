import copy
import math
from classes import Item

def make_cut(id_item: int, ancho_item: int, largo_item: int, index_selected_matrix: int, ultimo_cero: tuple[int, int], available_matrixes: list[list], added_items: list, all_matrixes: list[list]):
    '''
    ultima_pos (2, 2) -> x: 2 y: 2
    '''

    matrix = available_matrixes[index_selected_matrix]

    item_matrix = [[id_item for i in range(
        ancho_item)] for j in range(largo_item)]

    new_subspace_h = len(matrix) - (ultimo_cero[1] + 1)
    new_subspace_w = len(matrix[0]) - (ultimo_cero[0] + 1)

    '''
    El item ha completado todo el subespacio
    '''
    if new_subspace_h == 0 and new_subspace_w == 0:
        all_matrixes.append(added_items + copy.deepcopy(available_matrixes))
        added_items.append(item_matrix)
        del available_matrixes[index_selected_matrix]
        return

    '''
    El item ha completado toda la altura del subespacio
    '''
    if new_subspace_h == 0:
        new_matrix_1 = [[0 for i in range(new_subspace_w)]
                        for j in range(largo_item)]
        all_matrixes.append(added_items + copy.deepcopy(available_matrixes))
        added_items.append(item_matrix)
        available_matrixes.append(new_matrix_1)
        del available_matrixes[index_selected_matrix]
        return

    '''
    El item ha completado toda el ancho del subespacio
    '''
    if new_subspace_w == 0:
        new_matrix_1 = [[0 for i in range(ancho_item)]
                        for j in range(largo_item)]
        all_matrixes.append(added_items + copy.deepcopy(available_matrixes))
        added_items.append(item_matrix)
        available_matrixes.append(new_matrix_1)
        del available_matrixes[index_selected_matrix]
        return

    new_matrix_1 = [[0 for i in range(len(matrix[0]))]
                    for j in range(new_subspace_h)]
    new_matrix_2 = [[0 for i in range(new_subspace_w)]
                    for j in range(largo_item)]

    all_matrixes.append(added_items + copy.deepcopy(available_matrixes))

    available_matrixes.append(new_matrix_1)
    available_matrixes.append(new_matrix_2)

    del available_matrixes[index_selected_matrix]

    added_items.append(item_matrix)


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


def sol_inicial(ancho_grande, largo_grande, items: list[Item]):

  # Se crea la matriz con base en el ancho y largo definidos
  init_matrix = [[0 for _ in range(ancho_grande)] for _ in range(largo_grande)]

  all_matrixes = []
  added_items = []
  available_matrixes = [init_matrix]

  for item in items:
    '''
    ¿Ancho es igual al largo?
    '''
    ancho_eq_largo = item.ancho == item.largo

    '''
    ¿Se debe incluir el item en el subespacio?
    '''
    incluir_item = False

    index_selected_matrix = -1
    primer_cero = -1
    ultimo_cero = -1

    ancho_item = item.ancho
    largo_item = item.largo
    for i in range(len(available_matrixes)):

      matrix = available_matrixes[i]
      index_selected_matrix = i

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
                    ancho_item = item.largo
                    largo_item = item.ancho
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
                  ancho_item = item.largo
                  largo_item = item.ancho
                  break
      
      if incluir_item:
          break

    if incluir_item:
        matrix = available_matrixes[index_selected_matrix]
        for j in range(primer_cero[1], ultimo_cero[1] + 1):
            for k in range(primer_cero[0], ultimo_cero[0] + 1):
              matrix[j][k] = item.id
        available_matrixes[index_selected_matrix] = matrix

        make_cut(item.id, ancho_item, largo_item, index_selected_matrix, ultimo_cero, available_matrixes, added_items, all_matrixes)

  return all_matrixes