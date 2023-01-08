
import csv


def print_options(list_of_options):
    for index, option in enumerate(list_of_options):
        print(index, option)


def get_input(list_of_options, message, messages):
    user_input = None
    while user_input not in range(len(list_of_options)):
        print_options([messages[option] for option in list_of_options])
        try:
            user_input = int(input(message))
        except ValueError:
            user_input = None
    return list_of_options[user_input]


def change_language(language):
    messages = {}
    with open(f'{language}.txt', 'r') as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            messages[row['code_name']] = row['ui_message']
    return messages


def ui():
    messages = change_language('ENG')
    available_languages = ['ENG', 'PL']
    language = get_input(available_languages, 'choose_language', messages)
    # main_menu_options = [
    #     'buy_short_term_ticket',
    #     'buy_long_term_ticket',
    #     'other_long_term_ticket'
    #     ]
