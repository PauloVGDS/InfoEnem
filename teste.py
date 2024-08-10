import mysql.connector

class dataControl:
    def __init__(self, user, password, host, auth_plugin):
        self.user = user
        self.password = password
        self.host = host
        self.auth_plugin = auth_plugin

    def connect(self):
        try:
            self.connection = mysql.connector.connect(user=self.user, 
                                                  password=self.password, 
                                                  host=self.host, 
                                                  auth_plugin= self.auth_plugin, autocommit=True)
        except mysql.connector.errors.Error as erro:
            print(f"A conexão falhou por causa: \t{erro}\n")
            return False
        
        finally:
            if self.connection.is_connected():
                cursor = self.connection.cursor()  
                if not self.create():
                    cursor.execute("USE crud;")
                    print("Tabela selecionada!\n")
                print("Conexão realizada com sucesso!\n")
                return True
            print("Não foi possível conectar ao banco de dados!\n")
            return False

    def disconnect(self):
        try:
            if self.connection.is_connected():
                self.connection.disconnect()
                return True    
        except AttributeError:
            print("Banco de dados não iniciado!\n")
            return False
        except mysql.connector.errors.Error as erro:
            print(f"A desconexão falhou por causa: \n{erro}\n")
            return False
        finally:
            if not self.connection.is_connected():
                print("Desconectado com sucesso!\n")

                return True
            return False
        
    def create(self):
        try:
            if not self.connection.is_connected():
                print("Nenhum servidor encontrado!\n")
                return False
                
            cursor = self.connection.cursor()
            cursor.execute("CREATE SCHEMA crud;")
            cursor.execute("USE crud;")
            cursor.execute("""
                            CREATE TABLE usuarios(
                                id INT(5) PRIMARY KEY AUTO_INCREMENT, 
                                nome VARCHAR(30) NOT NULL, 
                                email VARCHAR(30) NOT NULL UNIQUE, 
                                senha VARBINARY(32) NOT NULL, 
                                birth DATE, 
                                genero ENUM('Masculino', 'Feminino'));
            """)
            print("Tabela criada com sucesso!\n")
            return True

        except mysql.connector.errors.Error as erro:
            if "exists" in str(erro):
                print("A Tabela já existe!\n")
                return False
            print(f"Não foi possível criar a tabela: \t{erro}\n")
            return False

    def read(self, answer):
        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s;", (answer,))
            result = cursor.fetchone()        

            if result == None:
                print("Não foi possível encontrar o usuário!\n")
                return False
            print("Usuário encontrado!\n")
            return result
        
        except mysql.connector.errors.Error:
            print("Operação não concluída!")
            return False

    def update(self, email, option, answer, master):
        try:
            email = email.strip()
            answer = answer.strip()
            cursor = self.connection.cursor()
            if not dataControl.read(self, email):
                return False

                
            query = ("UPDATE usuarios SET nome = '{}' WHERE email = '{}';").format(answer, email)
            cursor.execute(query)

            query = ("UPDATE usuarios SET email = '{}' WHERE email = '{}';").format(answer, email)
            cursor.execute(query)

            query = ("UPDATE usuarios SET senha = {} WHERE email = '{}';").format(answer, email)
            cursor.execute(query)

            query = ("UPDATE usuarios SET birth = '{}' WHERE email = '{}';").format(answer, email)
            cursor.execute(query)

            query = ("UPDATE usuarios SET genero = '{}' WHERE email = '{}';").format(answer, email)
            cursor.execute(query)

        except mysql.connector.errors.Error as erro:
            print(f"Não foi possível concluir a operação: {erro}\n")
            return False

    def delete(self, email, master):
        try:
            if not dataControl.read(self, email):
                return False
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM usuarios WHERE email = %s", (email,))
            print("Usuário removido!\n")
            return True
        
        except mysql.connector.errors.Error as erro:
            print(f"Não foi possível concluír a operação: {erro}\n")
            return False

    def insert(self, nome, email, senha, birth="", genero="", master=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha, birth, genero) VALUES (%s, %s, %s, %s, %s);", (nome, email, senha, birth, genero))
            print("Registro inserido!\n")
            return True
        
        except mysql.connector.errors.Error as erro:
            if "Duplicate" in str(erro):
                print("Email já cadastrado!\n")
                return False
            print(f"Não foi possível inserir os dados por causa: \t{erro}\n")
            return False
