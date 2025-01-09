from boto3.dynamodb.conditions import Key
import boto3
import datetime
import MFRC522
import RPi.GPIO as GPIO
import time

# Configuração do DynamoDB
dynamodb = boto3.resource('dynamodb')
tabelaTags = dynamodb.Table('tags')
tabelaLogs = dynamodb.Table('logs')

# Configuração do Leitor RFID
LeitorRFID = MFRC522.MFRC522()

# Função para ler a tag do RFID
def le_tag():
    while True:
        # Verifica se existe TAG no leitor
        (status, TagType) = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)

        # Leitura da TAG
        if status == LeitorRFID.MI_OK:
            print('TAG Detectada!')
            (status, uid) = LeitorRFID.MFRC522_Anticoll()
            uid = ''.join(str(registro) for registro in uid)
            break  # Sai do loop após a leitura
    return uid

# Função para consultar a tag no DynamoDB
def consulta_db(uid):
    try:
        resultado_consulta = tabelaTags.query(
            KeyConditionExpression=Key('id').eq(uid)
        )
        return resultado_consulta
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {e}")
        return None

# Função para validar o acesso da tag
def valida_tag(resultado_consulta):
    if resultado_consulta and len(resultado_consulta['Items']) == 1:
        usuario = resultado_consulta['Items'][0]['usuario']
        print(f'Usuario: {usuario} - Acesso Liberado!')
        acesso = 'Liberado'
    else:
        print('Usuario: Inválido - Acesso Negado!')
        acesso = 'Negado'
    return acesso

# Função para registrar o acesso no DynamoDB
def registra_acesso(uid, acesso):
    timestamp = str(datetime.datetime.now())
    try:
        tabelaLogs.put_item(
            Item={
                'timestamp': timestamp,
                'id': uid,
                'acesso': acesso
            }
        )
        print(f'Acesso registrado: {uid} - {acesso} - {timestamp}')
    except Exception as e:
        print(f"Erro ao registrar o acesso: {e}")

# Loop principal
try:
    while True:
        uid = le_tag()  # Lê a tag do RFID
        resultado_consulta = consulta_db(uid)  # Consulta o banco de dados
        if resultado_consulta:
            acesso = valida_tag(resultado_consulta)  # Valida o acesso
            registra_acesso(uid, acesso)  # Registra o acesso no banco de dados
        time.sleep(0.5)

except KeyboardInterrupt:
    # Interrupção do programa com Ctrl+C
    print("\nPrograma interrompido. Limpeza dos pinos GPIO.")
    GPIO.cleanup()

except Exception as e:
    # Trata outros erros inesperados
    print(f'Ocorreu um erro inesperado: {e}')
    GPIO.cleanup()
