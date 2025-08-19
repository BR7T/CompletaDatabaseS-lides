from datetime import datetime
import time
from functions.convertMsToDate import timeConvert
from functions.connection import connection
from functions.Solides.get import GetAllSolidesFunc , GetAllSolidesPontos


DataPonto = GetAllSolidesPontos()
DataFunc = GetAllSolidesFunc()

for d in DataPonto:
    d["nome"] = DataFunc.get(d["employeeId"] , "Desconhecido")


horaAtual = None

def AtualizaBanco():
    for d in DataPonto:
        dataHoraformatadaStart = timeConvert(d["startDateTimestamp"])
        dataHoraformatadaEnd = timeConvert(d["endDateTimestamp"])

        print(dataHoraformatadaStart)
        print(dataHoraformatadaEnd)
        print("tempo trabalhado " , dataHoraformatadaEnd - dataHoraformatadaStart)
        print("\n")

while True:
    horaAtual = datetime.now().time()

    if horaAtual == horaAtual:
        AtualizaBanco()

    time.sleep(5)





