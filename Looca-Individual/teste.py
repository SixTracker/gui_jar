from mysql.connector import connect
import psutil
import platform
import time
import mysql.connector
from datetime import datetime
import requests
import random
import json
import string
import socket
import sys
import pyodbc

print("Script Python enviando Sql.Server em execução...")


def sql_server_connection(server, database, username, password):
    connection_string = f"DRIVER={{SQL Server}};SERVER={'54.146.1.25'};DATABASE={'sixtracker'};UID={'sa'};PWD={'Sixtracker@'}"
    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as ex:
        print(f"Erro ao conectar ao banco de dados: {ex}")
        sys.exit()


def get_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


if __name__ == "__main__":
    ip = get_ip()
    print("O ip da máquina é:", ip)

    SO = platform.system()
    print("O sistema operacional é:", SO)

    hostname = socket.gethostname()
    print("Nome do host da máquina:", hostname)

    # Obtendo a conexão com o SQL Server
    connection = sql_server_connection(server='54.146.1.25', database='sixtracker', username='sa',
                                       password='Sixtracker@')

    cursor = connection.cursor()

    # Definindo os componentes
    componentes = {
        1: "Porcentagem de Memória",
        2: "Total de Memória",
        3: "Memória Usada",
        4: "Porcentagem de Memória Swap",
        5: "Memória Swap Usada"
    }

    # Buscar os componentes cadastrados para o servidor
    cursor.execute("SELECT idComponente, nome FROM Componente WHERE fkServidor = ?", (11,))
    componentes_servidor = cursor.fetchall()

    # Verificar e adicionar os componentes de 1 a 5 se não existirem
    for componente_id, componente_nome in componentes.items():
        if not any(componente_id == comp[0] for comp in componentes_servidor):
            # Componente não encontrado, adicionar à tabela Componente
            cursor.execute("INSERT INTO Componente (nome, fkServidor) VALUES (?, ?)", (componente_nome, 11))

    if not componentes_servidor:
        print(f"Não há componentes cadastrados para o Servidor {hostname}. Cadastre componentes para continuar.")
        sys.exit()

    connection.commit()
    cursor.close()


def bytes_para_gb(bytes_value):
    return bytes_value / (1024 ** 3)


horarioAtual = datetime.now()
horarioFormatado = horarioAtual.strftime('%Y-%m-%d %H:%M:%S')

# Seu código anterior...

while True:
    # CPU
    cpuPorcentagem = psutil.cpu_percent(None)

    # Memoria
    memoriaPorcentagem = psutil.virtual_memory()[2]

    # Outros
    boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    # Obtendo a data e hora atuais no formato correto
    horarioAtual = datetime.now()
    horarioFormatado = horarioAtual.strftime('%Y-%m-%d %H:%M:%S')

    ins = [cpuPorcentagem, memoriaPorcentagem]
    componentes = [264, 265]

    cursor = connection.cursor()

    for i in range(len(ins)):
        valorRegistro = ins[i]
        componente = componentes[i]

        # Utilizando placeholders corretos para SQL Server e formatando a data
        query = "INSERT INTO Registro (valorRegistro, dataRegistro, fkComponente) VALUES (?, ?, ?)"
        cursor.execute(query, (valorRegistro, horarioAtual, componente))
        connection.commit()

    print("\n----INFORMAÇÕES DA CPU: -----")
    print(f'\nPorcentagem da CPU: {cpuPorcentagem}%')

    print("\n----INFORMAÇÕES DA MEMORIA: -----")
    print(f"\nPorcentagem utilizada de memoria: {memoriaPorcentagem}")

    cursor.close()

    # Este sleep deve estar dentro do loop
    time.sleep(10)

cursor.close()
connection.close()
