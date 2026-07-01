import re


def calculate(query: str):

    try:
        expression = "".join(
            re.findall(r"[0-9\+\-\*\/\(\)\.\%]+", query)
        )

        return str(eval(expression))

    except Exception as e:
        return str(e)
