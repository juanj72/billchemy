from babel.numbers import format_currency


def colombian_number_format(number):
    if number is None:
        return ""
    try:
        round_number = round(number)
        return format_currency(round_number, "COP", locale="es_CO")
    except Exception as e:
        print(e)
        return ""
