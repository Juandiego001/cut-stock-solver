from .sort import sort
from .add import add
from .remove import remove
from .move import move
from .list_groups import list_groups
from .validate import validate
from config import instruction_text_manage_groups, validate_instruction, instruction_text_manage_groups_sort, possible_groups, get_group_name, instruction_text_manage_groups_add, instruction_text_manage_groups_remove, instruction_text_manage_groups_move_from, instruction_text_manage_groups_move_to, instruction_text_manage_groups_list, instruction_text_manage_groups_validate


def instruction_1():
    '''Listar casos de un grupo'''

    group = input(instruction_text_manage_groups_list)
    validate_instruction(len(possible_groups), group)
    group_name = get_group_name(int(group))
    list_groups(f'{group_name}.txt')


def instruction_2():
    '''Ingresar casos en un grupo'''

    group = input(instruction_text_manage_groups_add)
    validate_instruction(len(possible_groups), group)
    group_name = get_group_name(int(group))
    add(group_name)


def instruction_3():
    '''Organizar casos en un grupo'''

    group = input(instruction_text_manage_groups_sort)
    validate_instruction(len(possible_groups), group)
    group_name = get_group_name(int(group))
    sort(f'{group_name}.txt')


def instruction_4():
    '''Mover casos de un grupo a otro'''

    group_from = input(instruction_text_manage_groups_move_from)
    validate_instruction(len(possible_groups), group_from)
    group_from_name = get_group_name(int(group_from))

    group_to = input(instruction_text_manage_groups_move_to)
    validate_instruction(len(possible_groups), group_to)
    group_to_name = get_group_name(int(group_to))

    move(group_from_name, group_to_name)


def instruction_5():
    '''Eliminar casos de un grupo'''

    group = input(instruction_text_manage_groups_remove)
    validate_instruction(len(possible_groups), group)
    group_name = get_group_name(int(group))
    remove(group_name)


def instruction_6():
    '''Validar casos repetidos de un grupo'''

    group = input(instruction_text_manage_groups_validate)
    validate_instruction(len(possible_groups), group)
    group_name = get_group_name(int(group))
    validate(f'{group_name}.txt')


def run():

    instruction = input(instruction_text_manage_groups)
    validate_instruction(6, instruction)

    if instruction == '1':
        instruction_1()
    if instruction == '2':
        instruction_2()
    if instruction == '3':
        instruction_3()
    if instruction == '4':
        instruction_4()
    if instruction == '5':
        instruction_5()
    if instruction == '6':
        instruction_6()
