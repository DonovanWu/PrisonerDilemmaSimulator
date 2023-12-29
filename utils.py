def get_user_input(prompt='', default=None, parse=str, choices=None):
    answer = input(prompt)
    if not answer:
        if default is None:
            raise ValueError('Must give an input because default is not set!')
        answer = default
    answer = parse(answer)
    if choices:
        choices = set(choices)
        if answer not in choices:
            raise ValueError('Must choose from: ' + ', '.join(str(item) for item in sorted(choices)))
    return answer


def yes_or_no(s):
    return s.lower() in ('y', 'yes')


def zero_tolerant_division(a, b):
    if b == 0:
        if a > 0:
            return float('inf')
        elif a < 0:
            return -float('inf')
        else:
            return float('nan')
    return a / b
