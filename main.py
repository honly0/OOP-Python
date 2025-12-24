import math


def task_integer6():
    """
    Integer6.
    Given a two-digit integer number.
    Output first its left digit (tens),
    and then its right digit (ones).
    """
    try:
        n = int(input("Enter a two-digit number: "))
        if n < 10 or n > 99:
            raise ValueError
    except:
        print("ERROR: You must enter a POSITIVE two-digit INTEGER!")
    else:
        tens = n // 10
        ones = n % 10
        print("Tens digit:", tens)
        print("Ones digit:", ones)



def task_math1():
    """
    Calculate mathematical expression (Table 2, Variant 1)
    """
    try:
        x = float(input("Enter x: "))
    except:
        print("ERROR: x must be a NUMBER!")
    else:
        try:
            sin_x2 = math.sin(x ** 2) ** 2
            numerator = math.log(x ** 2 + math.cos(math.radians(37))) ** 2
            denominator = sin_x2 + math.sqrt(abs(1 - 2 * math.cos(x) - sin_x2))
            y = numerator / denominator
        except:
            print("ERROR: Calculation error!")
        else:
            print("y =", y)



def task_boolean1():
    """
    Boolean1.
    Given integer A, check if A is positive.
    """
    try:
        A = int(input("Enter A: "))
    except:
        print("ERROR: A must be INTEGER!")
    else:
        result = A > 0
        print("A is positive:", result)


if __name__ == "__main__":
    print("=== PRACTICAL WORK №1 ===\n")

    task_integer6()
    print("\n------------------------\n")

    task_math1()
    print("\n------------------------\n")

    task_boolean1()

    input("\nPress Enter to exit...")
