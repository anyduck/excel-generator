import math
import random
from typing import List
from tempfile import NamedTemporaryFile

from fastapi import APIRouter
from fastapi.responses import FileResponse
from openpyxl import load_workbook


router = APIRouter()

ADDITIONAL_RESISTANCE = 8.9
INNER_RADIUS = 0.5
OUTER_RADIUS = 10


def calculate_amperage(voltage: float, radius: float) -> float:
    """Обислює силу струму на основі віртуальної лаби 2-5."""

    if radius > .5 and radius < 10:
        voltage *= math.log(OUTER_RADIUS/radius) \
                 / math.log(OUTER_RADIUS/INNER_RADIUS)
    elif radius >= 10:
        voltage = 0

    amperage = voltage * ADDITIONAL_RESISTANCE

    if amperage % 1 > 0.3 and amperage % 1 < 0.7:  # дробова частина
        amperage += random.uniform(-0.5, 0.5)      # емуляція округлення на око

    return round(amperage)


def create_workbook() -> 'openpyxl.workbook.workbook.Workbook':

    voltage = round(random.uniform(4.5, 5.5), 1)  # напруга від 4.5 до 5.5 В
    amperages = [[calculate_amperage(voltage, radius) for column in range(4)]
                                                      for radius in range(9)]

    workbook = load_workbook(filename='app/templates/physics_2_5.xlsx')
    datasheet = workbook['Data']

    for amperages_row, cells_row in zip(amperages, datasheet['B3:E11']):
        for amperage, cell in zip(amperages_row, cells_row):
            cell.value = amperage

    return workbook


@router.get('/files/physics/2_5.xlsx')
def download():
    workbook = create_workbook()
    tmp = NamedTemporaryFile(delete=False)
    workbook.save(tmp.name)
    return FileResponse(tmp.name, filename='Лабораторна 2-5.xlsx')
