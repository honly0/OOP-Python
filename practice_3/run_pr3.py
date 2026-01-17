import pr3_module as m


def main():
    while True:
        print("\n==============================")
        print("Практична робота №3 | Варіант 22")
        print("1 — Task 1 (Proc14: ShiftRight3)")
        print("2 — Task 2 (Matrix22)")
        print("0 — Вихід")
        print("==============================")

        try:
            choice = int(input("Ваш вибір: "))
        except ValueError:
            print("Введіть ціле число (0-2)!")
            continue

        if choice == 0:
            print("Завершення програми.")
            break
        elif choice == 1:
            m.task_proc14_io()
        elif choice == 2:
            m.matrix22_outer()
        else:
            print("Невірний номер. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
