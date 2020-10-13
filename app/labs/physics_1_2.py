import math
import random
from typing import List
from tempfile import NamedTemporaryFile

from fastapi import APIRouter
from fastapi.responses import FileResponse
from openpyxl import load_workbook


router = APIRouter()

def calculate_period(a: float, a0: float) -> float:
    """Обислює період коливання маятника на основі віртуальної лаби 1-2."""

    lenght = 225 - 300 * (0.75 - a)
    omega = (2*lenght*a0 / (lenght**2 + a0**2)) ** 0.5 / 10

    return 2 * math.pi / omega / 33

def generate_time(a: float, a0: float, sigma: float, mu: float) -> float:
    return round(10*(calculate_period(a, a0) + random.gauss(sigma, mu)), 2)

def create_workbook() -> 'openpyxl.workbook.workbook.Workbook':
    ranges = [0.70, 0.70, 0.70, 0.67, 0.67, 0.67, 0.64, 0.64, 0.64,
              0.60, 0.60, 0.60, 0.57, 0.57, 0.57, 0.54, 0.54, 0.54,
              0.51, 0.51, 0.51, 0.48, 0.48, 0.48, 0.45, 0.45, 0.45,
              0.41, 0.41, 0.41, 0.38, 0.38, 0.38, 0.35, 0.35, 0.35,
              0.32, 0.32, 0.32, 0.28, 0.28, 0.28, 0.25, 0.25, 0.25]
    delta = random.uniform(0.02, 0.03)  # рамки відхилення
    sigma = delta / 3                   # cигма (https://bit.ly/3naLuFm)
    mu = random.uniform(-0.005, 0.01)   # мода вибірки
    a0 = random.randrange(124, 134)

    workbook = load_workbook(filename='app/templates/physics_1_2.xlsx')
    datasheet = workbook['Data']

    for a, (cell, *_) in zip(ranges, datasheet['C2:C46']):
        cell.value = generate_time(a, a0, sigma, mu)

    return workbook


@router.get('/files/physics/1_2.xlsx')
def download():
    workbook = create_workbook()
    tmp = NamedTemporaryFile(delete=False)
    workbook.save(tmp.name)
    return FileResponse(tmp.name, filename='Лабораторна 1-2.xlsx')
