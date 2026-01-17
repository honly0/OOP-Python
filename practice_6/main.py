import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfile, asksaveasfile

import cv2
import numpy as np


class ImageLab6(tk.Frame):
    """
    Практична робота №6.
    GUI для завантаження, обробки, відображення та збереження растрових зображень.
    Використано OpenCV: imread, cvtColor, Canny, threshold, goodFeaturesToTrack, imwrite.
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)

        # State
        self.img_bgr = None       # Original image (BGR)
        self.result_img = None    # Result image (BGR or Gray)

        # Params
        self.canny_t1 = tk.IntVar(value=100)
        self.canny_t2 = tk.IntVar(value=300)

        self.thr_val = tk.IntVar(value=55)

        self.corner_k = tk.IntVar(value=20)
        self.corner_q = tk.DoubleVar(value=0.01)
        self.corner_dist = tk.IntVar(value=10)

        self.info = tk.StringVar(value="Open an image to start.")

        self._build_ui()

    # ---------------- UI ----------------
    def _build_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        controls = tk.LabelFrame(self, text="Controls")
        controls.grid(row=0, column=0, sticky=tk.NSEW, padx=8, pady=8)
        for c in range(8):
            controls.grid_columnconfigure(c, weight=1)

        # Buttons
        tk.Button(controls, text="Open image", command=self.open_image).grid(
            row=0, column=0, sticky=tk.NSEW, padx=4, pady=4
        )
        tk.Button(controls, text="Show original", command=self.show_original).grid(
            row=0, column=1, sticky=tk.NSEW, padx=4, pady=4
        )
        tk.Button(controls, text="Save result", command=self.save_result).grid(
            row=0, column=2, sticky=tk.NSEW, padx=4, pady=4
        )

        tk.Button(controls, text="To Gray", command=self.to_gray).grid(
            row=1, column=0, sticky=tk.NSEW, padx=4, pady=4
        )
        tk.Button(controls, text="Canny edges", command=self.canny_edges).grid(
            row=1, column=1, sticky=tk.NSEW, padx=4, pady=4
        )
        tk.Button(controls, text="Binary threshold", command=self.binary_threshold).grid(
            row=1, column=2, sticky=tk.NSEW, padx=4, pady=4
        )
        tk.Button(controls, text="Corners", command=self.detect_corners).grid(
            row=1, column=3, sticky=tk.NSEW, padx=4, pady=4
        )

        # Params row: Canny
        tk.Label(controls, text="Canny t1").grid(row=2, column=0, sticky=tk.EW)
        tk.Entry(controls, textvariable=self.canny_t1).grid(row=2, column=1, sticky=tk.EW, padx=4)
        tk.Label(controls, text="Canny t2").grid(row=2, column=2, sticky=tk.EW)
        tk.Entry(controls, textvariable=self.canny_t2).grid(row=2, column=3, sticky=tk.EW, padx=4)

        # Params row: Threshold
        tk.Label(controls, text="Threshold").grid(row=3, column=0, sticky=tk.EW)
        tk.Entry(controls, textvariable=self.thr_val).grid(row=3, column=1, sticky=tk.EW, padx=4)

        # Params row: Corners
        tk.Label(controls, text="Corners k").grid(row=4, column=0, sticky=tk.EW)
        tk.Entry(controls, textvariable=self.corner_k).grid(row=4, column=1, sticky=tk.EW, padx=4)

        tk.Label(controls, text="quality").grid(row=4, column=2, sticky=tk.EW)
        tk.Entry(controls, textvariable=self.corner_q).grid(row=4, column=3, sticky=tk.EW, padx=4)

        tk.Label(controls, text="minDist").grid(row=4, column=4, sticky=tk.EW)
        tk.Entry(controls, textvariable=self.corner_dist).grid(row=4, column=5, sticky=tk.EW, padx=4)

        tk.Label(controls, textvariable=self.info).grid(
            row=5, column=0, columnspan=8, sticky=tk.W, padx=4, pady=4
        )

        view = tk.LabelFrame(self, text="View")
        view.grid(row=1, column=0, sticky=tk.NSEW, padx=8, pady=(0, 8))
        view.grid_rowconfigure(0, weight=1)
        view.grid_columnconfigure(0, weight=1)

        hint = (
            "OpenCV shows images in separate windows.\n"
            "Close the image window (or press any key in it) to continue.\n"
            "Use 'Save result' after applying any processing step."
        )
        tk.Label(view, text=hint, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.NW, padx=8, pady=8)

    # ---------------- Helpers ----------------
    def _require_image(self) -> bool:
        if self.img_bgr is None:
            messagebox.showwarning("Warning", "No image loaded. Click 'Open image' first.")
            return False
        return True

    @staticmethod
    def _show_cv(title: str, img):
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyWindow(title)

    def _set_result(self, img, msg: str):
        self.result_img = img
        self.info.set(msg)

    # ---------------- Actions ----------------
    def open_image(self):
        f = askopenfile(
            mode="rb",
            defaultextension=".jpg",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("All files", "*.*")),
        )
        if f is None:
            return
        path = f.name
        f.close()

        img = cv2.imread(path)  # BGR
        if img is None:
            messagebox.showerror("Error", "OpenCV cannot read this file as an image.")
            return

        self.img_bgr = img
        self.result_img = None

        h, w = img.shape[:2]
        self.info.set(f"Loaded: {path} ({w}x{h})")
        self._show_cv("Original (BGR)", self.img_bgr)

    def show_original(self):
        if not self._require_image():
            return
        self._show_cv("Original (BGR)", self.img_bgr)

    def to_gray(self):
        if not self._require_image():
            return
        gray = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2GRAY)
        self._set_result(gray, "Result: Grayscale")
        self._show_cv("Gray", gray)

    def canny_edges(self):
        if not self._require_image():
            return
        try:
            t1 = int(self.canny_t1.get())
            t2 = int(self.canny_t2.get())
        except Exception:
            messagebox.showerror("Data ERROR", "Canny thresholds must be integers.")
            return

        edges = cv2.Canny(self.img_bgr, t1, t2)
        self._set_result(edges, f"Result: Canny edges (t1={t1}, t2={t2})")
        self._show_cv("Edges (Canny)", edges)

    def binary_threshold(self):
        if not self._require_image():
            return
        try:
            thr = int(self.thr_val.get())
        except Exception:
            messagebox.showerror("Data ERROR", "Threshold must be an integer.")
            return

        gray = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(gray, thr, 255, cv2.THRESH_BINARY)
        self._set_result(bw, f"Result: Binary threshold (thr={thr})")
        self._show_cv("Binary", bw)

    def detect_corners(self):
        if not self._require_image():
            return

        try:
            k = int(self.corner_k.get())
            q = float(self.corner_q.get())
            dist = int(self.corner_dist.get())
        except Exception:
            messagebox.showerror("Data ERROR", "Corners params wrong (k=int, quality=float, minDist=int).")
            return

        gray = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, maxCorners=k, qualityLevel=q, minDistance=dist)

        if corners is None:
            messagebox.showinfo("Info", "No corners found with current parameters.")
            return

        corners = np.int32(corners)
        img2 = self.img_bgr.copy()

        for c in corners:
            x, y = c[0]
            cv2.circle(img2, (int(x), int(y)), 5, (0, 0, 255), -1)

        self._set_result(img2, f"Result: Corners (k={k}, q={q}, dist={dist})")
        self._show_cv("Corners", img2)

    def save_result(self):
        if self.result_img is None:
            messagebox.showwarning("Warning", "No result to save. Apply some processing first.")
            return

        f = asksaveasfile(
            mode="wb",
            defaultextension=".jpg",
            filetypes=(
                ("JPEG", "*.jpg"),
                ("PNG", "*.png"),
                ("BMP", "*.bmp"),
                ("All files", "*.*"),
            ),
        )
        if f is None:
            return

        path = f.name
        f.close()

        ok = cv2.imwrite(path, self.result_img)
        if not ok:
            messagebox.showerror("Error", "Failed to save image.")
            return

        self.info.set(f"Saved result: {path}")
        messagebox.showinfo("OK", "Saved successfully.")


def main():
    app = tk.Tk()
    app.title("lab6-v22-ImageApp")
    app.minsize(700, 350)
    ImageLab6(app)
    app.mainloop()


if __name__ == "__main__":
    main()
