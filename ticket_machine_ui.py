
from input_output_functions import (
    read_from_csv,
    get_input,
    get_input_id,
    clear_screen
)
from ticket_operations import (
    buy_short_term_ticket,
    buy_long_term_ticket,
    check_long_term_ticket_status,
    prolong_long_term_ticket,
    can_ticket_be_prolonged,
    buy_prepaid_ticket,
    check_prepaid_balance,
    recharge_prepaid_ticket,
    use_prepaid_ticket
)
from classes import (
    TicketTypeNotFoundError,
    InvalidTicketDataError,
    InvalidPathError,
    InvalidDataError,
    Ticket_Not_in_DatabaseError
)
from input_output_functions import NoInputTypeGivenError


def change_language(language: str):
    """
    Returns dictionary with translations in given language
    """
    messages = {}
    data = read_from_csv(f'./languages/{language}')
    for row in data:
        messages[row['code_name']] = row['ui_message']
    return messages


def change_language_ui(messages: dict) -> dict:
    """
    Gets language from user input
    Returns dictionary with translations in choosen language
    """
    available_languages = ['ENG', 'PL']
    language = get_input(
        'choose_language',
        messages,
        menu_options=available_languages
    )
    return change_language(language)


def choose_short_term_ticket(messages: dict) -> dict:
    """
    Gets short term ticket type from  user input
    """
    ticket_types_file = './available_ticket_types/short_term_ticket_types'
    short_term_ticket_types = read_from_csv(ticket_types_file)
    selected_type = get_input(
        'choose_ticket_type',
        messages,
        ticket_data=short_term_ticket_types
    )
    return selected_type


def buy_short_term_ticket_ui(messages: dict):
    """
    Gets short term ticket type from user input.
    Buys short term ticket.
    """
    selected_type = choose_short_term_ticket(messages)
    buy_short_term_ticket(selected_type, './ticket_database')
    print(messages['ticket_bought'])


def choose_long_term_ticket(messages: dict) -> dict:
    """
    Gets long term ticket type from user input
    """
    ticket_types_file = './available_ticket_types/long_term_ticket_types'
    long_term_ticket_types = read_from_csv(ticket_types_file)
    selected_type = get_input(
        'choose_ticket_type',
        messages,
        ticket_data=long_term_ticket_types
    )
    return selected_type


def buy_long_term_ticket_ui(messages: dict):
    """
    Gets long term ticket type from user input.
    Buys long term ticket.
    """
    selected_type = choose_long_term_ticket(messages)
    path = './ticket_database/long_term_tickets'
    id = buy_long_term_ticket(selected_type, path)
    print(messages['ticket_bought'])
    print(f'{messages["show_id"]}: {id}')


def check_long_term_ticket_status_ui(messages: dict):
    """
    Gets long term ticket id from user input.
    Checks its status.
    """
    path = './ticket_database/long_term_tickets'
    valid_id = get_input_id('enter_id', messages, path)
    status_info = check_long_term_ticket_status(valid_id, path)
    days_left = status_info['days_left']
    expires = status_info['expires']
    if days_left:
        print(f'{messages["days_left"]}: {days_left}')
        print(f'{messages["will_expire"]}: {expires}')
    else:
        print(f'{messages["ticket_expired"]}: {expires}')


def prolong_long_term_ticket_ui(messages: dict):
    """
    Gets long term ticket id from user input.
    Prolongs it.
    """
    # Getting user's ticket
    path = './ticket_database/long_term_tickets'
    valid_id = get_input_id('enter_id', messages, path)
    allow_prolonging = can_ticket_be_prolonged(valid_id, path)
    if allow_prolonging[0]:
        # Choosing a ticket to prolong user's ticket with
        selected_type = choose_long_term_ticket(messages)
        prolong_long_term_ticket(valid_id, selected_type, path)
        print(messages['ticket_prolonged'])
        new_status = check_long_term_ticket_status(valid_id, path)['days_left']
        print(f'{messages["days_left"]}: {new_status}')

    else:
        print(f'{messages["cannot_prolong"]}: {allow_prolonging[1]}')


def choose_prepaid_ticket(messages: dict) -> dict:
    """
    Gets prepaid ticket type from user input
    """
    ticket_types_file = './available_ticket_types/prepaid_ticket_types'
    prepaid_ticket_types = read_from_csv(ticket_types_file)
    selected_type = get_input(
        'choose_value',
        messages,
        ticket_data=prepaid_ticket_types
    )
    return selected_type


def buy_prepaid_ticket_ui(messages: dict):
    """
    Gets prepaid ticket type from user input
    Buys prepaid ticket.
    """
    path = './ticket_database/prepaid_tickets'
    selected_type = choose_prepaid_ticket(messages)
    id = buy_prepaid_ticket(selected_type, path)
    print(messages['ticket_bought'])
    print(f'{messages["show_id"]}: {id}')


def check_prepaid_balance_ui(messages: dict):
    """
    Gets prepaid ticket id from user input.
    Checks its balance.
    """
    path = './ticket_database/prepaid_tickets'
    valid_id = get_input_id('enter_id', messages, path)
    balance = check_prepaid_balance(valid_id, path)
    print(f'{messages["show_balance"]}: {balance} ({messages["currency"]})')


def recharge_prepaid_ticket_ui(messages: dict):
    """
    Gets prepaid ticket id from user input.
    Recharges it.
    """
    # Getting user's ticket
    path = './ticket_database/prepaid_tickets'
    valid_id = get_input_id('enter_id', messages, path)
    # Recharging
    selected_type = choose_prepaid_ticket(messages)
    recharge_prepaid_ticket(valid_id, selected_type, path)
    print(messages['recharged'])
    new_balance = check_prepaid_balance(valid_id, path)
    print(
        f'{messages["show_balance"]}: {new_balance} ({messages["currency"]})'
    )


def use_prepaid_ticket_ui(messages: dict):
    """
    Gets prepaid ticket id from user input.
    Gets short term ticket type from user input.
    Buys short term ticket using prepaid.
    """
    # Getting user's ticket
    path = './ticket_database/prepaid_tickets'
    valid_id = get_input_id('enter_id', messages, path)
    # Selecting short-term ticket
    selected_type = choose_short_term_ticket(messages)
    # Using prepaid if balance is enough
    if use_prepaid_ticket(valid_id, selected_type, './ticket_database'):
        print(messages['ticket_bought'])
        new_balance = check_prepaid_balance(valid_id, path)
        mess_new_balance = messages["show_balance"]
        mess_currency = messages["currency"]
        print(f'{mess_new_balance}: {new_balance} ({mess_currency})')
    else:
        print(messages['balance_too_low'])


def print_current_menu_option(text: str, messages: dict):
    """
    Prints current menu option
    """
    print(messages[text].upper())


def ui(messages: dict):
    """
    Main menu for user to navigate with
    """
    print('')
    print_current_menu_option('menu', messages)
    main_menu_options = [
        'main_menu_buy_a_ticket',
        'main_menu_check_status',
        'main_menu_recharge_ticket',
        'main_menu_change_language'
    ]
    main_menu_option = get_input(
        'choose_action',
        messages,
        menu_options=main_menu_options
    )
    print_current_menu_option(main_menu_option, messages)
    # BUY A TICKET
    if main_menu_option == main_menu_options[0]:
        main_menu_buy_a_ticket_options = {
            'buy_short_term_ticket': buy_short_term_ticket_ui,
            'buy_long_term_ticket': buy_long_term_ticket_ui,
            'buy_prepaid': buy_prepaid_ticket_ui,
            'use_prepaid': use_prepaid_ticket_ui
        }

        main_menu_buy_a_ticket_option = get_input(
            'choose_action',
            messages,
            menu_options=list(main_menu_buy_a_ticket_options.keys())
        )
        print_current_menu_option(main_menu_buy_a_ticket_option, messages)

        main_menu_buy_a_ticket_options[main_menu_buy_a_ticket_option](messages)
    # CHECK STATUS
    elif main_menu_option == main_menu_options[1]:
        main_menu_check_status_options = {
            'check_status': check_long_term_ticket_status_ui,
            'check_balance': check_prepaid_balance_ui
        }

        main_menu_check_status_option = get_input(
            'choose_action',
            messages,
            menu_options=list(main_menu_check_status_options.keys())
        )
        print_current_menu_option(main_menu_check_status_option, messages)

        main_menu_check_status_options[main_menu_check_status_option](messages)
    # RECHARGE
    elif main_menu_option == main_menu_options[2]:
        main_menu_recharge_options = {
            'prolong_long_term_ticket': prolong_long_term_ticket_ui,
            'recharge_prepaid_ticket': recharge_prepaid_ticket_ui
        }

        main_menu_recharge_option = get_input(
            'choose_action',
            messages,
            menu_options=list(main_menu_recharge_options.keys())
        )
        print_current_menu_option(main_menu_recharge_option, messages)

        main_menu_recharge_options[main_menu_recharge_option](messages)
    # CHANGE LANGUAGE
    elif main_menu_option == main_menu_options[3]:
        messages = change_language_ui(messages)
    return messages


def handle_exceptions(messages: dict, e: Exception):
    with open('error_reports.txt', 'a') as file_handle:
        file_handle.write(type(e).__name__)
    print(messages['error'])
    print('')


def main():
    clear_screen()
    messages = change_language('ENG')
    try:
        messages = change_language_ui(messages)
        print(messages['TICKET_MACHINE'])
        print(messages['controls'])
        start_program = get_input(
                'choose_action',
                messages,
                menu_options=['quit', 'start']
        )
        if start_program == 'start':
            continue_loop = True
        else:
            continue_loop = False

        while continue_loop:
            try:
                messages = ui(messages)
            except TicketTypeNotFoundError as e:
                handle_exceptions(messages, e)
                continue_loop = False
            except InvalidTicketDataError as e:
                handle_exceptions(messages, e)
                continue_loop = False
            except InvalidPathError as e:
                handle_exceptions(messages, e)
                continue_loop = False
            except InvalidDataError as e:
                handle_exceptions(messages, e)
                continue_loop = False
            except Ticket_Not_in_DatabaseError as e:
                handle_exceptions(messages, e)
                continue_loop = False
            except NoInputTypeGivenError as e:
                handle_exceptions(messages, e)
                continue_loop = False

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
