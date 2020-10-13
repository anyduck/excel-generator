import math
import random
from typing import List
from openpyxl import load_workbook


RANGES = [0.70, 0.70, 0.70, 0.67, 0.67, 0.67, 0.64, 0.64, 0.64,
          0.60, 0.60, 0.60, 0.57, 0.57, 0.57, 0.54, 0.54, 0.54,
          0.51, 0.51, 0.51, 0.48, 0.48, 0.48, 0.45, 0.45, 0.45,
          0.41, 0.41, 0.41, 0.38, 0.38, 0.38, 0.35, 0.35, 0.35,
          0.32, 0.32, 0.32, 0.28, 0.28, 0.28, 0.25, 0.25, 0.25]


def calculate_period(a: float, a0: float) -> float:
    """Обислює період коливання маятника на основі віртуальної лаби 1-2."""

    lenght = 225 - 300 * (0.75 - a)
    omega = (2*lenght*a0 / (lenght**2 + a0**2)) ** 0.5 / 10

    return 2 * math.pi / omega / 33


def generate_period(a: float, a0: float, sigma: float, mu: float) -> float:
    return calculate_period(a, a0) + random.gauss(sigma, mu)


def generate_data(ranges: list, delta: float, mu: float) -> List[float]:
    sigma = delta / 3                   # cигма (https://bit.ly/3naLuFm)
    a0 = random.randrange(124, 134)
    return [round(10 * generate_period(a, a0, sigma, mu), 2) for a in ranges]


def create_workbook() -> 'openpyxl.workbook.workbook.Workbook':
    delta = random.uniform(0.02, 0.03)  # рамки відхилення
    mu = random.uniform(-0.005, 0.01)   # мода вибірки
    periods = generate_data(RANGES, delta, mu)

    workbook = load_workbook(filename='../templates/physics_1_2.xlsx')
    datasheet = workbook['Data']

    for period, (cell, *_) in zip(periods, datasheet['C2:C46']):
        cell.value = period

    return workbook
