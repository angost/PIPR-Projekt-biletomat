
from datetime import date, timedelta
from pathlib import Path
from input_output_functions import (
    read_from_csv,
    write_to_csv
)


# class Ticket:
#     def __init__(self, id, data):
#         self.id = id
#         self.data = data
#         self.save_to_file()

#     def save_to_file(self):
#         with open(f'{self.id}.txt', 'w') as file_handle:
#             headers = ['id'] + list(self.data.keys())
#             file_data = {'id': self.id}
#             for property in self.data:
#                 file_data[property] = self.data[property]

#             writer = csv.DictWriter(file_handle, headers)
#             writer.writeheader()
#             writer.writerow(file_data)


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
        return max(days_left, timedelta(days=0))

    # def recharge_ticket(self, added_duration):
    #     days_left = self.check_status()
    #     new_date_of_purchase = date.today().isoformat()
    #     self.data['date_of_purchase'] = new_date_of_purchase
    #     # Extend ticket
    #     if days_left > timedelta(days=0):
    #         new_duration = int(days_left.days) + added_duration
    #         self.data['duration'] = new_duration
    #     # Reload expired ticket
    #     else:
    #         self.data['duration'] = added_duration

    #     self.save_to_file()


# class Long_Term_Prepaid_Ticket(Ticket):
#     def __init__(self, id, data):
#         super().__init__(id, data)
#         # data should include: balance, active_ticket

#     def check_balance(self):
#         return float(self.data['balance'])

#     def recharge_ticket(self, value):
#         self.data['balance'] = self.check_balance() + value
#         self.save_to_file()
#         return 1

#     def use_prepaid(self, ticket, price):
#         self.data['assigned_ticket'] = ticket
#         self.data['balance'] = self.check_balance() - price
#         self.save_to_file()
#         return 1
