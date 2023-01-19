
import csv
# from ticket_operations import (
# )


def print_options(list_of_options):
    for index, option in enumerate(list_of_options):
        print(index, option)


def get_input(list_of_options, message, messages):
    user_input = None
    while user_input not in range(len(list_of_options)):
        print_options([messages[option] for option in list_of_options])
        try:
            user_input = int(input(messages[message] + ' '))
        except ValueError:
            user_input = None
        print('')
    print('')
    return list_of_options[user_input]


def read_from_csv(file_name):
    data = []
    with open(f'{file_name}.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            data.append(row)
    return data


def change_language(language):
    messages = {}
    with open(f'{language}.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            messages[row['code_name']] = row['ui_message']
    return messages


def buy_short_term_ticket_ui():
    # [{'name': '20_min_reduced', 'price': '1.7'}]
    short_term_ticket_types = read_from_csv('short_term_ticket_types')


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
    language = get_input(available_languages, 'choose_language', messages)
    messages = change_language(language)

    main_menu_options = [
        'main_menu_buy_a_ticket',
        'main_menu_check_status',
        'main_menu_recharge_ticket'
    ]
    main_menu_option = get_input(main_menu_options, 'choose_action', messages)

    # BUY A TICKET
    if main_menu_option == main_menu_options[0]:
        main_menu_buy_a_ticket_options = {
            'buy_short_term_ticket': buy_short_term_ticket_ui,
            'buy_long_term_ticket': buy_long_term_ticket_ui,
            'assign_to_prepaid': assign_to_prepaid_ui
        }
        main_menu_buy_a_ticket_option = get_input(
            list(main_menu_buy_a_ticket_options.keys()),
            'choose_action',
            messages
        )
        main_menu_buy_a_ticket_options[main_menu_buy_a_ticket_option]()
    # CHECK STATUS
    elif main_menu_option == main_menu_options[1]:
        main_menu_check_status_options = {
            'check_status': check_status_ui,
            'check_balance': check_balance_ui
        }
        main_menu_check_status_option = get_input(
            list(main_menu_check_status_options.keys()),
            'choose_action',
            messages
        )
        main_menu_check_status_options[main_menu_check_status_option]()
    # RECHARGE
    elif main_menu_option == main_menu_options[2]:
        main_menu_recharge_options = {
            'recharge_time_ticket': recharge_time_ticket_ui,
            'recharge_prepaid_ticket': recharge_prepaid_ticket_ui
        }
        main_menu_recharge_option = get_input(
            list(main_menu_recharge_options.keys()),
            'choose_action',
            messages
        )
        main_menu_recharge_options[main_menu_recharge_option]()
