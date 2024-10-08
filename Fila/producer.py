import pika
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
# Coloque a URL da sua instancia cloudAMQP para rodar o projeto
load_dotenv()
url = os.getenv('CLOUDAMQP_URL')

# Configuração da conexão
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Cria uma fila chamada "sorveteria"
channel.queue_declare(queue='sorveteria', durable=True)

# Lê o último ID processado
def ler_ultimo_id():
    if os.path.exists('ultimo_id.txt'):
        with open('ultimo_id.txt', 'r') as file:
            return int(file.read().strip())
    return 0

# Variável para o último ID processado
ultimo_id = ler_ultimo_id()

# Lista de pedidos a serem enviados
pedidos = [
    'sorvete de chocolate',
    'sorvete de baunilha',
    'sorvete de morango',
    'milk shake de ovomaltine'
]

# Tratando exeption ao usar Ctrl C para finalizar execucao
try:
    # Enviar cada pedido para a fila
    for idx, pedido in enumerate(pedidos, start=ultimo_id + 1):
        pedido_com_id = f"ID-{idx}: {pedido}"
        channel.basic_publish(
            exchange='',
            routing_key='sorveteria',
            body=pedido_com_id,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Tornar a mensagem persistente
            )
        )
        print(f"\nCliente: Pedido de {pedido_com_id} enviado para a sorveteria!")

except KeyboardInterrupt:
    print("\nEnvio de pedidos interrompido pelo usuário.")
finally:
    
    channel.close()
    connection.close()
