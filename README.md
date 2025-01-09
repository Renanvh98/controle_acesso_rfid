# Sistema de Controle de Acesso RFID

Este projeto implementa um sistema de controle de acesso utilizando um leitor de RFID e integração com o DynamoDB da AWS.

## Descrição

Este sistema lê as tags RFID, consulta um banco de dados DynamoDB para verificar se o usuário está autorizado e registra o acesso em uma tabela de logs no DynamoDB. Caso o acesso seja autorizado, a porta será liberada. Caso contrário, o acesso será negado.

## Objetivo

O principal objetivo deste projeto é aprender a integrar hardware (leitor RFID) com serviços da AWS, utilizando o Python para controle e manipulação dos dados.

## Autor

- Renan Vinicius

## Créditos

Este código foi desenvolvido como parte do curso [Nome do Curso]. O código foi adaptado e modificado para fins de aprendizado.

## Tecnologias

- Python
- MFRC522 (Leitor RFID)
- AWS DynamoDB
- RPi.GPIO (para controle de GPIO na Raspberry Pi)

## Como usar

1. Conecte o leitor RFID à Raspberry Pi.
2. Configure as credenciais da AWS para acesso ao DynamoDB.
3. Execute o código Python para iniciar o sistema.

## Licença

Este projeto está licenciado sob a [licença XYZ].
