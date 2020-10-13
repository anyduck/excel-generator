import math
import random
from tempfile import NamedTemporaryFile

from fastapi import APIRouter
from fastapi.responses import FileResponse
from openpyxl import load_workbook


router = APIRouter()

def generate_time(period: float, sigma: float, mu: float) -> float:
    return round(5*(period + random.gauss(mu, sigma)), 2)

def calculate_period(length: float, g: float) -> float:
    return 2 * math.pi * math.sqrt(length/g)

def create_workbook() -> 'openpyxl.workbook.workbook.Workbook':
    delta = random.uniform(0.04, 0.05)  # рамки відхилення
    sigma = delta / 3                   # cигма (https://bit.ly/3naLuFm)
    mu = random.uniform(-0.01, 0.01)    # мода вибірки

    period = calculate_period(length=2.5, g=9.83)

    workbook = load_workbook(filename='app/templates/physics_1_1.xlsx')
    datasheet = workbook['Data']

    for cell, *_ in datasheet['B2:B101']:
        cell.value = generate_time(period, sigma, mu)

    return workbook


@router.get('/files/physics/1_1.xlsx')
def download():
    workbook = create_workbook()
    tmp = NamedTemporaryFile(delete=False)
    workbook.save(tmp.name)
    return FileResponse(tmp.name, filename='Лабораторна 1-1.xlsx')
