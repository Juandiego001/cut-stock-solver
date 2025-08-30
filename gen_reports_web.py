from io import TextIOWrapper


def write_final_index(iterations, file: TextIOWrapper):
    '''Función para escribir la parte final del archivo index.html'''

    script_tags = '''
<script src="https://unpkg.com/konva@9/konva.min.js"></script>
<script src="js/data_caso_prueba.js"></script>
<script src="js/data_iterations_summary.js"></script>
<script src="js/data_sol_inicial.js"></script>
<script src="js/data_solucion.js"></script>
'''
    for i in range(iterations):
        script_tags += f'<script src="js/iterations/{i+1}_h.js"></script>\n'
        script_tags += f'<script src="js/iterations/{i+1}_t.js"></script>\n'

    script_tags += '''
<script src="js/konva_for_sub_cuts.js"></script>
<script src="js/konva_for_sub_matrix.js"></script>
<script src="js/konva_for_sub_subspaces.js"></script>
<script src="js/gen_html_tags.js"></script>
<script src="js/iterations_objects.js"></script>
<script src="js/gen_konva.js"></script>
'''

    final_part = f'''
    {script_tags}
  </body>
</html>
'''
    file.writelines(final_part)


def write_konva_for_sub_subspaces(report_folder):
    '''Función para escribir una función que permita dibujar el Konva del decode'''

    konva_for_sub_subspaces_file = open(
        f'{report_folder}/web/js/konva_for_sub_subspaces.js', 'w', encoding='utf-8')
    konva_for_sub_subspaces_file.writelines('''
function konvaForSubspaces(containerCanvaId, subSpaces) {
  let layer = new Konva.Layer();

  let maxWidth = Math.max(...subSpaces.map(e => e.w)) + 20;
  maxWidth = maxWidth < 100 ? 100 : maxWidth;

  let maxHeightRequests = Math.max(...data_caso_prueba.map(e => e.h)) + 20; // 130

  let posX = 20;
  let posY = 20;

  // Celda base para indicar indices
  layer.add(new Konva.Rect({
    x: 20,
    y: 20,
    width: maxWidth + 60,
    height: maxHeightRequests + 60,
    fill: 'white',
    stroke: 'black',
    strokeWidth: 2
  }))

  // Escribir índices de demandas y demandas
  posX += maxWidth + 60;
  for (let [i, request] of data_caso_prueba.entries()) {
    let cellWidth = (request.w + 20) < 80 ? 80 : (request.w + 20);

    // Celda base para índices
    layer.add(new Konva.Rect({
      x: posX,
      y: 20,
      width: cellWidth,
      height: 30,
      fill: 'white',
      stroke: 'black',
      strokeWidth: 2
    }))

    // Texto índices
    layer.add(new Konva.Text({
      x: posX,
      y: 20,
      width: cellWidth,
      height: 30,
      text: i + 1,
      fontSize: 18,
      fontFamily: 'Roboto',
      fill: 'black',
      align: 'center',
      verticalAlign: 'middle'
    }))

    // Celda base para demandas
    layer.add(new Konva.Rect({
      x: posX,
      y: 50,
      width: cellWidth,
      height: maxHeightRequests + 30,
      fill: 'white',
      stroke: 'black',
      strokeWidth: 2
    }))

    // Demanda real
    layer.add(new Konva.Rect({
      x: posX + (cellWidth / 2) - (request.w / 2),
      y: 50 + (maxHeightRequests / 2) - (request.h / 2),
      width: request.w,
      height: request.h,
      fill: 'white',
      stroke: 'black',
      strokeWidth: 2
    }))

    posX += cellWidth;
  }

  // Escribir índices de subespacios y subespacios
  posY += maxHeightRequests + 60;
  for (let [i, subSpace] of subSpaces.entries()) {
    let cellHeight = (subSpace.h + 20) < 80 ? 80 : (subSpace.h + 20);

    // Celda base para índices
    layer.add(new Konva.Rect({
      x: 20,
      y: posY,
      width: 60,
      height: cellHeight,
      fill: 'white',
      stroke: 'black',
      strokeWidth: 2
    }))

    // Texto índices
    layer.add(new Konva.Text({
      x: 20,
      y: posY,
      width: 60,
      height: cellHeight,
      text: i + 1,
      fontSize: 18,
      fontFamily: 'Roboto',
      fill: 'black',
      align: 'center',
      verticalAlign: 'middle'
    }))

    // Celda base para subespacios
    layer.add(new Konva.Rect({
      x: 80,
      y: posY,
      width: maxWidth,
      height: cellHeight,
      fill: 'white',
      stroke: 'black',
      strokeWidth: 2
    }))

    // Subespacio real
    layer.add(new Konva.Rect({
      x: 80 + (maxWidth / 2) - (subSpace.w / 2),
      y: posY + (cellHeight / 2) - (subSpace.h / 2),
      width: subSpace.w,
      height: subSpace.h,
      fill: 'white',
      stroke: 'black',
      strokeWidth: 2
    }))

    posY += cellHeight;
  }

  // Escribir los valores completados
  let yPosMatrix = maxHeightRequests + 80;
  for (let [i, subSpace] of subSpaces.entries()) {
    let xPosMatrix = 80 + maxWidth;
    let cellHeight = (subSpace.h + 20) < 80 ? 80 : (subSpace.h + 20);;
    for (let rKey in subSpace.r) {
      let cellWidth = (data_caso_prueba[rKey - 1].w + 20) < 80 ? 80 : (data_caso_prueba[rKey - 1].w + 20);

      layer.add(new Konva.Rect({
        x: xPosMatrix,
        y: yPosMatrix,
        width: cellWidth,
        height: cellHeight,
        fill: 'white',
        stroke: 'black',
        strokeWidth: 2
      }))

      layer.add(new Konva.Text({
        x: xPosMatrix,
        y: yPosMatrix,
        width: cellWidth,
        height: cellHeight,
        text: subSpace.r[rKey],
        fontSize: 16,
        fontFamily: 'Roboto',
        fill: 'black',
        padding: 10,
        align: 'center',
        verticalAlign: 'middle'
      }))

      xPosMatrix += cellWidth;
    }
    yPosMatrix += cellHeight;
  }

  let stage = new Konva.Stage({
    container: containerCanvaId, // id of container <div>
    width: window.innerWidth,
    height: window.innerHeight
  });

  if (posY > window.innerHeight) {
    stage.setAttrs({ height: posY + 20 });
  }

  stage.add(layer);
}''')
    konva_for_sub_subspaces_file.close()


def write_konva_for_sub_cuts(report_folder):
    '''Función para escribir una función de dibujar el Konva cada que se envíe una data y un conteinerCanvasId'''

    konva_for_sub_cuts_file = open(
        f'{report_folder}/web/js/konva_for_sub_cuts.js', 'w', encoding='utf-8')
    konva_for_sub_cuts_file.writelines('''
function drawSubSpace(i, subSpace, layer, children1, children2) {  
  let width = subSpace.w;
  let height = subSpace.h;
  let posX = subSpace.x;
  let posY = subSpace.y;

  let groupKonva = new Konva.Group({ visible: false });
  groupKonva.add(new Konva.Rect({
    x: (i % 2 == 0 ? posX + width : posX - 110),
    y: posY - 130,
    width: 120,
    height: 120,
    fill: 'white',
    stroke: 'black',
    strokeWidth: 1.5
  }))

  let textInfo = `Índice: ${i}
Alto: ${height}
Ancho: ${width}`;
  if ('c' in subSpace) {
    textInfo += `
T: ${subSpace['c'].t}
H: ${subSpace['c'].h}`;
  }

  groupKonva.add(new Konva.Text({
    x: (i % 2 == 0 ? posX + width : posX - 110),
    y: posY - 130,
    width: 120,
    height: 120,
    text: textInfo,
    fontSize: 16,
    fontFamily: 'Roboto',
    fill: 'black',
    padding: 10,
    align: 'center',
    verticalAlign: 'middle'
  }))

  let rectMainKonva = new Konva.Rect({
    id: i,
    x: posX,
    y: posY,
    width: width,
    height: height,
    fill: 'white',
    stroke: 'black',
    strokeWidth: 1.5,
  })

  rectMainKonva.on('mouseover', function (event) {
    groupKonva.setAttrs({ visible: true })
  })

  rectMainKonva.on('mouseleave', function (event) {
    groupKonva.setAttrs({ visible: false })
  })

  layer.add(groupKonva);
  layer.add(rectMainKonva);

  if ('c' in subSpace) {
    // Flechas
    layer.add(new Konva.Arrow({
      x: posX,
      y: posY + (height / 2),
      points: [0, 0, (posX - children1.x - children1.w / 2) * -1, 0, (posX - children1.x - children1.w / 2) * -1, (height / 2)],
      pointerLength: 10,
      pointerWidth: 10,
      fill: 'black',
      stroke: 'black',
      strokeWidth: 2
    }))

    layer.add(new Konva.Arrow({
      x: posX + width,
      y: posY + (height / 2),
      points: [0, 0, (children2.x + (children2.w / 2) - (posX + width)), 0, (children2.x + (children2.w / 2) - (posX + width)), (height / 2)],
      pointerLength: 10,
      pointerWidth: 10,
      fill: 'black',
      stroke: 'black',
      strokeWidth: 2
    }))

    // Lineas de corte
    let posXLine = posX;
    let posYLine = posY;
    let points = [];
    if (subSpace['c'].t === 0) { // Corte Horizontal
      posYLine += height * subSpace['c'].h;
      points = [posXLine, posYLine, posXLine + width, posYLine];
    } else { // Corte Vertical
      posXLine += width * subSpace['c'].h;
      points = [posXLine, posYLine, posXLine, posYLine + height];
    }
    layer.add(new Konva.Line({
      points,
      stroke: 'black',
      strokeWidth: 2
    }));
  }
}

function konvaForCuts(containerCanvaId, data) {
  let layer = new Konva.Layer();

  const platesByLevels = [16, 8, 4, 2, 1];
  let amountBefore = 0;
  let platesLevels = [];
  for (let [i, amount] of platesByLevels.entries()) {
    platesLevels.push(data.toReversed().slice(amountBefore, amountBefore + amount).toReversed());
    amountBefore += amount;
  }
  /*
    platesLevels = [
      [16],
      [8],
      [4],
      [2],
      [1],
    ]  
  
    platesLevel[1] -> [16:23]
    platesLevel[2] -> [24:27]
    platesLevel[3] -> [28:29]
    platesLevel[4] -> [30]
  */
  let xByLevels = [150];
  let levelsLongestHeight = [];
  for (let [i, amount] of platesByLevels.entries()) {
    const platesLevel = platesLevels[i];
    let xLevel = xByLevels[i];
    if (amount === 1) {
      levelsLongestHeight.push(platesLevel[0].h);
    } else {
      let longestHeight = 0;
      let previousLevel = platesLevels[i + 1];
      for (let j = 0; j <= amount - 2; j += 2) {
        longestHeight = longestHeight < platesLevel[j].h ? platesLevel[j].h : longestHeight;
        longestHeight = longestHeight < platesLevel[j + 1].h ? platesLevel[j + 1].h : longestHeight;
        if (i == 0) {
          let sumWidth = previousLevel[j / 2].c.t == 1 ? (platesLevel[j].w + platesLevel[j + 1].w) : platesLevel[j].w;
          let x1 = xLevel;
          let x2 = xLevel + platesLevel[j].w + sumWidth;
          xLevel += platesLevel[j].w + sumWidth + platesLevel[j + 1].w + 10;
          if (j == 0) xByLevels.push(x1 + platesLevel[j].w);
          platesLevel[j].x = x1;
          platesLevel[j + 1].x = x2;
          previousLevel[j / 2].x = x1 + platesLevel[j].w;
        } else {
          previousLevel[j / 2].x = platesLevel[j].x + platesLevel[j].w;
        }
      }
      levelsLongestHeight.push(longestHeight);
    }
  }

  let x = 0;
  while (x != 4) {
    let ingreso = false;
    let previousLevel = platesLevels[x + 1];
    let platesLevelsLength = platesLevels[x].length;
    for (let i = 0; i < platesLevelsLength; i += 2) {
      let plate1 = platesLevels[x][i];
      let plate2 = platesLevels[x][i + 1];
      let parentPlate = previousLevel[i / 2];
      let difference = (plate1.x + plate1.w) - parentPlate.x;

      if (difference > 0) {
        for (let j = i / 2; j < platesLevels[x + 1].length; j++) {
          platesLevels[x + 1][j].x += difference;
        }
        ingreso = true;
      }

      let difference2 = (parentPlate.x + parentPlate.w) - plate2.x;
      if (difference2 > 0) {
        for (let j = i + 1; j < platesLevels[x].length; j++) {
          platesLevels[x][j].x += difference2;
        }
        ingreso = true;
      }
    }

    if (ingreso) { x = 0; } else x += 1;
  }

  /*
    levelsLongestHeight = [120, 120, 110, 100, 100]
    const maxHeight = levelsLongestHeight.reduce((a, e) => a + e.h + 10, 140);
    index -> total subespaces.
    index = platesByLevels.reduce((a, e) => a + e, 0);
  */
  const maxHeightKonva = levelsLongestHeight.reduce((a, e) => a + e + 10, 140);
  let yLevel = maxHeightKonva;
  let index = platesByLevels.reduce((a, e) => a + e, 0);
  for (let i = 0; i < platesByLevels.length; i++) {
    yLevel = yLevel - 10 - levelsLongestHeight[i];
    let levelBefore = platesLevels[i - 1];
    for (let [j, subSpace] of platesLevels[i].entries()) {
      subSpace.y = yLevel;
      drawSubSpace(index, subSpace, layer, levelBefore ? levelBefore[j*2] : null, levelBefore ? levelBefore[j*2 + 1] : null);
      index -= 1;
    }
  }

  let maxX = 0;
  for (let i = 0; i < platesLevels.length; i++) {
    let tempMaxX = platesLevels[i].reduce((max, current) => {
      return current.x > max.x ? current : max;
    });
    maxX = maxX < tempMaxX.x ? tempMaxX.x : maxX;
  }

  let stage = new Konva.Stage({
    container: containerCanvaId,
    width: window.innerWidth < maxX ? maxX + 150 : window.innerWidth,
    height: window.innerHeight < maxHeightKonva ? maxHeightKonva : window.innerHeight
  });

  stage.add(layer);
}
''')
    konva_for_sub_cuts_file.close()


def write_konva_for_sub_matrix(report_folder):
    '''Función para escribir función de generar el Konva de la matriz de cada subespacio'''
    
    konva_for_sub_matrix_file = open(f'{report_folder}/web/js/konva_for_sub_matrix.js',
                     'w', encoding='utf-8')
    
    konva_for_sub_matrix = '''function drawSubspaceMatrix (containerId, subSpaceWidth, subSpaceHeight, matrix) {
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
    container: containerId, // id of container <div>
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

function drawSubspaceTableMatrix(containerTable, matrix) {
  const tableElement = document.createElement('table');

  for (let j of matrix) {
    const trElement = document.createElement('tr');
    for (let i of j) {
      const tdElement = document.createElement('td');
      tdElement.innerHTML = i;
      trElement.appendChild(tdElement);
    }
    tableElement.appendChild(trElement);
  }

  document.getElementById(containerTable).innerHTML = '';
  document.getElementById(containerTable).appendChild(tableElement);
}

function konvaForMatrix(iterationId) {
  let containerCanvas = `${iterationId}_matrix_canvas`;
  let containerTable = `${iterationId}_container_table`;
  let subSpaceNeeded = document.getElementById(`${iterationId}_select`).value;
  const subSpace = dataIterationsSubspaces[
    `${iterationId}_subspaces_canvas`
  ].find((e) => e.id === parseInt(subSpaceNeeded));
  console.log({ subSpace });
  drawSubspaceTableMatrix(containerTable, subSpace.matrix);
  drawSubspaceMatrix(containerCanvas, subSpace.w, subSpace.h, subSpace.matrix);
}
    '''

    konva_for_sub_matrix_file.writelines(konva_for_sub_matrix)
    konva_for_sub_matrix_file.close()


def write_gen_konva(report_folder):
    '''Función para escribir función de generar el Konva de cada una de las iteraciones'''

    gen_konva = open(f'{report_folder}/web/js/gen_konva.js',
                     'w', encoding='utf-8')

    gen_konva_func = '''function generateKonvaStages(containerCanvaId) {
    if (containerCanvaId.includes('cuts')) {
      konvaForCuts(`${containerCanvaId}`, dataIterationsCuts[containerCanvaId]);
    } else {
      konvaForSubspaces(`${containerCanvaId}`, dataIterationsSubspaces[containerCanvaId]);
    }
  }
  '''

    gen_konva.writelines(gen_konva_func)
    gen_konva.close()


def write_gen_html_tags(iterations, c, report_folder):
    '''Función para escribir función de cargar la información HTML de la página'''

    gen_html_tags = open(
        f'{report_folder}/web/js/gen_html_tags.js', 'w', encoding='utf-8')
    gen_html_tags.writelines('''function generateHtmlTags(iterations, c) {
  let sectionParent = document.getElementById('iterations');
  for (let i = 0; i < iterations; i++) {
    let divParent = document.createElement('div');
    divParent.id = `iteration_${i+1}`;
    let h2Parent = document.createElement('h2');
    h2Parent.innerHTML = `Itearción # ${i+1}`

    // Iteraciones para T
    let divIterationsT = document.createElement('div');
    divIterationsT.id = `iteration_${i+1}_t`;
    let h3IterationsT = document.createElement('h3');
    h3IterationsT.innerHTML = `Vecinos T ${i+1}`;
    divIterationsT.appendChild(h3IterationsT);

    // Iteraciones para H
    let divIterationsH = document.createElement('div');
    divIterationsH.id = `iteration_${i+1}_h`;
    let h3IterationsH = document.createElement('h3');
    h3IterationsH.innerHTML = `Vecinos H ${i+1}`;
    divIterationsH.appendChild(h3IterationsH);

    // Iteraciones para T
    for (let j = 0; j < 2**c - 1; j++) {
      let divIterationT = document.createElement('div');
      divIterationT.id = `iteration_${i+1}_t_${j+1}`;

      // Para cortes
      let h4IterationTSubSpaces = document.createElement('h4');
      h4IterationTSubSpaces.innerHTML = `Vecino T #${i+1}-${j+1} - Generación de subespacios`;
      let divCanvasIterationTSubSpaces = document.createElement('div');
      divCanvasIterationTSubSpaces.id = `iteration_${i+1}_t_${j+1}_cuts_canvas`;
      divCanvasIterationTSubSpaces.className = 'container_canvas';
                             
      let btnIterationSubspaceT = document.createElement('button');
      btnIterationSubspaceT.className = 'iteration_subspace_button';
      btnIterationSubspaceT.innerHTML = 'Ver representación gráfica';
      btnIterationSubspaceT.addEventListener('click', function () {
        console.log(`iteration_${i+1}_t_${j+1}_cuts_canvas`);
        generateKonvaStages(`iteration_${i+1}_t_${j+1}_cuts_canvas`);
      });
                             
      // Para matriz de subespacios
      let h4IterationTMatrix = document.createElement('h4');
      h4IterationTMatrix.innerHTML = `Vecino T #${i+1}-${j+1} - Matriz de subespacios`;
      let divTableIterationTMatrix = document.createElement('div');
      divTableIterationTMatrix.id = `iteration_${i+1}_t_${j+1}_container_table`;
      divTableIterationTMatrix.className = 'container_table';
      let divCanvasIterationTMatrix = document.createElement('div');
      divCanvasIterationTMatrix.id = `iteration_${i+1}_t_${j+1}_matrix_canvas`;
      divCanvasIterationTMatrix.className = 'container_canvas';

      // Select div + select element
      let divSelectSubspaceTMatrix = document.createElement('div');
      divSelectSubspaceTMatrix.className = 'select_container';
      let selectSubspaceTMatrix = document.createElement('select');
      selectSubspaceTMatrix.id = `iteration_${i+1}_t_${j+1}_select`;

      // Select options
      for (let j = 0; j < 2**c; j++) {
        let selectOptionSubspaceTMatrix = document.createElement('option');
        selectOptionSubspaceTMatrix.value = j;
        selectOptionSubspaceTMatrix.innerHTML = `Subespacio #${j+1}`;
        selectSubspaceTMatrix.appendChild(selectOptionSubspaceTMatrix);
      }

      let btnSelecSubspaceTMatrix = document.createElement('button');
      btnSelecSubspaceTMatrix.innerHTML = 'Ver Matriz';
      btnSelecSubspaceTMatrix.className = 'iteration_subspace_button';
      btnSelecSubspaceTMatrix.addEventListener('click', function () {
        konvaForMatrix(`iteration_${i+1}_t_${j+1}`);
      });

      divSelectSubspaceTMatrix.appendChild(selectSubspaceTMatrix);
      divSelectSubspaceTMatrix.appendChild(btnSelecSubspaceTMatrix);

      // Para decode
      let h4IterationTDecode = document.createElement('h4');
      h4IterationTDecode.innerHTML = `Vecino T #${i+1}-${j+1} - Satisfacción de demanda`;
      let divCanvasIterationTDecode = document.createElement('div');
      divCanvasIterationTDecode.id = `iteration_${i+1}_t_${j+1}_subspaces_canvas`;
      divCanvasIterationTDecode.className = 'container_canvas';

      let btnIterationDecodeT = document.createElement('button');
      btnIterationDecodeT.className = 'iteration_button';
      btnIterationDecodeT.innerHTML = 'Ver representación gráfica';
      btnIterationDecodeT.addEventListener('click', function () {
        console.log(`iteration_${i+1}_t_${j+1}_subspaces_canvas`);
        generateKonvaStages(`iteration_${i+1}_t_${j+1}_subspaces_canvas`);
      });

      // Final append subspaces
      divIterationT.appendChild(h4IterationTSubSpaces);
      divIterationT.appendChild(btnIterationSubspaceT);
      divIterationT.appendChild(divCanvasIterationTSubSpaces);
      
      // Final append matrix
      divIterationT.appendChild(h4IterationTMatrix);
      divIterationT.appendChild(divSelectSubspaceTMatrix);
      divIterationT.appendChild(divTableIterationTMatrix);
      divIterationT.appendChild(divCanvasIterationTMatrix);

      // Final append decode
      divIterationT.appendChild(h4IterationTDecode);
      divIterationT.appendChild(divCanvasIterationTDecode);

      divIterationsT.appendChild(divIterationT);
    }

    // Iteraciones para H
    for (let j = 0; j < 2**c - 1; j++) {
      let divIterationH = document.createElement('div');
      divIterationH.id = `iteration_${i+1}_h_${j+1}`;

      // Para cortes
      let h4IterationHSubSpaces = document.createElement('h4');
      h4IterationHSubSpaces.innerHTML = `Vecino H #${i+1}-${j+1} - Generación de subespacios`;
      let divCanvasIterationHSubSpaces = document.createElement('div');
      divCanvasIterationHSubSpaces.id = `iteration_${i+1}_h_${j+1}_cuts_canvas`;
      divCanvasIterationHSubSpaces.className = 'container_canvas';

      let btnIterationSubspaceH = document.createElement('button');
      btnIterationSubspaceH.className = 'iteration_subspace_button';
      btnIterationSubspaceH.innerHTML = 'Ver representación gráfica';
      btnIterationSubspaceH.addEventListener('click', function () {
        console.log(`iteration_${i+1}_h_${j+1}_cuts_canvas`);
        generateKonvaStages(`iteration_${i+1}_h_${j+1}_cuts_canvas`);
      });
                             
      // Para matriz de subespacios
      let h4IterationHMatrix = document.createElement('h4');
      h4IterationHMatrix.innerHTML = `Vecino H #${i+1}-${j+1} - Matriz de subespacios`;
      let divTableIterationHMatrix = document.createElement('div');
      divTableIterationHMatrix.id = `iteration_${i+1}_h_${j+1}_container_table`;
      divTableIterationHMatrix.className = 'container_table';
      let divCanvasIterationHMatrix = document.createElement('div');
      divCanvasIterationHMatrix.id = `iteration_${i+1}_h_${j+1}_matrix_canvas`;
      divCanvasIterationHMatrix.className = 'container_canvas';

      // Select div + select element
      let divSelectSubspaceHMatrix = document.createElement('div');
      divSelectSubspaceHMatrix.className = 'select_container';
      let selectSubspaceHMatrix = document.createElement('select');
      selectSubspaceHMatrix.id = `iteration_${i+1}_h_${j+1}_select`;

      // Select options
      for (let j = 0; j < 2**c; j++) {
        let selectOptionSubspaceHMatrix = document.createElement('option');
        selectOptionSubspaceHMatrix.value = j;
        selectOptionSubspaceHMatrix.innerHTML = `Subespacio #${j+1}`;
        selectSubspaceHMatrix.appendChild(selectOptionSubspaceHMatrix);
      }

      let btnSelecSubspaceHMatrix = document.createElement('button');
      btnSelecSubspaceHMatrix.innerHTML = 'Ver Matriz';
      btnSelecSubspaceHMatrix.className = 'iteration_subspace_button';
      btnSelecSubspaceHMatrix.addEventListener('click', function () {
        konvaForMatrix(`iteration_${i+1}_h_${j+1}`);
      });

      divSelectSubspaceHMatrix.appendChild(selectSubspaceHMatrix);
      divSelectSubspaceHMatrix.appendChild(btnSelecSubspaceHMatrix);

      // Para decode
      let h4IterationHDecode = document.createElement('h4');
      h4IterationHDecode.innerHTML = `Vecino H #${i+1}-${j+1} - Satisfacción de demanda`;
      let divCanvasIterationHDecode = document.createElement('div');
      divCanvasIterationHDecode.id = `iteration_${i+1}_h_${j+1}_subspaces_canvas`;
      divCanvasIterationHDecode.className = 'container_canvas';
                             
      let btnIterationDecodeH = document.createElement('button');
      btnIterationDecodeH.className = 'iteration_button';
      btnIterationDecodeH.innerHTML = 'Ver representación gráfica';
      btnIterationDecodeH.addEventListener('click', function () {
        console.log(`iteration_${i+1}_h_${j+1}_subspaces_canvas`);
        generateKonvaStages(`iteration_${i+1}_h_${j+1}_subspaces_canvas`);
      });

      // Final append subspaces
      divIterationH.appendChild(h4IterationHSubSpaces);
      divIterationH.appendChild(btnIterationSubspaceH);
      divIterationH.appendChild(divCanvasIterationHSubSpaces);

      // Final append matrix
      divIterationH.appendChild(h4IterationHMatrix);
      divIterationH.appendChild(divSelectSubspaceHMatrix);
      divIterationH.appendChild(divTableIterationHMatrix);
      divIterationH.appendChild(divCanvasIterationHMatrix);

      // Final append decode
      divIterationH.appendChild(h4IterationHDecode);
      divIterationH.appendChild(divCanvasIterationHDecode);
      
      divIterationsH.appendChild(divIterationH);
    }

    divParent.appendChild(divIterationsT);
    divParent.appendChild(divIterationsH);
    sectionParent.appendChild(divParent);
  }
}
''')
    gen_html_tags.writelines(f'generateHtmlTags({iterations}, {c});')
    gen_html_tags.close()


def write_iterations_objects(iterations, c, report_folder):
    '''Función para escribir objetos de cada una de las iteraciones por los tres tipos de representaciones: cortes/cuts, subespacios/matrix y demanda/decode'''
    
    iterations_objects_file = open(f'{report_folder}/web/js/iterations_objects.js',
                     'w', encoding='utf-8')

    iterations_objects = '''let dataIterationsCuts = {\n'''

    for i in range(iterations):
        for j in range(2**c - 1):
            iterations_objects += f"\t'iteration_{i+1}_h_{j+1}_cuts_canvas': data_iteration_vecino_h_{i+1}_{j+1}.cortes,\n"
            iterations_objects += f"\t'iteration_{i+1}_t_{j+1}_cuts_canvas': data_iteration_vecino_t_{i+1}_{j+1}.cortes,\n"

    iterations_objects += '''};
    
    let dataIterationsSubspaces = {\n'''

    for i in range(iterations):
        for j in range(2**c - 1):
                iterations_objects += f"\t'iteration_{i+1}_h_{j+1}_subspaces_canvas': data_iteration_vecino_h_{i+1}_{j+1}.subSpaces,\n"
                iterations_objects += f"\t'iteration_{i+1}_t_{j+1}_subspaces_canvas': data_iteration_vecino_t_{i+1}_{j+1}.subSpaces,\n"

    iterations_objects += '''};'''

    iterations_objects_file.writelines(iterations_objects)
    iterations_objects_file.close()


def write_base_index(file: TextIOWrapper):
    '''Escribe el archivo index.html base'''

    file.writelines('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Resumen Reporte 2025-05-23_19_37_23</title>
  <link rel="stylesheet" href="./styles/normalize.css">
  <link rel="stylesheet" href="./styles/index.css">
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Menú Lateral -->
  <nav>
    <div class="nav_button_container">
      <p>Tabla de contenido</p>
      <button onclick="">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>menu</title><path d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" /></svg>
      </button>
    </div>

    <div class="nav_content">
      <!-- Resumen inicial -->
      <div class="nav_content__item">
        <div class="nav_content__item__item">
          <span>Resumen</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>chevron-down</title><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" /></svg>
        </div>
        <div class="nav_content__item__subnav">
          <div>Caso</div>
          <div>Solución Inicial</div>
          <div>Iteraciones</div>
          <div>Solución</div>
        </div>
      </div>

      <!-- Iteraciones -->
      <div class="nav_content__item">
        <div class="nav_content__item__item">
          <span>Iteraciones</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>chevron-down</title><path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" /></svg>
        </div>
        <div class="nav_content__item__subnav">
          <div class="nav_content__item__subnav__item">
          </div>
      </div>
    </div>
  </nav>
                  
  <article>
    <section>
      <h1>Resumen</h1>
    </section>

    <section id="iterations">
      <h1>Iteraciones</h1>
            
    </section>
  </article>
''')


def write_base_styles_files(base_dir):
    '''Función para escribir los archivos de CSS'''

    index_css_file = open(f'{base_dir}/index.css', 'w', encoding='utf-8')
    index_css_file.writelines('''
* {
  margin: 0;
  border: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Roboto', sans-serif;
}

body {
  width: 100%;
  height: 100dvh;  
  display: flex;
  flex-direction: row;
  overflow: hidden;
}

nav {
  position: sticky;
  max-width: 250px;
  width: 25%;
  height: 100%;
  background-color: white;
  box-shadow: 5px 0px 5px 0px rgba(0,0,0,0.2);
  -webkit-box-shadow: 5px 0px 5px 0px rgba(0,0,0,0.2);
  -moz-box-shadow: 5px 0px 5px 0px rgba(0,0,0,0.2);
  overflow-y: scroll;
}

button {
  border: 0;
  outline: 0;
  background: none;
}

/* Start Nav Button Container */
.nav_button_container {
  margin-top: 10px;
  width: 100%;
  display: flex;
  align-items: center;
  flex-direction: row;
}

.nav_button_container p {
  padding-left: 15px;
  text-align: left;
  flex-grow: 1;
}

.nav_button_container button {
  flex-grow: 1;
  cursor: pointer;
}

.nav_button_container button:hover {
  cursor: pointer;
}

.nav_button_container button svg {
  width: 25px;
}

/* Start Nav Content */
.nav_content {
  display: flex;
  flex-direction: column;
}

.nav_content__item {
  width: 100%;
}

.nav_content__item__item {
  display: flex;
  align-items: center;
  padding: 5px 0 5px 15px;
  flex-direction: row;
}

.nav_content__item__item svg {
  width: 25px;
}

.nav_content__item__subnav {
 padding-left: 20px;
}

.nav_content__item__subnav > div {
  padding: 5px 0;
}

.nav_content__item__subnav__item__subnav {
  padding: 5px 0 5px 10px;
}

.nav_content__item__subnav__item__subnav > div{
  padding: 5px 0;
}

/* Start Article */
article {
  overflow-y: scroll;
  width: 100%;
  padding-left: 20px;
}

.container_canvas {
  background-image: url('data:image/webp;base64,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');
  max-height: 500px;
  overflow: auto;
  margin: 40px 0;
}

.konvajs-content{
  width: 100% !important;
}
                              
/* Iterations Elements */
h3 {
  margin-bottom: 0.75rem;
}

h4 {
  margin-bottom: 0.5rem;
}

.iteration_subspace_button {
  padding: 0.5rem;
  background: gray;
  color: white;
  font-size: 12px;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  line-height: 100%;
}
                              
.select_container {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  align-items: center;
  padding: 1rem 0;
}

.select_container select {
  border: 1px solid lightgray;
  outline: 0;
  padding: 0.5rem;
}

.container_table {
  max-height: 600px;
  overflow-y: auto;
  padding: 10px 0;
}

.container_table table {
  border-spacing: 0;
  font-size: 1.25rem;
}

.container_table table td {
  padding: 1rem;
  border: 1px solid gray;
}
''')
    index_css_file.close()

    normalize_css_file = open(
        f'{base_dir}/normalize.css', 'w', encoding='utf-8')
    normalize_css_file.writelines('''
/*! normalize.css v8.0.1 | MIT License | github.com/necolas/normalize.css */

/* Document
   ========================================================================== */

/**
 * 1. Correct the line height in all browsers.
 * 2. Prevent adjustments of font size after orientation changes in iOS.
 */

html {
  line-height: 1.15; /* 1 */
  -webkit-text-size-adjust: 100%; /* 2 */
}

/* Sections
   ========================================================================== */

/**
 * Remove the margin in all browsers.
 */

body {
  margin: 0;
}

/**
 * Render the `main` element consistently in IE.
 */

main {
  display: block;
}

/**
 * Correct the font size and margin on `h1` elements within `section` and
 * `article` contexts in Chrome, Firefox, and Safari.
 */

h1 {
  font-size: 2em;
  margin: 0.67em 0;
}

/* Grouping content
   ========================================================================== */

/**
 * 1. Add the correct box sizing in Firefox.
 * 2. Show the overflow in Edge and IE.
 */

hr {
  box-sizing: content-box; /* 1 */
  height: 0; /* 1 */
  overflow: visible; /* 2 */
}

/**
 * 1. Correct the inheritance and scaling of font size in all browsers.
 * 2. Correct the odd `em` font sizing in all browsers.
 */

pre {
  font-family: monospace, monospace; /* 1 */
  font-size: 1em; /* 2 */
}

/* Text-level semantics
   ========================================================================== */

/**
 * Remove the gray background on active links in IE 10.
 */

a {
  background-color: transparent;
}

/**
 * 1. Remove the bottom border in Chrome 57-
 * 2. Add the correct text decoration in Chrome, Edge, IE, Opera, and Safari.
 */

abbr[title] {
  border-bottom: none; /* 1 */
  text-decoration: underline; /* 2 */
  text-decoration: underline dotted; /* 2 */
}

/**
 * Add the correct font weight in Chrome, Edge, and Safari.
 */

b,
strong {
  font-weight: bolder;
}

/**
 * 1. Correct the inheritance and scaling of font size in all browsers.
 * 2. Correct the odd `em` font sizing in all browsers.
 */

code,
kbd,
samp {
  font-family: monospace, monospace; /* 1 */
  font-size: 1em; /* 2 */
}

/**
 * Add the correct font size in all browsers.
 */

small {
  font-size: 80%;
}

/**
 * Prevent `sub` and `sup` elements from affecting the line height in
 * all browsers.
 */

sub,
sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline;
}

sub {
  bottom: -0.25em;
}

sup {
  top: -0.5em;
}

/* Embedded content
   ========================================================================== */

/**
 * Remove the border on images inside links in IE 10.
 */

img {
  border-style: none;
}

/* Forms
   ========================================================================== */

/**
 * 1. Change the font styles in all browsers.
 * 2. Remove the margin in Firefox and Safari.
 */

button,
input,
optgroup,
select,
textarea {
  font-family: inherit; /* 1 */
  font-size: 100%; /* 1 */
  line-height: 1.15; /* 1 */
  margin: 0; /* 2 */
}

/**
 * Show the overflow in IE.
 * 1. Show the overflow in Edge.
 */

button,
input { /* 1 */
  overflow: visible;
}

/**
 * Remove the inheritance of text transform in Edge, Firefox, and IE.
 * 1. Remove the inheritance of text transform in Firefox.
 */

button,
select { /* 1 */
  text-transform: none;
}

/**
 * Correct the inability to style clickable types in iOS and Safari.
 */

button,
[type="button"],
[type="reset"],
[type="submit"] {
  -webkit-appearance: button;
}

/**
 * Remove the inner border and padding in Firefox.
 */

button::-moz-focus-inner,
[type="button"]::-moz-focus-inner,
[type="reset"]::-moz-focus-inner,
[type="submit"]::-moz-focus-inner {
  border-style: none;
  padding: 0;
}

/**
 * Restore the focus styles unset by the previous rule.
 */

button:-moz-focusring,
[type="button"]:-moz-focusring,
[type="reset"]:-moz-focusring,
[type="submit"]:-moz-focusring {
  outline: 1px dotted ButtonText;
}

/**
 * Correct the padding in Firefox.
 */

fieldset {
  padding: 0.35em 0.75em 0.625em;
}

/**
 * 1. Correct the text wrapping in Edge and IE.
 * 2. Correct the color inheritance from `fieldset` elements in IE.
 * 3. Remove the padding so developers are not caught out when they zero out
 *    `fieldset` elements in all browsers.
 */

legend {
  box-sizing: border-box; /* 1 */
  color: inherit; /* 2 */
  display: table; /* 1 */
  max-width: 100%; /* 1 */
  padding: 0; /* 3 */
  white-space: normal; /* 1 */
}

/**
 * Add the correct vertical alignment in Chrome, Firefox, and Opera.
 */

progress {
  vertical-align: baseline;
}

/**
 * Remove the default vertical scrollbar in IE 10+.
 */

textarea {
  overflow: auto;
}

/**
 * 1. Add the correct box sizing in IE 10.
 * 2. Remove the padding in IE 10.
 */

[type="checkbox"],
[type="radio"] {
  box-sizing: border-box; /* 1 */
  padding: 0; /* 2 */
}

/**
 * Correct the cursor style of increment and decrement buttons in Chrome.
 */

[type="number"]::-webkit-inner-spin-button,
[type="number"]::-webkit-outer-spin-button {
  height: auto;
}

/**
 * 1. Correct the odd appearance in Chrome and Safari.
 * 2. Correct the outline style in Safari.
 */

[type="search"] {
  -webkit-appearance: textfield; /* 1 */
  outline-offset: -2px; /* 2 */
}

/**
 * Remove the inner padding in Chrome and Safari on macOS.
 */

[type="search"]::-webkit-search-decoration {
  -webkit-appearance: none;
}

/**
 * 1. Correct the inability to style clickable types in iOS and Safari.
 * 2. Change font properties to `inherit` in Safari.
 */

::-webkit-file-upload-button {
  -webkit-appearance: button; /* 1 */
  font: inherit; /* 2 */
}

/* Interactive
   ========================================================================== */

/*
 * Add the correct display in Edge, IE 10+, and Firefox.
 */

details {
  display: block;
}

/*
 * Add the correct display in all browsers.
 */

summary {
  display: list-item;
}

/* Misc
   ========================================================================== */

/**
 * Add the correct display in IE 10+.
 */

template {
  display: none;
}

/**
 * Add the correct display in IE 10.
 */

[hidden] {
  display: none;
}
''')
    normalize_css_file.close()
