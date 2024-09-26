
<h1 align="center" style="font-weight: bold;">Sorveteria - Comunicação Indireta</h1>

</br>
  <b>Esse projeto é uma simples demonstração de comunicação indireta por meio de uma sorveteria usando Python e RabbitMQ. Os padrões de mensageria implementados e comparados foram os de fila de mensagens e publicação-assinatura.</b>
</p>

<h2 id="started">🚀 Rodando localmente</h2>

<h3>Pré-requisitos</h3>

Ter instalado todas as tecnologias abaixo:

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [VsCode](https://code.visualstudio.com/download)

<h3>Clonando</h3>

Abra o git bash em alguma pasta e insira o comando abaixo para clonar o repositório

```bash
https://github.com/friche11/Comunicacao_Indireta.git
```
<h3> Abrindo e executando o projeto</h2>

Abra a pasta do projeto clonado, botão direito do mouse e clique em "Open git bash here". O terminal do git bash abrirá e você executará o comando abaixo para abrir o projeto no vscode

```bash
code .
```

Com o projeto aberto você deve criar um .env e colocar a url de seu cloudAMQP em uma variável de ambiente descrita abaixo.
</br>
</br>
 `CLOUDAMQP_URL= `

Agora basta instalar os módulos abaixo usando os comandos no terminal e na raiz do projeto. O primeiro módulo é necessário para se comunicar com o RabbitMQ, enquanto o segundo é responsável por carregar variáveis de ambiente a partir de um arquivo .env

```bash
pip install pika
```

```bash
pip install python-dotenv
```

Agora você pode executar cada classe em python e ver o funcionamento de cada um dos projetos. Lembre-se de entrar na pasta do projeto que você deseja executar antes de tentar executar uma classe. Para isso, basta colocar o comando  `cd Fila` ou  `cd Pub-Sub` para entrar no diretório de cada um dos projetos.
</br>
</br>
Depois de entrar no diretório de um projeto específico, rode uma das classes usando `python (nomeDaClasse.py)` no terminal. Exemplo: entre no projeto de fila e rode `python producer.py`
</br>
</br>
Agora abra outro terminal e execute o consumer para ver as mensagens/pedidos na fila sendo consumidas! 
</br>
</br>
Agora você pode executar o projeto de pub/sub, entre na pasta dele usando `cd Pub-Sub` e execute a classe de subscriber, coloque seu nome e deixe o terminal rodando. Agora abra outro terminal e execute novamente o subscriber, mas coloque outro nome de usuário. Por fim, execute em outro terminal o publisher e veja que todos os usuários que se inscreveram no tópico irão receber anúncios de novos sabores da sorveteria.
</br>
</br>
Se ainda tiver dúvidas, confira o vídeo abaixo:
</br>
https://youtu.be/GV7sdFoFpmk

<h3>Como o RabbitMQ é utilizado?</h3>

- Exchange: A exchange utilizada é do tipo fanout chamada novos_sabores. Ela distribui as mensagens de anúncios para todos os consumidores que estão inscritos nas filas vinculadas a essa exchange. A exchange novos_sabores é usada para enviar mensagens relacionadas aos novos sabores de sorvete.
- Fila principal de pedidos: A fila sorveteria recebe os pedidos de clientes. Cada pedido enviado para a sorveteria é enfileirado nessa fila.
- Filas exclusivas para assinantes: Cada cliente que se inscreve para receber anúncios de novos sabores terá uma fila exclusiva criada dinamicamente. Essas filas recebem os anúncios publicados na exchange novos_sabores.
- Bindings: As filas de anúncios (criadas para cada cliente assinante) são vinculadas à exchange novos_sabores sem uma chave de roteamento específica, pois a exchange é do tipo fanout, e envia as mensagens para todas as filas associadas.
A fila de pedidos (sorveteria) é diretamente acessada através do envio de mensagens com a chave de roteamento vazia (routing_key=''), o que é adequado para uma fila direta.
  
<h3> Observações</h2>

Persistência de IDs: O último ID de pedido processado é salvo em um arquivo ultimo_id.txt. Isso garante que, em caso de reinicialização do sistema, os pedidos continuem sendo processados a partir do último ID registrado, mantendo a continuidade e evitando duplicações.

