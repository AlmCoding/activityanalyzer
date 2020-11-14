import re
from datetime import datetime, timedelta


def parse_amount(amount: str) -> float:
    separators = re.findall(r'[^\d]', amount)
    decimal_separator = separators[-1]
    thousands_separator = ',' if decimal_separator == '.' else '.'
    amount = amount.replace(thousands_separator, '')
    amount = amount.replace(decimal_separator, '.')
    return float(amount)


def parse_date(date, format_context, time_delta=None):
    date_format = format_context['date']
    if time_delta:
        return datetime.strptime(date, date_format) + timedelta(**time_delta)
        # return datetime.strptime(date, date_format) + timedelta(hours=23, minutes=59)
    return datetime.strptime(date, date_format)
