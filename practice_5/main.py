import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile, asksaveasfile

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Lab5Window(tk.Frame):
    """
    Практична робота №5, варіант 22.
    GUI + 2 задачі:
    1) Func9: Even(K) і підрахунок парних у наборі з 10 цілих чисел.
    2) Побудова графіка за рекурентним виразом №1, робота з файлом, min/max, plot.
    """

    # ---------- Task 1 (Func9) ----------
    @staticmethod
    def even(k: int) -> bool:
        """Func9. Повертає True, якщо K парне; False інакше."""
        return k % 2 == 0

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.parent = parent

        # ---- Tk variables (Task 2 defaults for variant 1) ----
        # За методичкою: T = 0.3, K = 2.5, U[0] = 2, y[0] = 0
        self.group_var = tk.StringVar(value="320")          # можеш змінити
        self.surname_var = tk.StringVar(value="Pryanytskyi") # можеш змінити
        self.name_var = tk.StringVar(value="Oleksii")        # можеш змінити
        self.variant_var = tk.StringVar(value="22")

        self.n_var = tk.IntVar(value=200)       # N: 20..1000 (чим більше — тим гладкіше)
        self.T_var = tk.DoubleVar(value=0.3)
        self.K_var = tk.DoubleVar(value=2.5)
        self.U_var = tk.DoubleVar(value=2.0)
        self.y0_var = tk.DoubleVar(value=0.0)

        # ---- State ----
        self.file_lines = []      # зчитаний текст з файлу
        self.x = []               # t
        self.y = []               # y(t)
        self.canvas = None        # FigureCanvasTkAgg

        # ---- Layout root frame ----
        self.pack(fill=tk.BOTH, expand=True)
        self._build_gui()

        # Set initial window title
        self._update_title()

    # ---------------- GUI building ----------------
    def _build_gui(self):
        # Make grid responsive
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top = tk.LabelFrame(self, text="Header (for window title)")
        top.grid(row=0, column=0, sticky=tk.NSEW, padx=8, pady=8)
        top.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        tk.Label(top, text="Group:").grid(row=0, column=0, sticky=tk.EW, padx=4, pady=4)
        tk.Entry(top, textvariable=self.group_var).grid(row=0, column=1, sticky=tk.EW, padx=4, pady=4)

        tk.Label(top, text="Variant:").grid(row=0, column=2, sticky=tk.EW, padx=4, pady=4)
        tk.Entry(top, textvariable=self.variant_var).grid(row=0, column=3, sticky=tk.EW, padx=4, pady=4)

        tk.Label(top, text="Surname:").grid(row=1, column=0, sticky=tk.EW, padx=4, pady=4)
        tk.Entry(top, textvariable=self.surname_var).grid(row=1, column=1, sticky=tk.EW, padx=4, pady=4)

        tk.Label(top, text="Name:").grid(row=1, column=2, sticky=tk.EW, padx=4, pady=4)
        tk.Entry(top, textvariable=self.name_var).grid(row=1, column=3, sticky=tk.EW, padx=4, pady=4)

        tk.Button(top, text="Apply title", command=self._update_title).grid(
            row=0, column=4, rowspan=2, sticky=tk.NSEW, padx=4, pady=4
        )

        # ---------- Middle: two tasks controls ----------
        mid = tk.Frame(self)
        mid.grid(row=1, column=0, sticky=tk.NSEW, padx=8, pady=(0, 8))
        mid.grid_columnconfigure((0, 1), weight=1)
        mid.grid_rowconfigure(0, weight=1)

        # Task 1 frame
        task1 = tk.LabelFrame(mid, text="Task 1 (Func9): count even among 10 integers")
        task1.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 6))
        task1.grid_columnconfigure(0, weight=1)

        tk.Label(task1, text="Enter 10 integers (space-separated):").grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)
        self.integers_entry = tk.Entry(task1)
        self.integers_entry.grid(row=1, column=0, sticky=tk.EW, padx=6, pady=4)
        self.integers_entry.insert(0, "1 2 3 4 5 6 7 8 9 10")

        tk.Button(task1, text="Count even", command=self.count_even).grid(row=2, column=0, sticky=tk.EW, padx=6, pady=4)
        self.task1_out = tk.StringVar(value="Even count: -")
        tk.Label(task1, textvariable=self.task1_out).grid(row=3, column=0, sticky=tk.W, padx=6, pady=(0, 6))

        # Task 2 frame
        task2 = tk.LabelFrame(mid, text="Task 2: recurrence + file + min/max + plot (variant 1)")
        task2.grid(row=0, column=1, sticky=tk.NSEW, padx=(6, 0))
        task2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        tk.Label(task2, text="N (20..1000):").grid(row=0, column=0, sticky=tk.EW, padx=6, pady=4)
        tk.Entry(task2, textvariable=self.n_var).grid(row=0, column=1, sticky=tk.EW, padx=6, pady=4)

        tk.Label(task2, text="T:").grid(row=0, column=2, sticky=tk.EW, padx=6, pady=4)
        tk.Entry(task2, textvariable=self.T_var).grid(row=0, column=3, sticky=tk.EW, padx=6, pady=4)

        tk.Label(task2, text="K:").grid(row=1, column=0, sticky=tk.EW, padx=6, pady=4)
        tk.Entry(task2, textvariable=self.K_var).grid(row=1, column=1, sticky=tk.EW, padx=6, pady=4)

        tk.Label(task2, text="U[0]:").grid(row=1, column=2, sticky=tk.EW, padx=6, pady=4)
        tk.Entry(task2, textvariable=self.U_var).grid(row=1, column=3, sticky=tk.EW, padx=6, pady=4)

        tk.Label(task2, text="y[0]:").grid(row=2, column=0, sticky=tk.EW, padx=6, pady=4)
        tk.Entry(task2, textvariable=self.y0_var).grid(row=2, column=1, sticky=tk.EW, padx=6, pady=4)

        # Buttons row
        tk.Button(task2, text="Create file (t;y)", command=self.create_file).grid(row=3, column=0, sticky=tk.NSEW, padx=6, pady=6)
        tk.Button(task2, text="Open file", command=self.open_file).grid(row=3, column=1, sticky=tk.NSEW, padx=6, pady=6)
        tk.Button(task2, text="Show min/max", command=self.show_minmax).grid(row=3, column=2, sticky=tk.NSEW, padx=6, pady=6)
        tk.Button(task2, text="Show plot", command=self.show_plot).grid(row=3, column=3, sticky=tk.NSEW, padx=6, pady=6)

        # Output label
        self.task2_out = tk.StringVar(value="File: not loaded")
        tk.Label(task2, textvariable=self.task2_out).grid(row=4, column=0, columnspan=4, sticky=tk.W, padx=6, pady=(0, 6))

        # ---------- Bottom: plot area ----------
        bottom = tk.LabelFrame(self, text="Plot area")
        bottom.grid(row=2, column=0, sticky=tk.NSEW, padx=8, pady=(0, 8))
        bottom.grid_rowconfigure(0, weight=1)
        bottom.grid_columnconfigure(0, weight=1)
        self.plot_container = bottom

    # ---------------- Header title ----------------
    def _update_title(self):
        # Title format requirement: lab# - <group> -v <variant> - <surname> - <name>
        # Example in methodichka: lab4_2-320-v01-Ivanov-Ivan
        group = self.group_var.get().strip() or "???"
        var = self.variant_var.get().strip() or "??"
        surname = self.surname_var.get().strip() or "Surname"
        name = self.name_var.get().strip() or "Name"

        self.parent.title(f"lab5-{group}-v{var}-{surname}-{name}")

    # ---------------- Task 1 logic ----------------
    def count_even(self):
        raw = self.integers_entry.get().strip()
        if not raw:
            messagebox.showerror("Data ERROR", "Please enter 10 integers.")
            return

        parts = raw.split()
        if len(parts) != 10:
            messagebox.showerror("Data ERROR", "You must enter exactly 10 integers (space-separated).")
            return

        try:
            nums = [int(p) for p in parts]
        except ValueError:
            messagebox.showerror("Data ERROR", "All values must be integers.")
            return

        cnt = sum(1 for v in nums if self.even(v))
        self.task1_out.set(f"Even count: {cnt}")

    # ---------------- Task 2 calculation ----------------
    def calculate_arrays(self):
        """
        Variant 1 recurrence:
        y[k+1] = (1 - T0/T) * y[k] + (T0/T) * K * U
        where T0 = 2T / N, t[k] = k*T0
        """
        try:
            N = int(self.n_var.get())
            T = float(self.T_var.get())
            K = float(self.K_var.get())
            U = float(self.U_var.get())
            y0 = float(self.y0_var.get())
        except Exception:
            raise ValueError("Wrong numeric parameters.")

        if N < 20 or N > 1000:
            raise ValueError("N must be in range [20..1000].")
        if T == 0:
            raise ValueError("T must not be 0.")

        T0 = (2.0 * T) / N

        x = [0.0] * (N + 1)
        y = [0.0] * (N + 1)
        y[0] = y0

        for k in range(N):
            x[k] = k * T0
            y[k + 1] = (1.0 - T0 / T) * y[k] + (T0 / T) * K * U
        x[N] = N * T0

        return x, y, T0

    # ---------------- File operations ----------------
    def create_file(self):
        """
        Create text file with 2 columns: t;y
        For even variants delimiter must be ';'
        """
        try:
            x, y, T0 = self.calculate_arrays()
        except Exception as e:
            messagebox.showerror("Data ERROR", str(e))
            return

        f = asksaveasfile(
            mode="w",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        if f is None:
            return

        # Write data
        # Format: t;y (delimiter ';' for even variants)
        for i in range(len(x)):
            f.write(f"{x[i]};{y[i]}\n")
        f.close()

        self.task2_out.set("File created successfully (delimiter ';').")
        messagebox.showinfo("OK", "File created.\nDelimiter for even variants: ';'")

    def open_file(self):
        f = askopenfile(
            mode="r",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        if f is None:
            return

        try:
            self.file_lines = f.readlines()
        finally:
            f.close()

        try:
            self._parse_loaded_lines()
        except Exception as e:
            self.file_lines = []
            self.x, self.y = [], []
            messagebox.showerror("Data ERROR", f"Wrong file format!\n{e}")
            self.task2_out.set("File: load error")
            return

        self.task2_out.set(f"File loaded. Points: {len(self.x)}")

    def _parse_loaded_lines(self):
        """
        Parse file lines expecting: t;y
        """
        x = []
        y = []
        for line in self.file_lines:
            line = line.strip()
            if not line:
                continue
            # Even variant: delimiter ';'
            parts = line.split(";")
            if len(parts) != 2:
                raise ValueError("Each line must have exactly 2 values separated by ';'")
            x.append(float(parts[0].replace(",", ".")))
            y.append(float(parts[1].replace(",", ".")))

        if not x:
            raise ValueError("No data found in file.")
        self.x, self.y = x, y

    # ---------------- Min/Max ----------------
    def show_minmax(self):
        if not self.x or not self.y:
            messagebox.showwarning("Warning", "No data loaded. Use 'Open file' or 'Create file' first.")
            return

        xmin = min(self.x)
        xmax = max(self.x)
        ymin = min(self.y)
        ymax = max(self.y)

        msg = (
            f"Argument t:\n"
            f"  min = {xmin}\n"
            f"  max = {xmax}\n\n"
            f"Function y(t):\n"
            f"  min = {ymin}\n"
            f"  max = {ymax}\n"
        )
        messagebox.showinfo("Min/Max", msg)

    # ---------------- Plotting ----------------
    def show_plot(self):
        # If no file loaded, compute on the fly and plot (still OK)
        if not self.x or not self.y:
            try:
                self.x, self.y, _ = self.calculate_arrays()
                self.task2_out.set("Plot from calculated data (file not loaded).")
            except Exception as e:
                messagebox.showerror("Data ERROR", str(e))
                return

        # Destroy old canvas widget if exists
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Title and labels (physical sense for variant 1: temperature)
        ax.set_title("y[k+1] = (1 - T0/T)*y[k] + (T0/T)*K*U  (Variant 1)")
        ax.set_xlabel("t (time), s")
        ax.set_ylabel("y (Temperature), K")

        ax.plot(self.x, self.y)
        ax.grid(True)

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.NSEW)
        self.canvas.draw()


def main():
    app = tk.Tk()
    window = Lab5Window(app)
    app.minsize(900, 600)
    app.mainloop()


if __name__ == "__main__":
    main()
