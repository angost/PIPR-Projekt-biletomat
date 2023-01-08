
messages = {

}


def print_options(list_of_options):
    for index, option in enumerate(list_of_options):
        print(index, option)


def get_input(list_of_options, message):
    user_input = None
    while user_input not in range(len(list_of_options)):
        print_options(list_of_options)
        user_input = int(input(message))
    return list_of_options[user_input]


def ui(messages):
    available_languages = ['ENG', 'PL']
    language = get_input(available_languages, 'Choose a language')
    pass
