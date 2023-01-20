
from datetime import date, timedelta
from pathlib import Path
from input_output_functions import (
    read_from_csv,
    write_to_csv
)
from classes import Long_Term_Ticket, Prepaid_Ticket


def test_create_Long_Term_Ticket():
    ticket = Long_Term_Ticket(0, '2023-01-20', 30)
    assert ticket.id == 0
    assert ticket.date_of_purchase == '2023-01-20'
    assert ticket.duration == 30
    path = './ticket_database/long_term_tickets/0'
    assert Path(path + '.txt').is_file()
    file = read_from_csv(path)
    assert len(file) == 1
    ticket_data = file[0]
    assert len(ticket_data) == 3
    assert ticket_data['id'] == '0'
    assert ticket_data['date_of_purchase'] == '2023-01-20'
    assert ticket_data['duration'] == '30'
