from connection import connection

conn = connection()
cursor = conn.cursor(dictionary=True)

def InsertPonto(n_matricula , id_tangerino:int , nome:str , dataHora , tipo:str):
    # verifica se o ponto já não existe
    resultadoExiste = ExistPonto(int(id_tangerino) , dataHora , tipo)

    # se existir retorna nada
    if resultadoExiste: return False
    # se não existir registra
    try:
        query = "INSERT INTO pontos (n_matricula , nome , dataHora_ponto , tipo , n_tangerino) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(query , (n_matricula , nome , dataHora , tipo , id_tangerino))
        return True
    
    except Exception as err :
        cursor.close()
        conn.close()
        return False

def ExistPonto(id_tangerino:int , dataHora , tipo:str):
    query = "SELECT * FROM pontos WHERE dataHora_ponto = %s , tipo = %s , n_tangerino = %s"
    try:
        cursor.execute(query , (dataHora , tipo , id_tangerino))
        data = cursor.fetchall()

        if len(data) > 0:return True
        else:return False
    except Exception as err:
        print(err)
        conn.close()
        cursor.close()
        return True
    