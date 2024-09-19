import pika
import os
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
# Coloque a URL da sua instancia cloudAMQP para rodar o projeto
load_dotenv()
url = os.getenv('CLOUDAMQP_URL')

# Configuração da conexão
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Criar a exchange do tipo fanout para enviar os anúncios
channel.exchange_declare(exchange='novos_sabores', exchange_type='fanout')

# Lista de novos sabores a serem anunciados
novos_sabores = [
    "Novo sabor de pistache disponível!",
    "Sorvete de manga com maracujá agora na sorveteria!",
    "Chegou o sorvete de doce de leite com nozes!",
    "Experimente o novo sorvete de açaí com banana!"
]

# Publicar cada novo sabor na exchange
for sabor in novos_sabores:
    channel.basic_publish(
        exchange='novos_sabores',
        routing_key='',  # Não é necessário especificar uma fila
        body=sabor
    )
    print(f"Sorveteria: Anúncio publicado - {sabor}")

# Fechar a conexão
channel.close()
connection.close()
