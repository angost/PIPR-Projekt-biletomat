
import csv

class Ticket:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def save_to_file(self):
        with open(f'{self.id}.txt', 'w') as file_handle:
            headers = [self.id] + list(self.data.keys())
            file_data = {'id': self.id}
            for property in self.data:
                file_data[property] = self.data[property]

            writer = csv.DictWriter(file_handle, headers)
            writer.writeheader()
            writer.writerow(file_data)


class Long_Term_Ticket(Ticket):
    pass