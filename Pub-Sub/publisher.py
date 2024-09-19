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

# Cria a exchange do tipo fanout para enviar os anúncios
channel.exchange_declare(exchange='novos_sabores', exchange_type='fanout')

# Lista de novos sabores a serem anunciados
novos_sabores = [
    "Novo sabor de pistache disponível!",
    "Sorvete de manga com maracujá agora na sorveteria!",
    "Chegou o sorvete de doce de leite com nozes!",
    "Experimente o novo sorvete de açaí com banana!"
]

# Tratando exeption ao usar Ctrl C para finalizar execucao
try:
    # Publicar cada novo sabor na exchange
    for sabor in novos_sabores:
        channel.basic_publish(
            exchange='novos_sabores',
            routing_key='',  
            body=sabor
        )
        print(f"Sorveteria: Anúncio publicado - {sabor}")
except KeyboardInterrupt:
    print("\nSorveteria: Publicação interrompida pelo usuário.")
finally:
    
    channel.close()
    connection.close()