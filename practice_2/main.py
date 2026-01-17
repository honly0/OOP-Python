import math


def task_if29() -> bool:
    """
    If29.
    Дано ціле число. Вивести його рядок-опис виду
    «негативне парне число», «нульове число»,
    «додатне непарне число» і т.д.
    """
    try:
        n = int(input("Введіть ціле число: "))

        if n == 0:
            print("нульове число")
        else:
            sign = "додатне" if n > 0 else "негативне"
            parity = "парне" if n % 2 == 0 else "непарне"
            print(f"{sign} {parity} число")

        return True
    except ValueError:
        print("Помилка: потрібно ввести ціле число!")
        return False


def task_geom3() -> bool:
    """
    Завдання 2. Геометрична область, варіант 3.
    Дано (xi, yi) — координати точок. Порахувати кількість точок,
    що потрапляють у жовту область (трикутник мінус коло).

    Використано умови:
    - трикутник 45° у І чверті: x>=0, y>=0, y<=x
    - коло з центром у (0,0): x^2 + y^2 <= r^2
    """
    try:
        r = float(input("Введіть радіус кола r (>0): "))
        if r <= 0:
            print("Помилка: r має бути > 0")
            return False

        n = int(input("Введіть кількість точок n (>=1): "))
        if n <= 0:
            print("Помилка: n має бути >= 1")
            return False

        count = 0

        for i in range(n):
            print(f"\nТочка {i + 1}:")
            x = float(input("x = "))
            y = float(input("y = "))

            in_triangle = (x >= 0) and (y >= 0) and (y <= x)
            in_circle = (x * x + y * y) <= (r * r)

            # жовта область = в трикутнику, але НЕ в колі
            if in_triangle and not in_circle:
                count += 1

        print("\nКількість точок у жовтій області:", count)
        return True

    except ValueError:
        print("Помилка: введено некоректне число!")
        return False


def task_series5() -> bool:
    """
    Завдання 3. Математичний ряд, варіант 5:
        sum_{n=1..inf} (3n-2)! / (100*102*...*(98+2n))

    Умова завершення: |u_n| < e, e=1e-10
    """
    try:
        e = 1e-10
        n = 1
        s = 0.0

        while True:
           
            numerator = math.factorial(3 * n - 2)

          
            denominator = 1
            last = 98 + 2 * n
            for v in range(100, last + 1, 2):
                denominator *= v

            u = numerator / denominator

            if abs(u) < e:
                break

            s += u
            n += 1

            
            if n > 5000:
                print("Зупинка: перевищено ліміт ітерацій.")
                return False

        print("Ряд збігається (за критерієм |u_n| < e)")
        print("Сума ряду =", s)
        print("Кількість ітерацій =", n)
        return True

    except OverflowError:
        print("Помилка: переповнення (числа стали занадто великими).")
        return False
    except ValueError:
        print("Помилка: некоректні обчислення.")
        return False


def main():
    while True:
        print("\n==============================")
        print("Оберіть завдання:")
        print("1 — Завдання 1 (If29)")
        print("2 — Завдання 2 (Геометрія, варіант 3)")
        print("3 — Завдання 3 (Ряд, варіант 5)")
        print("0 — Вихід")
        print("==============================")

        try:
            choice = int(input("Ваш вибір: "))
        except ValueError:
            print("Введіть ціле число (0-3)!")
            continue

        if choice == 0:
            print("Завершення програми.")
            break
        elif choice == 1:
            task_if29()
        elif choice == 2:
            task_geom3()
        elif choice == 3:
            task_series5()
        else:
            print("Невірний номер. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
