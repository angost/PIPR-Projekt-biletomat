
import csv
from tabulate import tabulate
# from ticket_operations import (
# )


def read_from_csv(file_name):
    data = []
    with open(f'{file_name}.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            data.append(row)
    return data


def print_menu_options(list_of_options, messages):
    '''Converts raw options into readable options in given language'''
    for index, option in enumerate(list_of_options):
        print(index, messages[option])


def print_ticket_data(list_of_options, messages):
    '''Displays ticket data in a table'''
    options_data = []
    headers = ['']
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
            headers.append(messages['value'])
        options_data.append(option_data)

    print(tabulate(options_data, headers=headers, showindex="always", tablefmt="simple_grid", floatfmt=".2f"))


def get_input(message, messages, menu_options=None, ticket_data=None):
    # Choosing input type
    if menu_options is not None:
        input_type = 'menu'
    else:
        input_type = 'ticket_data'

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
    while user_input not in range(len(list_of_options[input_type])):
        print_function[input_type](list_of_options[input_type], messages)
        try:
            user_input = int(input(messages[message] + ' '))
        except ValueError:
            user_input = None
        print('')
    print('')
    return list_of_options[input_type][user_input]


def change_language(language):
    messages = {}
    with open(f'{language}.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            messages[row['code_name']] = row['ui_message']
    return messages


def buy_short_term_ticket_ui(messages):
    # [{'name': '20_min_reduced', 'price': '1.7'}]
    short_term_ticket_types = read_from_csv('short_term_ticket_types')
    print_ticket_data(short_term_ticket_types, messages)


def buy_long_term_ticket_ui():
    pass


def assign_to_prepaid_ui():
    pass


def check_status_ui():
    pass


def check_balance_ui():
    pass


def recharge_time_ticket_ui():
    pass


def recharge_prepaid_ticket_ui():
    pass


def ui():
    messages = change_language('ENG')
    available_languages = ['ENG', 'PL']
    language = get_input('choose_language', messages, menu_options=available_languages)
    messages = change_language(language)

    main_menu_options = [
        'main_menu_buy_a_ticket',
        'main_menu_check_status',
        'main_menu_recharge_ticket'
    ]
    main_menu_option = get_input('choose_action', messages, menu_options=main_menu_options)

    # BUY A TICKET
    if main_menu_option == main_menu_options[0]:
        main_menu_buy_a_ticket_options = {
            'buy_short_term_ticket': buy_short_term_ticket_ui,
            'buy_long_term_ticket': buy_long_term_ticket_ui,
            'assign_to_prepaid': assign_to_prepaid_ui
        }

        main_menu_buy_a_ticket_option = get_input(
            'choose_action',
            messages,
            menu_options=list(main_menu_buy_a_ticket_options.keys())
        )
        main_menu_buy_a_ticket_options[main_menu_buy_a_ticket_option](messages)
    # CHECK STATUS
    elif main_menu_option == main_menu_options[1]:
        main_menu_check_status_options = {
            'check_status': check_status_ui,
            'check_balance': check_balance_ui
        }

        main_menu_check_status_option = get_input(
            'choose_action',
            messages,
            menu_options=list(main_menu_check_status_options.keys())
        )
        main_menu_check_status_options[main_menu_check_status_option]()
    # RECHARGE
    elif main_menu_option == main_menu_options[2]:
        main_menu_recharge_options = {
            'recharge_time_ticket': recharge_time_ticket_ui,
            'recharge_prepaid_ticket': recharge_prepaid_ticket_ui
        }

        main_menu_recharge_option = get_input(
            'choose_action',
            messages,
            menu_options=list(main_menu_recharge_options.keys())
        )
        main_menu_recharge_options[main_menu_recharge_option]()

ui()