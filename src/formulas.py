"""
Parametry:
    t        — rozpatrywana chwila czasowa [h], t >= 0
    lambda_  — parametr rozkładu / intensywność [1/h], lambda_ > 0
    r        — rząd rozkładu Erlanga, liczba całkowita r >= 2

Dla obu rozkładów używamy tych samych wartości t oraz lambda_.
"""

KOMUNIKAT = "Tutaj będzie wynik"


# ============================================================
# ROZKŁAD WYKŁADNICZY
# ============================================================


def wykladniczy_F(t: float, lambda_: float) -> str:
    """F(t): prawdopodobieństwo uszkodzenia do chwili t."""
    return KOMUNIKAT


def wykladniczy_R(t: float, lambda_: float) -> str:
    """R(t): prawdopodobieństwo poprawnej pracy do chwili t."""
    return KOMUNIKAT


def wykladniczy_f(t: float, lambda_: float) -> str:
    """f(t): gęstość prawdopodobieństwa uszkodzenia."""
    return KOMUNIKAT


def wykladniczy_lambda_t(t: float, lambda_: float) -> str:
    """λ(t): intensywność uszkodzeń w chwili t."""
    return KOMUNIKAT


def wykladniczy_ET(lambda_: float) -> str:
    """ET: średni czas poprawnej pracy (bez parametru t)."""
    return KOMUNIKAT


def wykladniczy_wariancja(lambda_: float) -> str:
    """σ²: wariancja czasu poprawnej pracy (bez parametru t)."""
    return KOMUNIKAT


# ============================================================
# ROZKŁAD ERLANGA r-TEGO RZĘDU
# ============================================================


def erlang_F(t: float, lambda_: float, r: int) -> str:
    """F(t): prawdopodobieństwo uszkodzenia do chwili t."""
    return KOMUNIKAT


def erlang_R(t: float, lambda_: float, r: int) -> str:
    """R(t): prawdopodobieństwo poprawnej pracy do chwili t."""
    return KOMUNIKAT


def erlang_f(t: float, lambda_: float, r: int) -> str:
    """f(t): gęstość prawdopodobieństwa uszkodzenia."""
    return KOMUNIKAT


def erlang_lambda_t(t: float, lambda_: float, r: int) -> str:
    """λ(t): intensywność uszkodzeń w chwili t."""
    return KOMUNIKAT


def erlang_ET(lambda_: float, r: int) -> str:
    """ET: średni czas poprawnej pracy (bez parametru t)."""
    return KOMUNIKAT


def erlang_wariancja(lambda_: float, r: int) -> str:
    """σ²: wariancja czasu poprawnej pracy (bez parametru t)."""
    return KOMUNIKAT