import json


def example(**kwargs):

    data = {
        "español": f"{kwargs.get('titulo')}",
        "español2": f"{kwargs.get('dato')}"
    }
    print(data[kwargs['variable']])


example(dato="datazo", variable="español")
