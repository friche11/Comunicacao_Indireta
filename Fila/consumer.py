import pika
import os
import time
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
# Coloque a URL da sua instancia cloudAMQP para rodar o projeto
load_dotenv()
url = os.getenv('CLOUDAMQP_URL')

# Configuração da conexão
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Conectar à fila "sorveteria"
channel.queue_declare(queue='sorveteria', durable=True)

# Lê o último ID processado
def ler_ultimo_id():
    if os.path.exists('ultimo_id.txt'):
        with open('ultimo_id.txt', 'r') as file:
            return int(file.read().strip())
    return 0

# Salva o último ID processado
def salvar_ultimo_id(ultimo_id):
    with open('ultimo_id.txt', 'w') as file:
        file.write(str(ultimo_id))

# Variável para armazenar o último ID processado
ultimo_id = ler_ultimo_id()

# Processa cada mensagem da fila
def callback(ch, method, properties, body):
    global ultimo_id
    pedido = body.decode()
    id_pedido = int(pedido.split(':')[0].split('-')[1])  # Extrair o ID do pedido

    print(f"Atendente: Novo pedido recebido: {pedido}")
    print("Atendente: Preparando o pedido...")

    # Simula o tempo de preparação do pedido
    time.sleep(3)

    print(f"Atendente: {pedido} está pronto! Entregando ao cliente.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # Atualiza e salva o último ID processado
    ultimo_id = id_pedido
    salvar_ultimo_id(ultimo_id)
    print("Atendente: Pedido processado com sucesso!\n")

# Configura o consumidor para escutar a fila
channel.basic_consume(queue='sorveteria', on_message_callback=callback)

# Tratando exeption ao usar Ctrl C para finalizar execucao
try:
   
    print(f"Atendente: Esperando pedidos a partir do ID {ultimo_id + 1}...")
    channel.start_consuming()
except KeyboardInterrupt:
    print(f"\nAtendente encerrou o sistema da sorveteria.")
    
    channel.stop_consuming()
finally:
    connection.close()