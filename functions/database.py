from .connection import connection
from datetime import datetime

from functions.convertMsToDate import timeConvert



def InsertPonto(n_matricula , id_tangerino:int , nome:str , dataHora , tipo:str , workplaceName:str):
    # verifica se o ponto já não existe
    resultadoExiste = ExistPonto(int(id_tangerino) , dataHora , tipo)

    # se existir retorna nada
    if resultadoExiste: return
    # se não existir registra
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        query = "INSERT INTO pontos (n_matricula , nome , dataHora_ponto , tipo , n_tangerino , setor) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(query , (n_matricula , nome , dataHora , tipo , id_tangerino,workplaceName))
        conn.commit()
        return True
    
    except Exception as err :
        print(err)
    finally:
        cursor.close()
        conn.close()




def ExistPonto(id_tangerino:int , dataHora , tipo:str):
    query = "SELECT * FROM pontos WHERE dataHora_ponto = %s AND tipo = %s AND n_tangerino = %s"
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query , (dataHora , tipo , id_tangerino))
        data = cursor.fetchall()

        if len(data) > 0:return True
        else:return False

    except Exception as err:
        print(err)
    finally:
        conn.close()
        cursor.close()
        
    

def Jornada(id_tangerino , dataStart , n_matricula , nome , setor):
    # só a data, sem hora
    data_chave = dataStart.date()
    # diferença em minutos    
    conn = connection()
    rows = _pontos_do_dia_(id_tangerino , data_chave)
    minutos = _calcula_minutos_(rows)
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO jornadadiaria (nome , datajornada , n_matricula , minutosTrabalhadas , id_tangerino , setor) VALUES (%s , %s , %s , %s, %s , %s)
            ON DUPLICATE KEY UPDATE
                minutosTrabalhadas = VALUES(minutosTrabalhadas),
                nome = VALUES(nome),
                n_matricula = VALUES(n_matricula),
                setor = VALUES(setor)
        """

        cursor.execute(query , (nome , data_chave , n_matricula , minutos , id_tangerino , setor))
        conn.commit()
        return minutos
    finally:
        try: cursor.close()
        except: pass
        try: conn.close()
        except: pass


def _pontos_do_dia_(id_tangerino , dataStart):
    data_chave = dataStart.date() if hasattr(dataStart, "date") else dataStart
    try:
        conn = connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT n_tangerino, datahora_ponto , tipo FROM pontos WHERE DATE(datahora_ponto) = %s AND n_tangerino = %s ORDER BY datahora_ponto ASC", 
            (data_chave , id_tangerino)
        )
        data = cursor.fetchall()
        return data
    except Exception as err:
        print(err)
    finally:
        try: cursor.close()
        except: pass
        try: conn.close()
        except: pass

def _calcula_minutos_(list):
    obj = list
    mins , entrada = 0 , None
    for d in obj:
        data = d.get("datahora_ponto")
        tipo = d.get("tipo")
        if tipo == "entrada":
            entrada = data
        elif tipo == "saida" and entrada and data>entrada:
            mins += int((data - entrada).total_seconds() // 60)
            entrada = None
    return mins




