from datetime import datetime , timedelta
from functions.convertMsToDate import timeConvert
from functions.database import InsertPonto , Jornada
from functions.Solides.get import GetAllSolidesPontos , _GetAllEmployeesAndWorkPlace_


def AtualizaBanco(obj):
    nome = obj.get("employeeName")
    horarioPonto = timeConvert(obj.get("dateIn"))
    id_tangerino = obj.get("employeeId")
    id_matricula = obj.get("employeeExternalId")
    horarioSaida = obj.get("dateOut")
    workplaceName = obj.get("workPlaceName")
    if horarioSaida:
        horarioSaida = timeConvert(horarioSaida)
        InsertPonto(id_matricula , id_tangerino , nome , horarioSaida , "saida" , workplaceName)
        Jornada(id_tangerino , horarioPonto , id_matricula , nome , workplaceName)
        
    InsertPonto(id_matricula , id_tangerino , nome , horarioPonto , "entrada" , workplaceName)

page = 0

diaconsulta = datetime.now().date() - timedelta(days=1)
dt = datetime.combine(diaconsulta, datetime.min.time())
form = int(dt.timestamp() * 1000)

dataEmployees , dataWorkPlace = _GetAllEmployeesAndWorkPlace_()

baseWorkPlace = {w.get("id"): w.get("name")  for w in dataWorkPlace.get("content")}

baseEmployees = {}
for e in dataEmployees['content']:
    w1 = e.get("workplaceList") or []
    wpl = w1[0].get("id") if w1 else None
    baseEmployees[e["id"]] = {
        "workPlaceId" : wpl,
        "workplaceName" : baseWorkPlace.get(wpl , "Desconhecido")
    }

while True:

    resp = GetAllSolidesPontos(page , form)
    content = (resp or {}).get("content") or []

    if not content:
        break

    for obj in content:
        baseCruza = baseEmployees.get(obj.get("employeeId"))
        obj["workPlaceName"] = baseCruza.get("workplaceName")

        if obj.get("allowance"):
            continue
        AtualizaBanco(obj)
    
    page += 1





