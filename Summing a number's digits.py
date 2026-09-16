def sum_digits(dm_number):
    return sum(int(dm_char) for dm_char in str(abs(dm_number)))
