# tweetMetricsComprehend

![tweetMetric drawio](https://github.com/GaberRB/tweetMetricsComprehend/assets/28874479/1412002e-1451-4372-9fc7-f5059c87c7ce)

## Descrição
O projeto **tweetMetricsComprehend** é uma solução que visa monitorar o sentimento das postagens do Twitter e classificar se um tweet é Negativo, Positivo, Neutro ou Misto. Essas informações são exibidas em um painel de controle no Grafana.

## Funcionalidades
1. **Serviço de coleta de Tweets**
   - Este serviço, construído em Python, é responsável por acessar a API do Twitter e buscar os últimos tweets postados com base em uma palavra-chave específica. Neste caso, escolhemos uma marca ou empresa para simular um cenário.
   - Após a coleta dos tweets, o serviço processa a resposta da API do Twitter e produz as mensagens no tópico do Kafka.

2. **Comunicação entre os Serviços**
   - A comunicação entre os serviços é feita de forma assíncrona, utilizando o Apache Kafka. Os serviços são responsáveis por produzir e consumir os dados do tópico.

3. **Serviço de Análise de Sentimento**
   - Este serviço, construído em Go, consome as mensagens do tópico contendo os dados dos tweets e processa-os utilizando a IA da AWS Comprehend. Ele analisa o texto e determina se o conteúdo é positivo, negativo ou neutro.
   - Após o processamento, as métricas são criadas usando o Prometheus, que é responsável por contabilizar a quantidade de cada sentimento.

4. **Exposição das Métricas**
   - Utilizando o Prometheus, as métricas são expostas através de uma rota, permitindo a visualização e monitoramento dos dados.
   - O Grafana é utilizado para criar dashboards que mostram as métricas de sentimentos, permitindo acompanhar a repercussão de uma marca.

5. **Banco de Dados**
   - Após o processamento, os dados processados são armazenados no MySQL para consultas posteriores.

6. **Grafana Dashboard**
   - O Grafana oferece diversas possibilidades de visualização. No dashboard criado para este projeto, é possível acompanhar a repercussão de uma marca por meio das métricas de sentimentos.

## Configuração do Ambiente
O projeto utiliza o Docker Compose para facilitar a montagem do ambiente com todos os serviços necessários. São utilizados contêineres para executar o código Python e Go, o tópico no Kafka, o Prometheus, o Grafana e o MySQL.

## Pré-requisitos
Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina antes de prosseguir.

## Instalação e Configuração
1. Clone este repositório em sua máquina:
   git clone https://github.com/GaberRB/tweetMetricsComprehend.git

2. Navegue até o diretório clonado:
   cd tweetMetricsComprehend/docker

3. Execute o Docker Compose para iniciar os serviços:
   docker-compose up -d

4. Aguarde até que todos os serviços estejam em execução.
5. Após subida do ambiente aqui está a lista de acessos do localhost
  - Kafdrop: Acesse o Kafdrop em http://localhost:9000 para visualizar e explorar os tópicos e mensagens do Kafka.

  - Prometheus: Acesse o Prometheus em http://localhost:9090 para visualizar as métricas coletadas do Kafka.

  - Grafana: Acesse o Grafana em http://localhost:3000 e faça login com as credenciais padrão (usuário: admin, senha: admin). Configure um novo painel para         
    visualizar os dados e métricas coletadas pelo Prometheus.

  Ps: Adicione o datasource do prometheus

6. Acesse o Grafana em seu navegador através do endereço `http://localhost:3000`.

7. Faça login no Grafana usando as credenciais padrão (usuário: admin, senha: admin).

8. No Grafana, importe o painel de controle fornecido no diretório `grafana-dashboard/`.

9. Após a importação, você poderá visualizar as métricas de sentimentos e acompanhar a repercussão da marca no Twitter.

   ![image](https://github.com/GaberRB/tweetMetricsComprehend/assets/28874479/58d109f7-3514-4d91-8da8-c72135c3be03)




## Contribuição
Contribuições são bem-vindas! Se você quiser contribuir para o projeto, sinta-se à vontade para abrir uma issue ou enviar um pull request.





