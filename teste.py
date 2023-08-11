import mysql.connector


database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="site_enem"
)

def insertData(nome, sexo, idade, email, telefone, msg):

    global cursor
    try: 
        cursor = database.cursor()
        cursor.execute('INSERT INTO Nome VALUES ?', nome)
        cursor.execute('INSERT INTO Sexo VALUES ?', sexo)
        cursor.execute('INSERT INTO Idade VALUES ?', idade)
        cursor.execute('INSERT INTO Email VALUES ?', email)
        cursor.execute('INSERT INTO Telefone VALUES ?', telefone)
        cursor.execute('INSERT INTO Mensagem VALUES ?', msg)      

    except Exception as e:
        return f"Erro: {e}"

    finally:

        database.commit()
        cursor.close()
        database.close()
        return "Done"



insertData(nome='Daniel Freitas do Amaral', sexo="M",idade=19,email='waterfox@gmail.com',telefone=991462904,msg='Site bem estruturado e responsívo e acessível, bom trabalho!') # type: ignore