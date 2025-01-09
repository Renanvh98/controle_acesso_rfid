import MFRC522
import RPi.GPIO as GPIO
import time

# Configuração do GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

# Dicionário de tags liberadas (UID, Nome)
tags_liberadas = {
    (197, 12, 12, 171, 110): 'ricardo',
    (68, 138, 241, 197, 250): 'alura'
}

# Inicializa o leitor RFID
LeitorRFID = MFRC522.MFRC522()

# Função para liberar a porta
def libera_porta():
    GPIO.output(7, 1)  # Abre a porta (ligando o pino GPIO)
    print('Porta Aberta!')
    time.sleep(3)  # A porta fica aberta por 3 segundos
    print('Porta Fechada!')
    GPIO.output(7, 0)  # Fecha a porta (desligando o pino GPIO)

# Mensagem inicial
print('Aproxime a TAG')

# Loop principal
try:
    while True:
        # Verifica se existe TAG no leitor
        (status, TagType) = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)

        # Se uma TAG foi detectada
        if status == LeitorRFID.MI_OK:
            print('TAG Detectada!')
            (status, uid) = LeitorRFID.MFRC522_Anticoll()

            if status == LeitorRFID.MI_OK:
                # Converte o UID para uma tupla
                uid = tuple(uid)
                print(f'UID lido: {uid}')

                # Verifica se o UID está nas tags liberadas
                if uid in tags_liberadas:
                    nome_usuario = tags_liberadas[uid]
                    print(f'Acesso Liberado para {nome_usuario}!')
                    libera_porta()  # Libera a porta
                else:
                    print('Acesso Negado! UID inválido.')

        # Pausa para evitar leituras contínuas
        time.sleep(0.5)

except KeyboardInterrupt:
    # Interrupção do programa com Ctrl+C
    print("\nPrograma interrompido. Limpeza dos pinos GPIO.")
    GPIO.cleanup()

except Exception as e:
    # Trata qualquer outro erro inesperado
    print(f'Ocorreu um erro: {e}')
    GPIO.cleanup()