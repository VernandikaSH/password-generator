import tkinter as tk
from tkinter import messagebox
import secrets
import string

# ---------- Palet warna monokrom klasik ----------
BG = "#f4f4f2"          # background utama (putih gading)
FG = "#1a1a1a"          # teks utama (hitam)
ACCENT = "#1a1a1a"      # aksen tombol/handle (hitam)
BORDER = "#1a1a1a"      # garis border
GRAY_LIGHT = "#d9d9d6"  # track slider
GRAY_MID = "#8c8c88"    # teks sekunder
WHITE = "#ffffff"
FONT_SERIF = "Georgia"


class RoundSlider(tk.Canvas):
    """Slider horizontal custom dengan handle berbentuk bulat (lingkaran)."""

    def __init__(self, parent, from_=4, to=64, value=12, width=340, height=40,
                 on_change=None, **kwargs):
        super().__init__(parent, width=width, height=height, bg=BG,
                          highlightthickness=0, **kwargs)
        self.from_ = from_
        self.to = to
        self.width = width
        self.height = height
        self.radius = 9            # radius handle bulat
        self.track_pad = 14        # jarak tepi kiri/kanan untuk track
        self.value = value
        self.on_change = on_change

        self.bind("<Button-1>", self._on_click_or_drag)
        self.bind("<B1-Motion>", self._on_click_or_drag)

        self._draw()

    def _value_to_x(self, value):
        usable_w = self.width - 2 * self.track_pad
        ratio = (value - self.from_) / (self.to - self.from_)
        return self.track_pad + ratio * usable_w

    def _x_to_value(self, x):
        usable_w = self.width - 2 * self.track_pad
        x = max(self.track_pad, min(self.width - self.track_pad, x))
        ratio = (x - self.track_pad) / usable_w
        raw = self.from_ + ratio * (self.to - self.from_)
        return int(round(raw))

    def _draw(self):
        self.delete("all")
        cy = self.height / 2
        x_handle = self._value_to_x(self.value)

        # track belakang (abu-abu)
        self.create_line(self.track_pad, cy, self.width - self.track_pad, cy,
                          fill=GRAY_LIGHT, width=4, capstyle="round")
        # track terisi (hitam) dari kiri sampai handle
        self.create_line(self.track_pad, cy, x_handle, cy,
                          fill=ACCENT, width=4, capstyle="round")
        # handle bulat
        r = self.radius
        self.create_oval(x_handle - r, cy - r, x_handle + r, cy + r,
                          fill=WHITE, outline=ACCENT, width=2)

    def _on_click_or_drag(self, event):
        new_value = self._x_to_value(event.x)
        if new_value != self.value:
            self.value = new_value
            self._draw()
            if self.on_change:
                self.on_change(self.value)

    def get(self):
        return self.value

    def set(self, value):
        self.value = int(round(value))
        self._draw()


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("420x460")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 24, "pady": 8}

        title = tk.Label(
            self.root, text="PASSWORD GENERATOR",
            font=(FONT_SERIF, 16, "bold"), bg=BG, fg=FG
        )
        title.pack(pady=(24, 2))

        subtitle = tk.Label(
            self.root, text="Simple. Secure. Offline.",
            font=(FONT_SERIF, 9, "italic"), bg=BG, fg=GRAY_MID
        )
        subtitle.pack(pady=(0, 16))

        # garis pemisah tipis
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x", padx=24)

        # --- Panjang password ---
        length_frame = tk.Frame(self.root, bg=BG)
        length_frame.pack(fill="x", padx=24, pady=(16, 0))

        tk.Label(length_frame, text="PANJANG PASSWORD", bg=BG, fg=FG,
                 font=(FONT_SERIF, 10, "bold")).pack(side="left")

        self.length_label = tk.Label(length_frame, text="12", bg=BG, fg=FG,
                                      font=(FONT_SERIF, 10, "bold"))
        self.length_label.pack(side="right")

        self.length_slider = RoundSlider(
            self.root, from_=4, to=64, value=12, width=372, height=36,
            on_change=self._on_length_change
        )
        self.length_slider.pack(padx=24, pady=(4, 4))

        # --- Checkbox opsi karakter ---
        options_frame = tk.LabelFrame(
            self.root, text=" JENIS KARAKTER ", bg=BG, fg=FG,
            font=(FONT_SERIF, 9, "bold"), bd=1, relief="solid",
            labelanchor="n"
        )
        options_frame.pack(fill="x", **pad)

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)

        chk_opts = dict(bg=BG, fg=FG, activebackground=BG, anchor="w",
                         font=(FONT_SERIF, 10), selectcolor=WHITE,
                         highlightthickness=0)

        tk.Checkbutton(options_frame, text="Huruf Besar (A-Z)",
                        variable=self.use_upper, **chk_opts).pack(fill="x", padx=14, pady=3)
        tk.Checkbutton(options_frame, text="Huruf Kecil (a-z)",
                        variable=self.use_lower, **chk_opts).pack(fill="x", padx=14, pady=3)
        tk.Checkbutton(options_frame, text="Angka (0-9)",
                        variable=self.use_digits, **chk_opts).pack(fill="x", padx=14, pady=3)
        tk.Checkbutton(options_frame, text="Simbol (!@#$%...)",
                        variable=self.use_symbols, **chk_opts).pack(fill="x", padx=14, pady=3)

        # --- Hasil password ---
        result_frame = tk.Frame(self.root, bg=BG)
        result_frame.pack(fill="x", **pad)

        self.result_var = tk.StringVar(value="")
        self.result_entry = tk.Entry(
            result_frame, textvariable=self.result_var,
            font=("Consolas", 12), justify="center", state="readonly",
            readonlybackground=WHITE, fg=FG,
            relief="solid", bd=1, highlightbackground=BORDER
        )
        self.result_entry.pack(fill="x", ipady=8)

        # --- Tombol ---
        button_frame = tk.Frame(self.root, bg=BG)
        button_frame.pack(fill="x", padx=24, pady=(12, 24))

        generate_btn = tk.Button(
            button_frame, text="GENERATE", command=self.generate_password,
            bg=FG, fg=WHITE, font=(FONT_SERIF, 10, "bold"),
            relief="flat", padx=10, pady=9, cursor="hand2",
            activebackground="#333333", activeforeground=WHITE
        )
        generate_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))

        copy_btn = tk.Button(
            button_frame, text="COPY", command=self.copy_to_clipboard,
            bg=WHITE, fg=FG, font=(FONT_SERIF, 10, "bold"),
            relief="solid", bd=1, padx=10, pady=8, cursor="hand2",
            activebackground=GRAY_LIGHT
        )
        copy_btn.pack(side="left", expand=True, fill="x", padx=(6, 0))

        # Generate satu password langsung saat aplikasi dibuka
        self.generate_password()

    def _on_length_change(self, value):
        self.length_label.config(text=str(value))

    def generate_password(self):
        pool = ""
        if self.use_upper.get():
            pool += string.ascii_uppercase
        if self.use_lower.get():
            pool += string.ascii_lowercase
        if self.use_digits.get():
            pool += string.digits
        if self.use_symbols.get():
            pool += "!@#$%^&*()-_=+[]{}"

        if not pool:
            messagebox.showwarning(
                "Tidak Ada Jenis Karakter",
                "Pilih minimal satu jenis karakter (huruf/angka/simbol) terlebih dahulu."
            )
            return

        length = self.length_slider.get()
        password = "".join(secrets.choice(pool) for _ in range(length))
        self.result_var.set(password)

    def copy_to_clipboard(self):
        password = self.result_var.get()
        if not password:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()
        messagebox.showinfo("Tersalin", "Password berhasil disalin ke clipboard.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()