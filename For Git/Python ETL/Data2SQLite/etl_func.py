
def time_normalize(time: str):
    # Example
    #
    # Input: '14:6:9'
    # Output: '14:06:09'

    d = time.split(':')
    # print(d)
    out = ''
    for w in d:
        # Две цифры после двоеточия
        if len(w) == 2:
            out += w + ':'

        # Одна цифра после двоеточия
        elif len(w) == 1:
            out += '0' + w + ':'

        # Ни одной цифры после двоеточия
        elif len(w) == 0:
            out += '00:'

        # Непредвиденный случай
        else:
            out += w + ':'

    # Обрезка двоеточия в конце строки
    out = out.rstrip(':')

    return out


# ------ ------
# print(time_normalize('14:6:9'))


def date_normalize(date: str):
    # Example
    #
    # Input: '2.10.2014'
    # Output: '2014-10-02'

    f = date.split('.')
    # print(f)
    out = ''

    for w in f:

        # Одна цифра
        if len(w) == 1:
            out = '0' + w + '-' + out

        # Две цифры
        elif len(w) == 2:
            out = w + '-' + out

        # 4 цифры, и все остальные случаи
        else:
            out = w + '-' + out

    # Удаление минуса в конце строки
    out = out.rstrip('-')

    return out


# print( date_normalize('2.10.2014') )


# a = date.fromisoformat('2.10.2014')
# print(date.fromisoformat('2.10.2014'))

def dt_normalize(dt: str):
    # Example
    #
    # Input: '2.10.2014 14:6:9'
    # Output: '2014-10-02 14:06:09'

    out = ''
    str_buff = dt.split(' ')
    out = date_normalize(str_buff[0]) + ' ' + time_normalize(str_buff[1])

    return out


# print( dt_normalize('2.10.2014 14:6:9') )

def dt_normalize_list(dt: list):
    # Example
    #
    # Input: ['2.10.2014 14:6:9']
    # Output: ['2014-10-02 14:06:09']

    out = []
    for w in dt:
        str_buff = w.split(' ')
        out.append(date_normalize(str_buff[0]) + ' ' + time_normalize(str_buff[1]))

    return out

print( dt_normalize_list(['2.10.2014 14:6:9']) )
