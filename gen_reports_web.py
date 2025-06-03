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
<script src="js/konva_for_sub_decode.js"></script>
<script src="js/konva_for_sub_spaces.js"></script>
<script src="js/gen_html_tags.js"></script>
<script src="js/gen_konva.js"></script>
'''

  final_part = f'''
    {script_tags}
  </body>
</html>
'''
  file.writelines(final_part)


def write_konva_for_decode(report_folder):
  '''Función para escribir una función que permita dibujar el Konva del decode'''

  konva_for_decode_file = open(f'{report_folder}/web/js/konva_for_sub_decode.js', 'w', encoding='utf-8')
  konva_for_decode_file.writelines('''
function konvaForDecode(containerCanvaId, subSpaces) {
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
  konva_for_decode_file.close()


def write_konva_for_sub(report_folder):
  '''Función para escribir una función de dibujar el Konva cada que se envíe una data y un conteinerCanvasId'''

  konva_for_sub_file = open(f'{report_folder}/web/js/konva_for_sub_spaces.js', 'w', encoding='utf-8')
  konva_for_sub_file.writelines('''
function konvaForSubSpaces(containerCanvaId, data) {
  let layer = new Konva.Layer();

  // Punto de partida desde el primer subespacio
  let centers = [[window.innerWidth / 2, 140]];

  // Calculo para los subespacios de la izquierda
  let greaterPosY = 0;
  for (let [i, subSpace] of data.entries()) {
    let width = (subSpace.w);
    let height = (subSpace.h);
    let [centerX, centerY] = centers.shift();

    let posX = centerX - (width / 2);
    let posY = centerY;
    greaterPosY = greaterPosY < posY ? posY : greaterPosY;

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

    let textInfo = `Índice: ${i}\nAlto: ${height}\nAncho: ${width}`;
    if ('c' in subSpace) {
      textInfo += `\nT: ${subSpace['c'].t}\nH: ${subSpace['c'].h}`;
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
      let childSubSpace1 = data[(i * 2) + 1];
      let childSubSpace2 = data[(i * 2) + 2];

      // Flechas
      layer.add(new Konva.Arrow({
        x: posX,
        y: posY + (height / 2),
        points: [0, 0, (childSubSpace1.w / 2) * -1, 0, (childSubSpace1.w / 2) * -1, (height / 2)],
        pointerLength: 10,
        pointerWidth: 10,
        fill: 'black',
        stroke: 'black',
        strokeWidth: 2
      }))

      layer.add(new Konva.Arrow({
        x: posX + width,
        y: posY + (height / 2),
        points: [0, 0, (childSubSpace2.w / 2), 0, (childSubSpace2.w / 2), (height / 2)],
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
        posYLine += height*subSpace['c'].h;
        points = [posXLine, posYLine, posXLine + width, posYLine];
      } else { // Corte Vertical
        posXLine += width*subSpace['c'].h;
        points = [posXLine, posYLine, posXLine, posYLine + height];
      }
      layer.add(new Konva.Line({
        points,
        stroke: 'black',
        strokeWidth: 2
      }));

      centers.push([posX - (childSubSpace1.w / 2), posY + height + 10])
      centers.push([posX + width + (childSubSpace2.w / 2), posY + height + 10])
    }
  }

  let stage = new Konva.Stage({
    container: containerCanvaId,
    width: window.innerWidth,
    height: window.innerHeight
  });

  if (greaterPosY > window.innerHeight) {
    stage.setAttrs({ height: greaterPosY + 100 });
  }

  stage.add(layer);
}
''')
  konva_for_sub_file.close()


def write_gen_konva(iterations, c, report_folder):
  '''Función para escribir función de generar el Konva de cada una de las iteraciones'''
  
  gen_konva = open(f'{report_folder}/web/js/gen_konva.js', 'w', encoding='utf-8')

  gen_konva_func = '''
  function generateKonvaStages() {
    let data_iterations = [\n'''
  for i in range(iterations):
    for j in range(2**c - 1):
      gen_konva_func += f"['iteration_{i+1}_h_{j+1}_subspaces_canvas', data_iteration_vecino_h_{i+1}_{j+1}.cortes],\n"
      gen_konva_func += f"['iteration_{i+1}_h_{j+1}_decode_canvas', data_iteration_vecino_h_{i+1}_{j+1}.subSpaces],\n"
      gen_konva_func += f"['iteration_{i+1}_t_{j+1}_subspaces_canvas', data_iteration_vecino_t_{i+1}_{j+1}.cortes],\n"
      gen_konva_func += f"['iteration_{i+1}_t_{j+1}_decode_canvas', data_iteration_vecino_t_{i+1}_{j+1}.subSpaces],\n"

  gen_konva_func += '''];
    for (let [containerCanvaId, data_iteration] of data_iterations) {
      if (containerCanvaId.includes('subspaces')) {
        konvaForSubSpaces(`${containerCanvaId}`, data_iteration);
      } else {
        konvaForDecode(`${containerCanvaId}`, data_iteration);
      }
    }
  }

  generateKonvaStages();'''

  gen_konva.writelines(gen_konva_func)
  gen_konva.close()


def write_gen_html_tags(iterations, c, report_folder):
  '''Función para escribir función de cargar la información HTML de la página'''

  gen_html_tags = open(f'{report_folder}/web/js/gen_html_tags.js', 'w', encoding='utf-8')
  gen_html_tags.writelines('''
function generateHtmlTags(iterations, c) {
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

      // Para subespacios
      let h4IterationTSubSpaces = document.createElement('h4');
      h4IterationTSubSpaces.innerHTML = `Vecino T #${i+1}-${j+1} - Generación de subespacios`;
      let divCanvasIterationTSubSpaces = document.createElement('div');
      divCanvasIterationTSubSpaces.id = `iteration_${i+1}_t_${j+1}_subspaces_canvas`;
      divCanvasIterationTSubSpaces.className = 'container_canvas';

      // Para decode
      let h4IterationTDecode = document.createElement('h4');
      h4IterationTDecode.innerHTML = `Vecino T #${i+1}-${j+1} - Satisfacción de demanda`;
      let divCanvasIterationTDecode = document.createElement('div');
      divCanvasIterationTDecode.id = `iteration_${i+1}_t_${j+1}_decode_canvas`;
      divCanvasIterationTDecode.className = 'container_canvas';

      divIterationT.appendChild(h4IterationTSubSpaces);
      divIterationT.appendChild(divCanvasIterationTSubSpaces);
      divIterationT.appendChild(h4IterationTDecode);
      divIterationT.appendChild(divCanvasIterationTDecode);

      divIterationsT.appendChild(divIterationT);
    }

    // Iteraciones para H
    for (let j = 0; j < 2**c - 1; j++) {
      let divIterationH = document.createElement('div');
      divIterationH.id = `iteration_${i+1}_h_${j+1}`;

      // Para subespacios
      let h4IterationHSubSpaces = document.createElement('h4');
      h4IterationHSubSpaces.innerHTML = `Vecino H #${i+1}-${j+1} - Generación de subespacios`;
      let divCanvasIterationHSubSpaces = document.createElement('div');
      divCanvasIterationHSubSpaces.id = `iteration_${i+1}_h_${j+1}_subspaces_canvas`;
      divCanvasIterationHSubSpaces.className = 'container_canvas';

      // Para decode
      let h4IterationHDecode = document.createElement('h4');
      h4IterationHDecode.innerHTML = `Vecino H #${i+1}-${j+1} - Satisfacción de demanda`;
      let divCanvasIterationHDecode = document.createElement('div');
      divCanvasIterationHDecode.id = `iteration_${i+1}_h_${j+1}_decode_canvas`;
      divCanvasIterationHDecode.className = 'container_canvas';

      divIterationH.appendChild(h4IterationHSubSpaces);
      divIterationH.appendChild(divCanvasIterationHSubSpaces);
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
  box-sizing: border-box;
}

body {
  width: 100%;
  height: 100dvh;  
  font-family: 'Roboto', sans-serif;
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
  background-image: url('https://www.shutterstock.com/image-vector/bullet-journal-texture-seamless-pattern-600nw-1938185254.jpg');
  max-height: 500px;
  overflow: scroll;
  margin: 40px 0;
}

.konvajs-content{
  width: 100% !important;
}
''')
  index_css_file.close()

  normalize_css_file = open(f'{base_dir}/normalize.css', 'w', encoding='utf-8')
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
