from pathlib import Path
from datetime import date
from input_output_functions import (
    read_from_csv,
    write_to_csv
)
from classes import Long_Term_Ticket


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


def buy_long_term_ticket(ticket_to_buy):
    database_path = './ticket_database/long_term_tickets'
    # Choose id
    with open(database_path + '/last_id.txt', 'r') as file_handle:
        new_id = int(file_handle.readline()) + 1
    with open(database_path + '/last_id.txt', 'w') as file_handle:
        file_handle.write(str(new_id))
    # Create Long_Term_Ticket instance
    current_date = date.today()
    Long_Term_Ticket(new_id, current_date, ticket_to_buy['duration'])
