from pathlib import Path
from datetime import date
from input_output_functions import (
    read_from_csv,
    write_to_csv
)
from classes import (
    Long_Term_Ticket,
    Prepaid_Ticket,
    TicketTypeNotFoundError,
    InvalidTicketDataError,
    InvalidPathError,
    InvalidDataError,
    Ticket_Not_in_DatabaseError
)


def buy_short_term_ticket(ticket_to_buy: dict, folder_path: str):
    """
    Updates short_term_tickets_data file which holds info
    how much of each short term ticket type was bought

    ticket_to_buy - dicts with ticket info
    folder_path - holds path to a folder where file should be located
    """
    file_name = folder_path + './short_term_tickets_data'
    path = Path(file_name + '.txt')

    if not Path(folder_path).is_dir():
        raise InvalidPathError

    # Getting current ticket info
    tickets_data_from_database = []
    if not path.is_file():
        ticket_types_file = './available_ticket_types/short_term_ticket_types'
        available_ticket_types = read_from_csv(ticket_types_file)
        for ticket_type in available_ticket_types:
            tickets_data_from_database.append({
                'ticket_type': ticket_type['name'],
                'number_sold': 0
            })
    else:
        tickets_data_from_database = read_from_csv(file_name)

    try:
        # Adding a ticket
        found_ticket = False
        for ticket in tickets_data_from_database:
            if ticket['ticket_type'] == ticket_to_buy['name']:
                ticket['number_sold'] = int(ticket['number_sold']) + 1
                found_ticket = True
        if not found_ticket:
            raise TicketTypeNotFoundError
    except KeyError:
        raise InvalidTicketDataError

    # Updating the database
    headers = ['ticket_type', 'number_sold']
    write_to_csv(file_name, tickets_data_from_database, headers)


def choose_id(database_path: str) -> int:
    """
    Returns id which should be next in the database.
    """
    try:
        with open(database_path + '/last_id.txt', 'r') as file_handle:
            new_id = int(file_handle.readline()) + 1
    except FileNotFoundError:
        raise InvalidPathError
    except ValueError:
        raise InvalidDataError

    with open(database_path + '/last_id.txt', 'w') as file_handle:
        file_handle.write(str(new_id))
    return new_id


def buy_long_term_ticket(ticket_to_buy: dict, folder_path: str) -> int:
    """
    Sets ticket's id.
    Creates instance of Long_Term_Ticket class.
    Returns created ticket's id.
    """
    id = choose_id(folder_path)

    current_date = date.today().isoformat()
    try:
        ticket_duration = int(ticket_to_buy['duration'])
    except KeyError:
        raise InvalidTicketDataError
    except ValueError:
        raise InvalidTicketDataError

    Long_Term_Ticket(id, current_date, ticket_duration, folder_path)
    return id


def get_ticket_from_database(id: int, folder_path: str) -> Long_Term_Ticket:
    """
    Returns instance of Long_Term_Ticket class from data
    existing in database.
    """
    if not Path((f'{folder_path}/{id}' + '.txt')).is_file():
        raise Ticket_Not_in_DatabaseError
    ticket_data = read_from_csv(f'{folder_path}/{id}')[0]

    try:
        ticket = Long_Term_Ticket(
            int(ticket_data['id']),
            ticket_data['date_of_purchase'],
            int(ticket_data['duration']),
            folder_path
        )
    except KeyError:
        raise InvalidDataError
    except ValueError:
        raise InvalidDataError
    return ticket


def check_long_term_ticket_status(id: int, folder_path: str) -> dict:
    """
    Checks status of ticket with given id.
    Returns dict with 'days_left' and 'expires' keys
    """
    ticket = get_ticket_from_database(id, folder_path)
    return ticket.check_status()


def can_ticket_be_prolonged(id: int, folder_path: str) -> list:
    """
    Return 2 element list.
    First element is True if ticket can be prolonged.
    Second element is a number of days till expiration
    to allow prolonging (7)
    """
    days_left_to_allow_prolonging = 7
    status_info = check_long_term_ticket_status(id, folder_path)
    if status_info['days_left'] <= days_left_to_allow_prolonging:
        return [True, days_left_to_allow_prolonging]
    return [False, days_left_to_allow_prolonging]


def prolong_long_term_ticket(id: int, added_ticket: dict, folder_path: str):
    """
    Prolongs ticket with given id with duration of given ticket type
    """
    ticket = get_ticket_from_database(id, folder_path)
    try:
        added_duration = int(added_ticket['duration'])
    except KeyError:
        raise InvalidDataError
    except ValueError:
        raise InvalidDataError
    ticket.prolong_ticket(added_duration)


def buy_prepaid_ticket(ticket_to_buy: dict, folder_path: str) -> int:
    """
    Sets ticket's id.
    Creates instance of Prepaid_Ticket class.
    Returns created ticket's id.
    """
    id = choose_id(folder_path)

    try:
        value = float(ticket_to_buy['value'])
    except KeyError:
        raise InvalidTicketDataError
    except ValueError:
        raise InvalidTicketDataError
    Prepaid_Ticket(id, value, folder_path)
    return id


def get_prepaid_ticket_from_database(
    id: int, folder_path: str
) -> Prepaid_Ticket:
    """
    Returns instance of Prepaid_Ticket class from
    data existing in database.
    """
    if not Path((f'{folder_path}/{id}' + '.txt')).is_file():
        raise Ticket_Not_in_DatabaseError
    ticket_data = read_from_csv(f'{folder_path}/{id}')[0]

    try:
        ticket = Prepaid_Ticket(
            int(ticket_data['id']),
            float(ticket_data['balance']),
            folder_path
        )
    except KeyError:
        raise InvalidDataError
    except ValueError:
        raise InvalidDataError
    return ticket


def check_prepaid_balance(id: int, folder_path: str) -> float:
    """
    Returns balance of ticket in database with given id
    """
    ticket = get_prepaid_ticket_from_database(id, folder_path)
    return ticket.check_balance()


def recharge_prepaid_ticket(id: int, added_ticket: dict, folder_path: str):
    """
    Increases balance of ticket with given id with value of given ticket type
    """
    ticket = get_prepaid_ticket_from_database(id, folder_path)
    try:
        added_value = float(added_ticket['value'])
    except KeyError:
        raise InvalidDataError
    except ValueError:
        raise InvalidDataError
    ticket.recharge_ticket(added_value)


def use_prepaid_ticket(
    id: int, bought_ticket: dict,
    database_folder_path: str
) -> bool:
    """
    If ticket's balance is enough, decrements bought_ticket's
    price from it.
    Returns True if balance was enough.
    """
    folder_path = database_folder_path + './prepaid_tickets'
    ticket = get_prepaid_ticket_from_database(id, folder_path)
    try:
        price = float(bought_ticket['price'])
    except KeyError:
        raise InvalidDataError
    except ValueError:
        raise InvalidDataError

    if ticket.use_prepaid(price):
        buy_short_term_ticket(bought_ticket, database_folder_path)
        return 1
    return 0
