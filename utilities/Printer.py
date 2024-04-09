from termcolor import colored

def print_message(title: str, content: str, color: str = "white"):
    """
    Imprime un mensaje con un título y un color específicos.
    :param title: El título del mensaje.
    :param content: El contenido del mensaje.
    :param color: El color del mensaje.
    """
    if color != "white":
        print(colored(f"[{title}]: {content}", color))
    else:
        print(f"[{title}]: {content}")

def print_title_message(content):
    """
    Imprime un mensaje con un formato especial de título.
    :param content: El contenido del mensaje.
    """
    message_length = len(content)
    window_width = 80
    separator_length = (window_width - message_length) // 2
    left_separator = "-" * separator_length
    right_separator = "-" * (window_width - message_length - separator_length)
    print(f"\n{left_separator} {content} {right_separator}")
