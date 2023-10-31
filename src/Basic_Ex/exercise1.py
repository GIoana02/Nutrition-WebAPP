def fibonacci(n):
    sequence = []
    a, b = 0, 1
    while len(sequence) < n:
        sequence.append(b)
        temp = a
        a = b
        b = temp + b
    return sequence


print(fibonacci(10))
