import re
from django import template

register = template.Library()


@register.filter()
def censor(text):
    # Список нежелательных слов

    stop_list = ['Гидра', 'Скотина', 'Падла',
                 'Гнида', 'Редиска',
                 'Padla', 'CkotiHa',
                 'Padla', 'GHida', 'Редиска',
                 'П4дл4', 'Плохой', 'Фигня']

    # Замена букв в нежелательных словах на '*'
    for word in stop_list:
        pattern = re.compile(word, re.IGNORECASE)
        text = pattern.sub(word[0] + "*" * len(word), text)

    return text
