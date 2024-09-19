import pika
import os
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
# Coloque a URL da sua instancia cloudAMQP para rodar o projeto
load_dotenv()
url = os.getenv('CLOUDAMQP_URL')

# Solicitar o nome do cliente ao iniciar o script
nome_cliente = input("Digite seu nome para se inscrever nos anúncios de novos sabores: ")

# Configuração da conexão
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Conectar-se à exchange do tipo fanout
channel.exchange_declare(exchange='novos_sabores', exchange_type='fanout')

# Criar uma fila exclusiva para cada subscriber
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Vincular a fila do subscriber à exchange
channel.queue_bind(exchange='novos_sabores', queue=queue_name)

print(f"{nome_cliente}, você está inscrito para receber anúncios de novos sabores.")

# Função de callback para processar cada mensagem recebida
def callback(ch, method, properties, body):
    print(f"{nome_cliente}: Novo anúncio recebido - {body.decode()}")

# Configurar o subscriber para escutar a fila
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(f"{nome_cliente}: Aguardando anúncios de novos sabores...")
channel.start_consuming()
