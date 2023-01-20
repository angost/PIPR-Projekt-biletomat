from pathlib import Path
from datetime import date
from input_output_functions import (
    read_from_csv,
    write_to_csv
)
from classes import Long_Term_Ticket, Prepaid_Ticket


def buy_short_term_ticket(ticket_to_buy):
    file_name = './ticket_database/short_term_tickets_data'
    path = Path(file_name + '.txt')

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

    # Adding a ticket
    for ticket in tickets_data_from_database:
        if ticket['ticket_type'] == ticket_to_buy['name']:
            ticket['number_sold'] = int(ticket['number_sold']) + 1

    # Updating the database
        headers = ['ticket_type', 'number_sold']
        write_to_csv(file_name, tickets_data_from_database, headers)


def choose_id(database_path):
    with open(database_path + '/last_id.txt', 'r') as file_handle:
        new_id = int(file_handle.readline()) + 1
    with open(database_path + '/last_id.txt', 'w') as file_handle:
        file_handle.write(str(new_id))
    return new_id


def buy_long_term_ticket(ticket_to_buy):
    id = choose_id('./ticket_database/long_term_tickets')
    current_date = date.today()
    Long_Term_Ticket(new_id, current_date, ticket_to_buy['duration'])


def get_ticket_from_database(id):
    path = './ticket_database/long_term_tickets'
    ticket_data = read_from_csv(f'{path}/{id}')[0]
    ticket = Long_Term_Ticket(
        ticket_data['id'],
        ticket_data['date_of_purchase'],
        ticket_data['duration']
    )
    return ticket


def check_long_term_ticket_status(id):
    ticket = get_ticket_from_database(id)
    return ticket.check_status()


def can_ticket_be_prolonged(id):
    days_left_to_allow_prolonging = 7
    status_info = check_long_term_ticket_status(id)
    if status_info['days_left'] <= days_left_to_allow_prolonging:
        return True
    return False


def prolong_long_term_ticket(id, added_ticket):
    ticket = get_ticket_from_database(id)
    added_duration = added_ticket['duration']
    ticket.prolong_ticket(added_duration)


def buy_prepaid_ticket(ticket_to_buy):
    id = choose_id('./ticket_database/prepaid_tickets')
    Prepaid_Ticket(id, ticket_to_buy['value'])


def get_prepaid_ticket_from_database(id):
    path = './ticket_database/prepaid_tickets'
    ticket_data = read_from_csv(f'{path}/{id}')[0]
    ticket = Prepaid_Ticket(
        ticket_data['id'],
        ticket_data['balance']
    )
    return ticket


def check_prepaid_balance(id):
    ticket = get_prepaid_ticket_from_database(id)
    return ticket.check_balance()


def use_prepaid_ticket():
    pass
