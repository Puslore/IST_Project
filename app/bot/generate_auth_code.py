from random import sample

def generate_auth_code():
    digits = sample(range(10), 4)

    if digits[0] == 0:
        for i in range(1, 4):
            if digits[i] != 0:
                digits[0], digits[i] = digits[i], digits[0]
                break
    code = int(''.join(map(str, digits)))
    return code
