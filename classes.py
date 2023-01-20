
from datetime import date, timedelta
from pathlib import Path
from input_output_functions import (
    # read_from_csv,
    write_to_csv
)


class Long_Term_Ticket():
    def __init__(self, id: int, date_of_purchase: str, duration: int, folder_path: str):
        """
        Creates instance of Long_Term_Ticket object.
        Creates a file with its data.
        """
        if id < 0:
            raise Exception
        if date.fromisoformat(date_of_purchase) > date.today():
            raise Exception
        if duration < 0:
            raise Exception
        if not Path(folder_path).is_dir():
            raise Exception

        self.id = id
        self.date_of_purchase = date_of_purchase
        self.duration = duration
        self.path = folder_path + f'/{self.id}'
        if not Path(self.path + '.txt').is_file():
            self.save_to_file()

    def save_to_file(self):
        """
        Saves ticket data to a file. Creates it or overrides its content
        """
        headers = ['id', 'date_of_purchase', 'duration']
        ticket_data = [{
            'id': self.id,
            'date_of_purchase': self.date_of_purchase,
            'duration': self.duration
        }]
        write_to_csv(self.path, ticket_data, headers)

    def check_status(self) -> dict:
        """
        Returns dict{'days_left': int, 'expires': str}
        with status info
        """
        current_date = date.today()
        date_of_purchase = date.fromisoformat(self.date_of_purchase)
        duration = timedelta(days=int(self.duration))
        days_left = duration - (current_date - date_of_purchase)
        status_info = {
            'days_left': max(days_left, timedelta(days=0)).days,
            'expires': (date_of_purchase + duration).isoformat()}
        return status_info

    def prolong_ticket(self, added_duration: int):
        """
        Changes ticket's duration
        to added_duration + days_left if there are any.
        Sets date_of_purchase to current day
        """
        if added_duration < 0:
            raise Exception
        days_left = self.check_status()['days_left']
        new_date_of_purchase = date.today().isoformat()
        self.date_of_purchase = new_date_of_purchase
        # Extend ticket
        if days_left:
            new_duration = days_left + added_duration
            self.duration = new_duration
        # Reload expired ticket
        else:
            self.duration = added_duration

        self.save_to_file()


class Prepaid_Ticket():
    def __init__(self, id: int, balance: float, folder_path: str):
        """
        Creates instance of Prepaid_Ticket object.
        Creates a file with its data.
        """
        if id < 0:
            raise Exception
        if balance < 0:
            raise Exception
        if not Path(folder_path).is_dir():
            raise Exception

        self.id = id
        self.balance = balance
        self.path = folder_path + f'/{self.id}'
        if not Path(self.path + '.txt').is_file():
            self.save_to_file()

    def save_to_file(self):
        """
        Saves ticket data to a file. Creates it or overrides its content
        """
        headers = ['id', 'balance']
        ticket_data = [{
            'id': self.id,
            'balance': self.balance
        }]
        write_to_csv(self.path, ticket_data, headers)

    def check_balance(self) -> float:
        """
        Returns ticket's balance
        """
        return self.balance

    def recharge_ticket(self, value: float):
        """
        Adds value to ticket's balance
        """
        if value < 0:
            raise Exception
        self.balance = round(self.check_balance() + value, 2)
        self.save_to_file()

    def use_prepaid(self, price: float) -> bool:
        """
        Decrements price from ticket's balance.
        Returns False if balance is too low.
        """
        if price < 0:
            raise Exception
        new_balance = round(self.check_balance() - price, 2)
        if new_balance >= 0.0:
            self.balance = new_balance
            self.save_to_file()
            return 1
        return 0
