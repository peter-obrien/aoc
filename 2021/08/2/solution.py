result = 0

def get_one(patterns):
    for pattern in patterns:
        if len(pattern) == 2:
            return pattern

def get_seven(patterns):
    for pattern in patterns:
        if len(pattern) == 3:
            return pattern

def get_four(patterns):
    for pattern in patterns:
        if len(pattern) == 4:
            return pattern

def get_eight(patterns):
    for pattern in patterns:
        if len(pattern) == 7:
            return pattern

def get_three(patterns, one, four):
    fmo = list(set(one).symmetric_difference(set(four)))
    for pattern in patterns:
        if len(pattern) == 5:
            if ((fmo[0] in pattern and fmo[1] not in pattern) or (fmo[1] in pattern and fmo[0] not in pattern)) and one[0] in pattern and one[1] in pattern:
                return pattern

def get_two(patterns, one, three, four):
    fmo = list(set(one).symmetric_difference(set(four)))
    for pattern in patterns:
        if len(pattern) == 5:
            if ((fmo[0] in pattern and fmo[1] not in pattern) or (fmo[1] in pattern and fmo[0] not in pattern)) and pattern != three:
                return pattern

def get_five(patterns, two, three):
    for pattern in patterns:
        if len(pattern) == 5:
            if pattern != two and pattern != three:
                return pattern

def get_zero(patterns, five):
    for pattern in patterns:
        if len(pattern) == 6:
            if not (five[0] in pattern and five[1] in pattern and five[2] in pattern and five[3] in pattern and five[4] in pattern):
                return pattern

def get_nine(patterns, zero, seven):
    for pattern in patterns:
        if len(pattern) == 6:
            if (seven[0] in pattern and seven[1] in pattern and seven[2] in pattern) and pattern != zero:
                return pattern

def get_six(patterns, zero, nine):
    for pattern in patterns:
        if len(pattern) == 6:
            if pattern != zero and pattern != nine:
                return pattern

def decode_signal(signal):
    mapping = signal.strip().split(' | ')[0]
    output = signal.strip().split(' | ')[1]
    patterns = mapping.split()
    one = get_one(patterns)
    seven = get_seven(patterns)
    four = get_four(patterns)
    eight = get_eight(patterns)
    three = get_three(patterns, one, four)
    two = get_two(patterns, one, three, four)
    five = get_five(patterns, two, three)
    zero = get_zero(patterns, five)
    nine = get_nine(patterns, zero, seven)
    six = get_six(patterns, zero, nine)
    output_str = ""
    for digit in output.split():
        digit = sorted(digit)
        if digit == sorted(zero):
            output_str += "0"
        elif digit == sorted(one):
            output_str += "1"
        elif digit == sorted(two):
            output_str += "2"
        elif digit == sorted(three):
            output_str += "3"
        elif digit == sorted(four):
            output_str += "4"
        elif digit == sorted(five):
            output_str += "5"
        elif digit == sorted(six):
            output_str += "6"
        elif digit == sorted(seven):
            output_str += "7"
        elif digit == sorted(eight):
            output_str += "8"
        elif digit == sorted(nine):
            output_str += "9"
    return int(output_str)



with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        result += decode_signal(line)
print(result)