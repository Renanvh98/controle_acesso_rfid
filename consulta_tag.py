import MFRC522
import RPi.GPIO as GPIO
import time

# Inicializa o leitor RFID
LeitorRFID = MFRC522.MFRC522()

# Função para ler o UID da tag
def ler_tag():
    status, TagType = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)

    if status == LeitorRFID.MI_OK:
        print('TAG Detectada!')
        status, uid = LeitorRFID.MFRC522_Anticoll()
        if status == LeitorRFID.MI_OK:
            print('UID da TAG:', uid)
            return uid
    return None

# Mensagem inicial
print('Aproxime a TAG')

# Loop principal
while True:
    try:
        # Tenta ler a tag
        uid = ler_tag()

        if uid:
            # Aqui você pode adicionar a lógica para processar o UID ou realizar outras ações
            print(f'UID da TAG lida: {uid}')
        else:
            print('Nenhuma TAG detectada.')

        # Pausa para evitar leituras excessivas
        time.sleep(0.5)

    except KeyboardInterrupt:
        # Caso o usuário interrompa o processo com Ctrl+C
        print("\nProcesso interrompido.")
        GPIO.cleanup()
        break

    except Exception as e:
        # Trata erros gerais
        print(f'Ocorreu um erro: {e}')
        time.sleep(1)