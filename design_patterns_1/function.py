
def fact(x):
    if x == 0:
        return 1
    return x * fact(x - 1)

def f(x, b):
    x = x ** b
    return fact(x)

def main():
    x = int(input("Enter x: "))
    b = int(input("Enter b: "))
    print(f(x, b))


if __name__ == '__main__':
    main()

