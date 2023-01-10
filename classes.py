
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

    def check_status(self):
        current_date = date.today()
        date_of_purchase = date.fromisoformat(self.data['date_of_purchase'])
        duration = timedelta(days=int(self.data['duration']))
        days_left = duration - (current_date - date_of_purchase)
        return max(days_left, timedelta(days=0))


class Long_Term_Prepaid_Ticket(Ticket):
    def __init__(self, id, data):
        super().__init__(id, data)
