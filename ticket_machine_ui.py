# Dictionary of message codes to ui messages in different languages
messages = {
    'choose_language': {
        'ENG': 'Choose a language',
        'PL': 'Wybierz jezyk'
    },
    'choose_action': {
        'ENG': 'Choose an action',
        'PL': 'Wybierz akcje'
    },
    'ENG': {
        'ENG': 'English',
        'PL': 'Angielski'
    },
    'PL': {
        'ENG': 'English',
        'PL': 'Angielski'
    },

}


def print_options(list_of_options):
    for index, option in enumerate(list_of_options):
        print(index, option)


def get_input(list_of_options, message):
    user_input = None
    while user_input not in range(len(list_of_options)):
        print_options(list_of_options)
        try:
            user_input = int(input(message))
        except ValueError:
            user_input = None
    return list_of_options[user_input]


def ui(messages):
    available_languages = ['ENG', 'PL']
    language = get_input(available_languages, 'choose_language')
    main_menu_options = [
        'buy_short_term_ticket',
        'buy_long_term_ticket',
        'other_long_term_ticket'
        ]
