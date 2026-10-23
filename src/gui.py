import math
import tkinter as tk
from tkinter import messagebox, ttk

from src import formulas


WSKAZNIKI = (
    ("F(t)", "Funkcja zawodności"),
    ("R(t)", "Funkcja niezawodności"),
    ("f(t)", "Gęstość prawdopodobieństwa"),
    ("λ(t)", "Intensywność uszkodzeń"),
    ("ET", "Średni czas poprawnej pracy"),
    ("σ²", "Wariancja czasu poprawnej pracy"),
)

TLO = "#F5F5F5"
BIALY = "#FFFFFF"
TEKST = "#292929"
DRUGORZEDNY = "#6C6C6C"
RAMKA = "#DDDDDD"
PRZYCISK = "#424242"


class AplikacjaNSK:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Wskaźniki niezawodności")
        self.root.geometry("1020x690")
        self.root.minsize(900, 650)
        self.root.configure(bg=TLO)

        self.czas_var = tk.StringVar()
        self.lambda_var = tk.StringVar()
        self.r_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Wprowadź parametry, aby wyznaczyć wskaźniki.")

        self.wyniki_wykladniczy = {symbol: tk.StringVar(value="—") for symbol, _ in WSKAZNIKI}
        self.wyniki_erlang = {symbol: tk.StringVar(value="—") for symbol, _ in WSKAZNIKI}

        self._ustaw_styl()
        self._zbuduj_okno()

    def _ustaw_styl(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=TLO)
        style.configure("TLabel", background=TLO, foreground=TEKST, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 17, "bold"), foreground=TEKST)
        style.configure("Section.TLabel", background=BIALY, foreground=TEKST, font=("Segoe UI", 11, "bold"))
        style.configure("Panel.TFrame", background=BIALY, borderwidth=1, relief="solid")
        style.configure("Inside.TFrame", background=BIALY)
        style.configure("Panel.TLabel", background=BIALY, foreground=TEKST)
        style.configure("Muted.TLabel", background=BIALY, foreground=DRUGORZEDNY, font=("Segoe UI", 9))
        style.configure("Value.TLabel", background=BIALY, foreground=TEKST, font=("Segoe UI", 10, "bold"))
        style.configure("Status.TLabel", background=TLO, foreground=DRUGORZEDNY, font=("Segoe UI", 9))
        style.configure("TEntry", padding=6, fieldbackground=BIALY, bordercolor=RAMKA, lightcolor=RAMKA, darkcolor=RAMKA)

        style.configure(
            "Main.TButton", font=("Segoe UI", 10), padding=(15, 8),
            background=PRZYCISK, foreground=BIALY, borderwidth=1, relief="flat",
        )
        style.map(
            "Main.TButton",
            background=[("pressed", "#303030"), ("active", "#565656")],
            foreground=[("disabled", "#AAAAAA"), ("active", BIALY)],
        )
        style.configure(
            "Clear.TButton", font=("Segoe UI", 10), padding=(15, 8),
            background="#EBEBEB", foreground=TEKST, borderwidth=1, relief="flat",
        )
        style.map("Clear.TButton", background=[("pressed", "#D4D4D4"), ("active", "#E0E0E0")])

    def _zbuduj_okno(self) -> None:
        container = ttk.Frame(self.root, padding=(24, 22))
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=1)

        ttk.Label(
            container, text="Wskaźniki niezawodności obiektów nienaprawialnych",
            style="Title.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        self._zbuduj_pola_wejsciowe(container)
        self._zbuduj_wyniki(container)
        ttk.Label(container, textvariable=self.status_var, style="Status.TLabel").grid(
            row=3, column=0, sticky="w", pady=(12, 0)
        )

    def _zbuduj_pola_wejsciowe(self, parent: ttk.Frame) -> None:
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=(20, 17))
        panel.grid(row=1, column=0, sticky="ew", pady=(0, 16))
        for kolumna in range(3):
            panel.columnconfigure(kolumna, weight=1)

        ttk.Label(panel, text="Dane wejściowe", style="Section.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 14)
        )

        dane_pol = (
            (0, "Czas t [h]", "np. 1000", self.czas_var),
            (1, "Parametr λ [1/h]", "np. 1e-3 lub 0,001", self.lambda_var),
            (2, "Rząd Erlanga r [–]", "np. 3", self.r_var),
        )
        self.pola = []
        for kolumna, opis, podpowiedz, zmienna in dane_pol:
            grupa = ttk.Frame(panel, style="Inside.TFrame")
            grupa.grid(row=1, column=kolumna, sticky="ew", padx=(0, 16) if kolumna < 2 else 0)
            ttk.Label(grupa, text=opis, style="Panel.TLabel").pack(anchor="w", pady=(0, 6))
            pole = ttk.Entry(grupa, textvariable=zmienna, font=("Segoe UI", 10))
            pole.pack(fill="x")
            ttk.Label(grupa, text=podpowiedz, style="Muted.TLabel").pack(anchor="w", pady=(5, 0))
            self.pola.append(pole)

        ttk.Label(
            panel, text="Wymagania: t ≥ 0, λ > 0, r = 2, 3, 4...  ·  Te same t i λ dla obu rozkładów.",
            style="Muted.TLabel",
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(15, 13))

        buttons = ttk.Frame(panel, style="Inside.TFrame")
        buttons.grid(row=3, column=0, columnspan=3, sticky="w")
        ttk.Button(buttons, text="Wyznacz wskaźniki", style="Main.TButton", command=self.oblicz).pack(
            side="left", padx=(0, 9)
        )
        ttk.Button(buttons, text="Wyczyść", style="Clear.TButton", command=self.wyczysc).pack(side="left")

        self.pola[0].focus_set()
        self.root.bind("<Return>", lambda _event: self.oblicz())

    def _zbuduj_wyniki(self, parent: ttk.Frame) -> None:
        area = ttk.Frame(parent)
        area.grid(row=2, column=0, sticky="nsew")
        area.columnconfigure(0, weight=1, uniform="wyniki")
        area.columnconfigure(1, weight=1, uniform="wyniki")
        area.rowconfigure(0, weight=1)

        self._stworz_karte_wynikow(area, 0, "Rozkład wykładniczy", self.wyniki_wykladniczy)
        self._stworz_karte_wynikow(area, 1, "Rozkład Erlanga r-tego rzędu", self.wyniki_erlang)

    def _stworz_karte_wynikow(
        self, parent: ttk.Frame, kolumna: int, tytul: str, wartosci: dict[str, tk.StringVar]
    ) -> None:
        panel = ttk.Frame(parent, style="Panel.TFrame", padding=(18, 17))
        panel.grid(row=0, column=kolumna, sticky="nsew", padx=(0, 8) if kolumna == 0 else (8, 0))
        panel.columnconfigure(1, weight=1)

        ttk.Label(panel, text=tytul, style="Section.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 14)
        )
        for i, (symbol, opis) in enumerate(WSKAZNIKI, start=1):
            ttk.Label(panel, text=f"{symbol}  —  {opis}", style="Panel.TLabel", wraplength=310).grid(
                row=i, column=0, sticky="w", pady=6, padx=(0, 12)
            )
            ttk.Label(panel, textvariable=wartosci[symbol], style="Value.TLabel", wraplength=170).grid(
                row=i, column=1, sticky="e", pady=6
            )

    @staticmethod
    def _czytaj_liczbe(wartosc: str, nazwa: str, *, dodatnia: bool = False) -> float:
        wpis = wartosc.strip().replace(",", ".")
        if not wpis:
            raise ValueError(f"Wprowadź wartość pola „{nazwa}”.")
        try:
            liczba = float(wpis)
        except ValueError as exc:
            raise ValueError(f"Pole „{nazwa}” musi zawierać liczbę.") from exc
        if not math.isfinite(liczba):
            raise ValueError(f"Pole „{nazwa}” musi zawierać skończoną liczbę.")
        if dodatnia and liczba <= 0:
            raise ValueError(f"Pole „{nazwa}” musi być większe od zera.")
        if not dodatnia and liczba < 0:
            raise ValueError(f"Pole „{nazwa}” nie może być ujemne.")
        return liczba

    @staticmethod
    def _czytaj_rzad(wartosc: str) -> int:
        wpis = wartosc.strip()
        if not wpis:
            raise ValueError("Wprowadź rząd rozkładu Erlanga (r).")
        try:
            r = int(wpis)
        except ValueError as exc:
            raise ValueError("Rząd Erlanga r musi być liczbą całkowitą.") from exc
        if r < 2:
            raise ValueError("Rząd Erlanga r musi wynosić co najmniej 2.")
        return r

    def oblicz(self) -> None:
        try:
            t = self._czytaj_liczbe(self.czas_var.get(), "Czas t")
            lambda_ = self._czytaj_liczbe(self.lambda_var.get(), "Parametr λ", dodatnia=True)
            r = self._czytaj_rzad(self.r_var.get())
        except ValueError as exc:
            messagebox.showerror("Nieprawidłowe dane", str(exc), parent=self.root)
            self.status_var.set("Popraw dane wejściowe i spróbuj ponownie.")
            return

        wykladniczy = {
            "F(t)": formulas.wykladniczy_F(t, lambda_),
            "R(t)": formulas.wykladniczy_R(t, lambda_),
            "f(t)": formulas.wykladniczy_f(t, lambda_),
            "λ(t)": formulas.wykladniczy_lambda_t(t, lambda_),
            "ET": formulas.wykladniczy_ET(lambda_),
            "σ²": formulas.wykladniczy_wariancja(lambda_),
        }
        erlang = {
            "F(t)": formulas.erlang_F(t, lambda_, r),
            "R(t)": formulas.erlang_R(t, lambda_, r),
            "f(t)": formulas.erlang_f(t, lambda_, r),
            "λ(t)": formulas.erlang_lambda_t(t, lambda_, r),
            "ET": formulas.erlang_ET(lambda_, r),
            "σ²": formulas.erlang_wariancja(lambda_, r),
        }
        for symbol, wynik in wykladniczy.items():
            self.wyniki_wykladniczy[symbol].set(str(wynik))
        for symbol, wynik in erlang.items():
            self.wyniki_erlang[symbol].set(str(wynik))

        self.status_var.set(f"Dane przyjęte: t = {t:g} h, λ = {lambda_:g} 1/h, r = {r}.")

    def wyczysc(self) -> None:
        self.czas_var.set("")
        self.lambda_var.set("")
        self.r_var.set("")
        for zmienna in (*self.wyniki_wykladniczy.values(), *self.wyniki_erlang.values()):
            zmienna.set("—")
        self.status_var.set("Wprowadź parametry, aby wyznaczyć wskaźniki.")
        self.pola[0].focus_set()
