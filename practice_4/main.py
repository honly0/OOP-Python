import math
import matplotlib.pyplot as plt


class Point_22:
    """
    Point_22: точка на площині.
    - приховані координати __x, __y
    - геттери/сеттери з перевіркою [-100, 100] (інакше 0)
    - лічильник екземплярів (змінна класу)
    - метод класу для отримання кількості екземплярів
    - конструктор (2 параметри за замовчуванням)
    - деструктор з повідомленням
    - метод shift(dx, dy): зсув точки
    """
    __count = 0

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.__x = 0.0
        self.__y = 0.0
        self.x = x  # через сеттер
        self.y = y  # через сеттер
        Point_22.__count += 1

    def __del__(self):
        Point_22.__count -= 1
        print("Point_22 object destroyed!")

    @classmethod
    def get_count(cls) -> int:
        return cls.__count

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, val: float):
        try:
            val = float(val)
        except ValueError:
            val = 0.0
        self.__x = val if -100 <= val <= 100 else 0.0

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, val: float):
        try:
            val = float(val)
        except ValueError:
            val = 0.0
        self.__y = val if -100 <= val <= 100 else 0.0

    def shift(self, dx: float, dy: float):
        """Зсув точки: dx по x, dy по y."""
        self.x = self.x + dx
        self.y = self.y + dy

    def distance_to(self, other: "Point_22") -> float:
        """Відстань між двома точками."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self) -> str:
        return f"Point_22(x={self.x}, y={self.y})"


def read_point(i: int) -> Point_22:
    """Зчитування точки з перевіркою."""
    while True:
        raw = input(f"Введіть координати точки #{i} (x y): ").strip().replace(",", ".")
        parts = raw.split()
        if len(parts) != 2:
            print("Помилка: введіть 2 числа через пробіл.")
            continue
        try:
            x = float(parts[0])
            y = float(parts[1])
            return Point_22(x, y)
        except ValueError:
            print("Помилка: некоректні числа. Спробуйте ще раз.")


def plot_points(before, after):
    """Візуалізація точок до і після змін (matplotlib)."""
    bx = [p.x for p in before]
    by = [p.y for p in before]
    ax = [p.x for p in after]
    ay = [p.y for p in after]

    plt.figure()
    plt.title("Practice 4 (variant 22): Points before/after")
    plt.grid(True)

    # до
    plt.scatter(bx, by, marker="o", label="Before")
    for idx, p in enumerate(before, start=1):
        plt.text(p.x, p.y, f" {idx}", fontsize=9)

    # після
    plt.scatter(ax, ay, marker="x", label="After")
    for idx, p in enumerate(after, start=1):
        plt.text(p.x, p.y, f" {idx}", fontsize=9)

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()


def save_points_to_file(points, filename: str):
    """
    Зберігає координати точок у файл.
    Для парних варіантів формат: (номер) координата_х: координата_у
    """
    with open(filename, "w", encoding="utf-8") as f:
        for i, p in enumerate(points, start=1):
            f.write(f"({i}) {p.x}: {p.y}\n")


def main():
    print("Практична робота №4 | Варіант 22")
    print("Введіть 4 точки (координати в межах [-100, 100], інакше буде 0).")

    # 1) створити список з 4 точок
    points = [read_point(i) for i in range(1, 5)]
    print("\nСтворені точки:", points)
    print("Кількість екземплярів Point_22:", Point_22.get_count())

    # збережемо стан ДО
    before = [Point_22(p.x, p.y) for p in points]

    # 2) відстань між 1 і 4
    dist_1_4 = points[0].distance_to(points[3])
    print(f"\nВідстань між точкою 1 і 4: {dist_1_4}")

    # 3) пересунути 3-тю точку на 17 вниз і 24 вліво
    # вниз = -17 по y, вліво = -24 по x
    points[2].shift(-24, -17)
    print("\nПісля зміщення 3-ї точки (-24 по x, -17 по y):", points)

    # збережемо стан ПІСЛЯ
    after = [Point_22(p.x, p.y) for p in points]

    # 4) візуалізація до/після
    plot_points(before, after)

    # 5) запис у файл (парний варіант)
    out_file = "points_22.txt"
    save_points_to_file(points, out_file)
    print(f"\nКоординати збережено у файл: {out_file}")


if __name__ == "__main__":
    main()
