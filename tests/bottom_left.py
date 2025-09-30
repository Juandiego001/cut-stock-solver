import math
import os
from v1.classes import Item, SubEs
from datetime import datetime


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


def bottom_left(sub_esp: SubEs, items: list[Item], dem_fal: dict):
    '''Función para decodificar las soluciones 1 - 1'''

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
        for i in range(dem_fal[item.id]):
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
                        sub_esp.items_capacidad[item.id] += 1
                        dem_fal[item.id] -= 1
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
                        sub_esp.items_capacidad[item.id] += 1
                        dem_fal[item.id] -= 1
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
                            sub_esp.items_capacidad[item.id] += 1
                            dem_fal[item.id] -= 1
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
                        sub_esp.items_capacidad[item.id] += 1
                        dem_fal[item.id] -= 1
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
                            sub_esp.items_capacidad[item.id] += 1
                            dem_fal[item.id] -= 1
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
                        sub_esp.items_capacidad[item.id] += 1
                        dem_fal[item.id] -= 1
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


def write_style_file(report_folder: str):
    '''Escribir archivo index.css para index.html'''

    index_css_file = open(f'{report_folder}/web/index.css', 'w+', encoding='utf-8')
    index_css_file.writelines(
'''* {
  margin: 0;
  padding: 0;
  border: 0;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

section {
  height: 100vh;
  width: 100%;
  background-color: oklch(97% 0 0);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
}

p {
  font-weight: bold;
  font-size: 1rem;
}


#container_table {
  max-height: 600px;
  overflow-y: auto;
  padding: 10px 0;
}

#container_table table {
  border-spacing: 0;
  font-size: 1.25rem;
}

#container_table table td {
  padding: 1rem;
  border: 1px solid gray;
}

#container_konva {
  height: 100%;
  width: 100%;
  max-height: 400px;
  background-image: url('data:image/webp;base64,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');
  overflow: auto;
}''')
    index_css_file.close()


def write_index(report_folder: str, sub_esp: SubEs):
    '''Escribir archivo index.html'''
    
    file_date = report_folder.split('report_')[1]
    index_file_content =\
f'''
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Algoritmo Bottom-Left {file_date}</title>
  <link rel="stylesheet" href="./index.css" />
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
</head>

<body>
  <section>
    <p>Resultado de ejecución de Algoritmo Bottom-Left</p>

    <!-- Tabla -->
    <div id="container_table">
      <table>
'''

    for j in sub_esp.matrix:
        index_file_content += '''
        <tr>
'''
        for i in j:
          index_file_content += f'''
          <td>{i.id if type(i) != int else 0}</td>
'''
        
        index_file_content += '''
        </tr>
'''

    index_file_content +=\
'''
      </table>
    </div>

    <!-- Contenedor de Konva -->
     <div id="container_konva"></div>
  </section>

  <script src="https://unpkg.com/konva@9/konva.min.js"></script>
  <script src="./index.js"></script>
</body>
</html>
'''
    index_file = open(f'{report_folder}/web/index.html', 'w+', encoding='utf-8')
    index_file.writelines(index_file_content)
    index_file.close()


def write_js(report_folder: str, sub_esp: SubEs):
    
    index_js_file_content = f'''
let subSpaceWidth = {sub_esp.ancho*100};
let subSpaceHeight = {sub_esp.largo*100}; 
let matrix = [
'''

    for j in sub_esp.matrix:  
      index_js_file_content +=\
'''['''
      for i in j:  
        index_js_file_content += f'{str(i.id) if type(i) != int else '0'}, '

      index_js_file_content += '],'

    index_js_file_content +=\
'''
]
function drawSubspaceMatrix () {
  let colores = [
    "#FADADD",
    "#FFC0CB",
    "#F0F8FF",
    "#B0E0E6",
    "#ADD8E6",
    "#F0FFF0",
    "#98FB98",
    "#E0FFFF",
    "#B7F0E7",
    "#FFFACD",
    "#FFEFD5",
    "#FAEBD7",
    "#FFF8DC",
    "#F5F5DC",
    "#FFDAB9",
    "#FFE4C4",
    "#EE82EE",
    "#DDA0DD",
    "#E6E6FA",
    "#D8BFD8",
  ];

  const stage = new Konva.Stage({
    container: 'container_konva', // id of container <div>
    width: window.innerWidth > subSpaceWidth + 40 ? window.innerWidth : subSpaceWidth + 40,
    height: subSpaceHeight + 40,
  });

  const layer = new Konva.Layer();

  // Primero se dibuja el subespacio
  const rect1 = new Konva.Rect({
    x: 20,
    y: 20,
    width: subSpaceWidth,
    height: subSpaceHeight,
    fill: "gray",
  });

  layer.add(rect1);

  let posYInicial = 20;
  let indexColor = -1;
  let selectColor = {};
  let theColor = '';

  for (let row of matrix) {
    let posXInicial = 20;
    for (let [i, e] of row.entries()) {
      if (e !== 0) {
        if (selectColor[e]) theColor = selectColor[e];
        else {
          indexColor++;
          theColor = selectColor[e] = colores[indexColor];
        }
        const rectPos = new Konva.Rect({
           x: posXInicial,
           y: posYInicial,
           width: 100,
           height: 100,
           fill: theColor,
         });
         layer.add(rectPos);
         posXInicial += 100;
      }
    }
    posYInicial += 100;
  }

  stage.add(layer);
};

drawSubspaceMatrix();
'''

    index_js_file = open(f'{report_folder}/web/index.js', 'w+', encoding='utf-8')
    index_js_file.writelines(index_js_file_content)
    index_js_file.close()


def generate_report_web(report_folder: str, sub_esp: SubEs):
    '''Generar reporte web'''

    os.mkdir(f'{report_folder}/web')
    write_style_file(report_folder)
    write_index(report_folder, sub_esp)
    write_js(report_folder, sub_esp)


if __name__ == '__main__':

    '''
    Se establecen los items manualmente
    '''
    items = [
        Item(id=1, dem=4, ancho=1, largo=4),
        Item(id=2, dem=4, ancho=2, largo=1),
        Item(id=3, dem=2, ancho=2, largo=2),
    ]

    dem_fal = {item.id: item.dem for item in items}
    sub_esp = SubEs(ancho=6, largo=6, items_capacidad={item.id: 0 for item in items})    
    bottom_left(sub_esp=sub_esp, items=items, dem_fal=dem_fal)

    '''Creación de carpeta de reporte'''
    date_now = str(datetime.now().replace(microsecond=0)
                   ).replace(' ', '_').replace(':', '_')
    report_folder = f'./reports_bottom_left/report_{date_now}'
    os.mkdir(report_folder)

    generate_report_web(report_folder, sub_esp)
