
from datetime import date, timedelta
from pathlib import Path
from input_output_functions import (
    # read_from_csv,
    write_to_csv
)


class Long_Term_Ticket():
    def __init__(self, id, date_of_purchase, duration):
        self.id = id
        self.date_of_purchase = date_of_purchase
        self.duration = duration
        self.path = f'./ticket_database/long_term_tickets/{self.id}'
        if not Path(self.path + '.txt').is_file():
            self.save_to_file()

    def save_to_file(self):
        headers = ['id', 'date_of_purchase', 'duration']
        ticket_data = [{
            'id': self.id,
            'date_of_purchase': self.date_of_purchase,
            'duration': self.duration
        }]
        write_to_csv(self.path, ticket_data, headers)

    def check_status(self):
        current_date = date.today()
        date_of_purchase = date.fromisoformat(self.date_of_purchase)
        duration = timedelta(days=int(self.duration))
        days_left = duration - (current_date - date_of_purchase)
        status_info = {
            'days_left': max(days_left, timedelta(days=0)).days,
            'expires': (date_of_purchase + duration).isoformat()}
        return status_info

    def prolong_ticket(self, added_duration):
        days_left = self.check_status()['days_left']
        new_date_of_purchase = date.today().isoformat()
        self.date_of_purchase = new_date_of_purchase
        # Extend ticket
        if days_left:
            new_duration = int(days_left) + int(added_duration)
            self.duration = str(new_duration)
        # Reload expired ticket
        else:
            self.duration = added_duration

        self.save_to_file()


class Prepaid_Ticket():
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.path = f'./ticket_database/prepaid_tickets/{self.id}'
        if not Path(self.path + '.txt').is_file():
            self.save_to_file()

    def save_to_file(self):
        headers = ['id', 'balance']
        ticket_data = [{
            'id': self.id,
            'balance': self.balance
        }]
        write_to_csv(self.path, ticket_data, headers)

    def check_balance(self):
        return self.balance

    def recharge_ticket(self, value):
        self.balance = self.check_balance() + value
        self.save_to_file()

    def use_prepaid(self, price):
        new_balance = self.check_balance() - price
        if new_balance:
            self.balance = new_balance
            self.save_to_file()
