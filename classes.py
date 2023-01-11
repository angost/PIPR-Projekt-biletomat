
import csv
from datetime import date, timedelta


class Ticket:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def save_to_file(self):
        with open(f'{self.id}.txt', 'w') as file_handle:
            headers = ['id'] + list(self.data.keys())
            file_data = {'id': self.id}
            for property in self.data:
                file_data[property] = self.data[property]

            writer = csv.DictWriter(file_handle, headers)
            writer.writeheader()
            writer.writerow(file_data)


class Long_Term_Time_Ticket(Ticket):
    def __init__(self, id, data):
        super().__init__(id, data)
        # data should include: duration, date_of_purchase
        # data could include: price, discount_type

    def check_status(self):
        current_date = date.today()
        date_of_purchase = date.fromisoformat(self.data['date_of_purchase'])
        duration = timedelta(days=int(self.data['duration']))
        days_left = duration - (current_date - date_of_purchase)
        return max(days_left, timedelta(days=0))

    def recharge_ticket(self, added_duration):
        days_left = self.check_status()
        new_date_of_purchase = date.today().isoformat()
        self.data['date_of_purchase'] = new_date_of_purchase
        # Extend ticket
        if days_left > timedelta(days=0):
            new_duration = int(days_left.days) + added_duration
            self.data['duration'] = new_duration
        # Reload expired ticket
        else:
            self.data['duration'] = added_duration

        self.save_to_file()


class Long_Term_Prepaid_Ticket(Ticket):
    def __init__(self, id, data):
        super().__init__(id, data)
        # data should include: balance, active_ticket

    def check_balance(self):
        return float(self.data['balance'])

    def recharge_ticket(self, value):
        self.data['balance'] = self.check_balance() + value
        self.save_to_file()
        return 1

    def use_prepaid(self, ticket, price):
        self.data['current_ticket'] = ticket
        self.data['balance'] = self.check_balance() - price
        self.save_to_file()
        return 1
