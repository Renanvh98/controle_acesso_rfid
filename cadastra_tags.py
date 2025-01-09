import boto3

# Conectar ao serviço DynamoDB da AWS
dynamodb = boto3.resource('dynamodb')

# Referência para a tabela 'tags' no DynamoDB
table = dynamodb.Table('tags')

# Dados de exemplo (Cartões de RFID) a serem armazenados no DynamoDB
cartoes = {
    '1971212171110': 'Renan',  # Exemplo: Cartão de RFID do usuário Renan
    '1971212171111': 'teste',  # Exemplo: Cartão de RFID de teste
    '1971212171112': 'teste2'  # Exemplo: Cartão de RFID de teste 2
}

# Usando o batch_writer para inserir múltiplos itens de forma eficiente
with table.batch_writer() as batch:
    for id, usuario in cartoes.items():
        try:
            # Inserção de item no DynamoDB
            batch.put_item(
                Item={
                    'id': id,  # Chave primária do item (cartão RFID)
                    'usuario': usuario  # Nome do usuário associado ao cartão RFID
                }
            )
            # Exibir confirmação no console
            print(f'Cartão {id} associado a {usuario} inserido com sucesso.')
        except Exception as e:
            # Caso haja erro na inserção, exibir mensagem de erro
            print(f'Erro ao inserir o cartão {id}: {str(e)}')