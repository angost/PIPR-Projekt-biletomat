
import csv
from tabulate import tabulate


def read_from_csv(file_name):
    data = []
    with open(f'{file_name}.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            data.append(row)
    return data


def write_to_csv(file_name, data, headers):
    with open(f'{file_name}.txt', 'w') as file_handle:
        writer = csv.DictWriter(file_handle, headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def print_menu_options(list_of_options, messages):
    '''Converts raw options into readable options in given language'''
    for index, option in enumerate(list_of_options):
        print(index, messages[option])


def print_ticket_data(list_of_options, messages):
    '''Displays ticket data in a table'''
    options_data = []
    headers = ['']
    for option in list_of_options:
        option_data = []
        if 'name' in option.keys():
            option_data.append(messages[option['name']])
            headers.append(messages['ticket_type'])
        if 'price' in option.keys():
            option_data.append(float(option['price']))
            headers.append(messages['ticket_price'])
        if 'value' in option.keys():
            option_data.append(option['value'])
            headers.append(messages['value'])
        options_data.append(option_data)

    print(tabulate(options_data, headers=headers, showindex="always", tablefmt="simple_grid", floatfmt=".2f"))


def get_input(message, messages, menu_options=None, ticket_data=None):
    # Choosing input type
    if menu_options is not None:
        input_type = 'menu'
    else:
        input_type = 'ticket_data'

    print_function = {
        'menu': print_menu_options,
        'ticket_data': print_ticket_data
    }
    list_of_options = {
        'menu': menu_options,
        'ticket_data': ticket_data
    }
    # Getting user input
    user_input = None
    while user_input not in range(len(list_of_options[input_type])):
        print_function[input_type](list_of_options[input_type], messages)
        try:
            user_input = int(input(messages[message] + ' '))
        except ValueError:
            user_input = None
        print('')
    print('')
    return list_of_options[input_type][user_input]
