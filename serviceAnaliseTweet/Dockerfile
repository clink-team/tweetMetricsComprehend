FROM golang

# Define o diretório de trabalho
WORKDIR /app

# # Copia os arquivos go.mod e go.sum
COPY serviceAnaliseTweet/app/go.mod ./
COPY serviceAnaliseTweet/app/go.sum ./

RUN go clean -modcache

RUN go mod tidy
# Baixa as dependências. As dependências serão armazenadas em cache se os arquivos go.mod e go.sum não forem alterados
RUN go mod download

# Copia o restante do código-fonte
COPY serviceAnaliseTweet/app .

# Compila o aplicativo Go
RUN go build -o /server


# Expose a porta 8080 para o mundo externo
EXPOSE 8080


ENTRYPOINT ["/server"]



