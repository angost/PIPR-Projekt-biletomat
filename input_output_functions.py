
import csv
from tabulate import tabulate
from pathlib import Path
import os
# from time import sleep


class NoTranslationAvailableError(Exception):
    pass


def clear_screen():
    # Linux/Mac
    if os.name == 'posix':
        os.system('clear')
    # Windows
    else:
        os.system('cls')


def read_from_csv(file_name):
    data = []
    with open(f'{file_name}.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            data.append(row)
    return data


def write_to_csv(file_name, data, headers):
    with open(f'{file_name}.txt', 'w') as file_handle:
        writer = csv.DictWriter(file_handle, headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


# def print_list_menu_options(list_of_options, messages):
#     '''Prints menu options'''
#     for index, option in enumerate(list_of_options):
#         print(index, messages[option])


def print_menu_options(list_of_options: list, messages: dict):
    '''
    Prints translated menu options as a table.
    list_of_options - options as str
    messages - dict translating code names to names in proper language
    '''
    try:
        options = [[messages[option]] for option in list_of_options]
    except KeyError:
        raise NoTranslationAvailableError
    print(tabulate(
        options,
        showindex="always",
        tablefmt="rounded_outline"
    ))


def print_ticket_data(list_of_options: list, messages: dict):
    '''
    Prints translated ticket data as a table.
    list_of_options - options as dicts holding ticket data
    messages - dict translating code names to names in proper language
    '''
    options_data = []
    headers = ['']

    try:
        for option in list_of_options:
            option_data = []
            if 'name' in option.keys():
                option_data.append(messages[option['name']])
                headers.append(messages['ticket_type'])
            if 'price' in option.keys():
                option_data.append(float(option['price']))
                headers.append(messages['ticket_price'])
            if 'value' in option.keys():
                option_data.append(option['value'])
                headers.append(messages['ticket_value'])
            options_data.append(option_data)
    except KeyError:
        raise NoTranslationAvailableError

    print(tabulate(
        options_data,
        headers=headers,
        showindex="always",
        tablefmt="simple_grid",
        floatfmt=".2f")
        )


def get_input(
    message: str,
    messages: dict,
    menu_options: list = None,
    ticket_data: list = None
) -> str | dict:
    """
    Asks for user input until a valid number of option is given.
    If menu_options is given, asks to choose from strings
    and returns one of them.
    If ticket_data is given, asks to choose from dicts with ticket data
    and returns one of them.
    """
    # Choosing input type
    if menu_options is not None:
        input_type = 'menu'
    elif ticket_data is not None:
        input_type = 'ticket_data'
    else:
        raise Exception

    print_function = {
        'menu': print_menu_options,
        'ticket_data': print_ticket_data
    }
    list_of_options = {
        'menu': menu_options,
        'ticket_data': ticket_data
    }
    # Getting user input
    user_input = None
    print('\n> > >\n')
    try:
        while user_input not in range(len(list_of_options[input_type])):
            print_function[input_type](list_of_options[input_type], messages)
            try:
                print('')
                user_input = int(input(messages[message] + ' '))
            except ValueError:
                user_input = None
            clear_screen()
        return list_of_options[input_type][user_input]
    except NoTranslationAvailableError:
        return 0


def get_input_id(message: str, messages: dict, path: str) -> int:
    """
    Asks user for id (number) until id of existing file is given
    """
    user_input = None
    id_exists = False
    print('\n> > >\n')
    try:
        while not id_exists:
            user_input = input(messages[message] + ' ')
            try:
                int(user_input)
                if Path(f'{path}/{user_input}.txt').is_file():
                    id_exists = True
                else:
                    user_input = None
            except ValueError:
                user_input = None

            clear_screen()
        return user_input
    except NoTranslationAvailableError:
        return 0
