
from input_output_functions import (
    read_from_csv,
    get_input
)
from ticket_operations import (
    buy_short_term_ticket,
    buy_long_term_ticket
)


def change_language(language):
    messages = {}
    data = read_from_csv(f'./languages/{language}')
    for row in data:
        messages[row['code_name']] = row['ui_message']
    return messages


def buy_short_term_ticket_ui(messages):
    ticket_types_file = './available_ticket_types/short_term_ticket_types'
    short_term_ticket_types = read_from_csv(ticket_types_file)
    selected_type = get_input(
        'choose_ticket_type',
        messages,
        ticket_data=short_term_ticket_types
    )
    buy_short_term_ticket(selected_type)


def buy_long_term_ticket_ui(messages):
    ticket_types_file = './available_ticket_types/long_term_ticket_types'
    long_term_ticket_types = read_from_csv(ticket_types_file)
    selected_type = get_input(
        'choose_ticket_type',
        messages,
        ticket_data=long_term_ticket_types
    )
    buy_long_term_ticket(selected_type)


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
    language = get_input(
        'choose_language',
        messages, menu_options=available_languages
    )
    messages = change_language(language)

    main_menu_options = [
        'main_menu_buy_a_ticket',
        'main_menu_check_status',
        'main_menu_recharge_ticket'
    ]
    main_menu_option = get_input(
        'choose_action',
        messages, menu_options=main_menu_options
    )

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
