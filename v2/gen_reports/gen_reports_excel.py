import random
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side

black_border = Border(left=Side(border_style='thin', color='FF000000'),
                      right=Side(border_style='thin', color='FF000000'),
                      top=Side(border_style='thin', color='FF000000'),
                      bottom=Side(border_style='thin', color='FF000000'))


colors = {}
saved_colors = []


def generate_random_color():

  rojo = random.randint(0, 255)
  verde = random.randint(0, 255)
  azul = random.randint(0, 255)

  the_color = f'{rojo:02x}{verde:02x}{azul:02x}'

  while(the_color in saved_colors):
    rojo = random.randint(0, 255)
    verde = random.randint(0, 255)
    azul = random.randint(0, 255)

    the_color = f'{rojo:02x}{verde:02x}{azul:02x}'
      
  return the_color


def save_solution(matrixes):
    '''
    Función para guardar solución
    '''

    wb = Workbook()
    wb.active.title = 'Caso'
    ws = wb['Caso']

    # Change column widths
    base_cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    all_cols = []
    for col1 in base_cols:
        ws.column_dimensions[col1].width = 4
        all_cols.append(col1)

    for col1 in base_cols:
        for col2 in base_cols:
            ws.column_dimensions[f'{col1}{col2}'].width = 4
            all_cols.append(f'{col1}{col2}')

    all_cols_size = len(all_cols)
    start_row_row = 2
    for i in matrixes:
        max_row = 0
        last_col_matrix = start_col_matrix = 'B'
        for matrix in i:
            start_row_matrix = start_row_row
            for k in matrix:
                cell = [start_col_matrix, start_row_matrix]

                for l in k:
                    ws[f'{cell[0]}{cell[1]}'].border = black_border

                    if l != 0:
                      if not(l in colors):
                          colors[l] = generate_random_color()
                      
                      ws[f'{cell[0]}{cell[1]}'].fill = PatternFill(fill_type='solid', fgColor=f'{colors[l]}')

                    col_pos = all_cols.index(cell[0])
                    next_col_pos = col_pos + 1 if col_pos + 1 != all_cols_size else 0
                    next_col = all_cols[next_col_pos]
                    cell = [next_col, cell[1]]
                    last_col_matrix = next_col

                start_row_matrix += 1

                max_row = start_row_matrix + 1 if start_row_matrix > max_row else max_row

            col_pos = all_cols.index(last_col_matrix)
            next_col_pos = col_pos + 1 if col_pos + 1 < all_cols_size else 0
            next_col = all_cols[next_col_pos]
            start_col_matrix = next_col

        start_row_row = max_row + 2
    
    wb.save(f'reports/testing.xlsx')
