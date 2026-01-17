"""
Практична робота №3
Варіант 22: Proc14 + Matrix22
"""

from __future__ import annotations
from typing import List, Tuple, Iterable
import numpy as np


# ---------------------------
# Task 1 (Proc14): ShiftRight3
# ---------------------------

def shift_right3(a: float, b: float, c: float) -> Tuple[float, float, float]:
    """
    Proc14. Правий циклічний зсув:
    значення A переходить в B, B -> C, C -> A.
    Повертає (newA, newB, newC).
    """
    return c, a, b


def shift_right3_for_two_sets(pairs: Iterable[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
    """
    Друга частина задачі (виклик функції для наборів):
    На вході список/ітератор трійок (A,B,C),
    на виході список результатів після ShiftRight3.
    """
    res: List[Tuple[float, float, float]] = []
    for (a, b, c) in pairs:
        res.append(shift_right3(a, b, c))
    return res


def task_proc14_io() -> bool:
    """
    Третя функція без параметрів:
    введення даних, виклик, виведення результатів для двох наборів (A1,B1,C1) і (A2,B2,C2).
    """
    try:
        print("Proc14 (ShiftRight3): введіть два набори по 3 числа (A B C).")

        a1, b1, c1 = map(float, input("Набір 1 (A1 B1 C1): ").split())
        a2, b2, c2 = map(float, input("Набір 2 (A2 B2 C2): ").split())

        out = shift_right3_for_two_sets([(a1, b1, c1), (a2, b2, c2)])

        print("\nРезультати правого циклічного зсуву:")
        print(f"Набір 1 -> A={out[0][0]}, B={out[0][1]}, C={out[0][2]}")
        print(f"Набір 2 -> A={out[1][0]}, B={out[1][1]}, C={out[1][2]}")
        return True

    except ValueError:
        print("Помилка: введіть рівно 3 числа через пробіл для кожного набору.")
        return False


# ---------------------------
# Task 2 (Matrix22): nested functions + numpy
# ---------------------------

def _read_int_matrix_from_file(filename: str) -> np.ndarray:
    """
    Читає цілочисельну матрицю з текстового файлу.
    Формат: кожен рядок = рядок матриці, числа розділені пробілами.
    """
    try:
        rows: List[List[int]] = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rows.append([int(x) for x in line.split()])

        if not rows:
            raise ValueError("Файл порожній або не містить чисел.")

        # Перевірка прямокутності
        n_cols = len(rows[0])
        if any(len(r) != n_cols for r in rows):
            raise ValueError("Матриця у файлі не прямокутна (різна кількість елементів у рядках).")

        return np.array(rows, dtype=int)

    except FileNotFoundError:
        raise FileNotFoundError("Файл не знайдено.")
    except ValueError as e:
        raise ValueError(f"Некоректні дані у файлі: {e}")


def matrix22_outer() -> bool:
    """
    Зовнішня функція без параметрів (за методичкою).
    Вона містить вкладену функцію, яка приймає ім'я файлу.
    """
    def matrix22_inner(filename: str) -> Tuple[List[Tuple[int, int]], np.ndarray, Tuple[int, int]]:
        """
        Внутрішня функція:
        Вхід: filename
        Вихід:
          - список (argmax_idx, argmin_idx) для кожного рядка (1-based індекси)
          - перетворена матриця після перестановки стовпців
          - (col_of_global_max, col_of_global_min) (1-based)
        """
        A = _read_int_matrix_from_file(filename)  # shape (M,N)

        # 1) Для кожного рядка: індекси max/min (1-based)
        row_max_idx = np.argmax(A, axis=1) + 1
        row_min_idx = np.argmin(A, axis=1) + 1
        row_indices = list(zip(row_max_idx.tolist(), row_min_idx.tolist()))

        # 2) Знайти стовпець глобального max і глобального min, потім поміняти їх місцями
        flat_argmax = int(np.argmax(A))
        flat_argmin = int(np.argmin(A))
        max_pos = np.unravel_index(flat_argmax, A.shape)  # (row, col)
        min_pos = np.unravel_index(flat_argmin, A.shape)

        col_max = int(max_pos[1])  # 0-based
        col_min = int(min_pos[1])  # 0-based

        B = A.copy()
        if col_max != col_min:
            B[:, [col_max, col_min]] = B[:, [col_min, col_max]]

        return row_indices, B, (col_max + 1, col_min + 1)

    try:
        filename = input("Введіть ім'я файлу з матрицею (наприклад matrix.txt): ").strip()
        row_indices, new_matrix, (col_max, col_min) = matrix22_inner(filename)

        print("\nMatrix22: індекси елементів у кожному рядку (1-based):")
        for i, (imax, imin) in enumerate(row_indices, start=1):
            print(f"Рядок {i}: max -> {imax}, min -> {imin}")

        print(f"\nСтовпець з глобальним MAX: {col_max}")
        print(f"Стовпець з глобальним MIN: {col_min}")
        print("\nМатриця після перестановки цих стовпців:")
        print(new_matrix)

        return True

    except Exception as e:
        print(f"Помилка: {e}")
        return False
