import math
import random
from typing import List
from tempfile import NamedTemporaryFile

from fastapi import APIRouter
from fastapi.responses import FileResponse
from openpyxl import load_workbook


router = APIRouter()

VALUE_OF_SCALE = 0.2
AMPERAGES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
MULTIPLIERS = [1] * 7 + [5] * 3


def calculate_deviation(amperage: int, multiplier: int) -> float:
    """Обислює відхилення гальванометра експерементальної установки. """

    deviation = 0.7029 * amperage / (multiplier * VALUE_OF_SCALE)

    if deviation % 1 > 0.2 and deviation % 1 < 0.8:  # дробова частина
        deviation += random.uniform(-0.6, 0.6)       # емуляція округлення на око

    return round(deviation) * (multiplier * VALUE_OF_SCALE)


def create_workbook() -> 'openpyxl.workbook.workbook.Workbook':

    deviations = [[calculate_deviation(amperage, multiplier) for amperage, multiplier in zip(AMPERAGES, MULTIPLIERS)]
                                                             for row in range(5)]

    workbook = load_workbook(filename='app/templates/physics_2_12.xlsx')
    datasheet = workbook['Data']

    for deviations_row, cells_row in zip(deviations, datasheet['H2:Q6']):
        for deviation, cell in zip(deviations_row, cells_row):
            cell.value = deviation

    return workbook


@router.get('/files/physics/2_12.xlsx')
def download():
    workbook = create_workbook()
    tmp = NamedTemporaryFile(delete=False)
    workbook.save(tmp.name)
    return FileResponse(tmp.name, filename='Лабораторна 2-12.xlsx')
