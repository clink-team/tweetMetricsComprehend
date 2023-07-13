package kafka

import (
	"app/metric"
	"app/repository"
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/segmentio/kafka-go"
)

func Listen() {
	kafkaURL := os.Getenv("KAFKA_URL")

	config := kafka.ReaderConfig{
		Brokers:        []string{kafkaURL},
		GroupID:        "groupId",
		Topic:          "producer-twitter",
		MinBytes:       10e3, // 10KB
		MaxBytes:       10e6, // 10MB
		MaxWait:        time.Second * 1,
		CommitInterval: time.Second * 1,
	}

	reader := kafka.NewReader(config)
	defer reader.Close()

	for {
		message, err := reader.ReadMessage(context.Background())
		if err != nil {
			fmt.Println("Falha ao ler a mensagem: ", err)
			continue
		}

		fmt.Println("Mensagem recebida: " + string(message.Value))

		resultMessage, errMetric := metric.GetMetricMessage(string(message.Value))
		if errMetric != nil {
			log.Fatal("Erro ao recuperar a mensagem da analise:", errMetric)
		}

		errDb := repository.SaveMessageToMySQL(resultMessage)
		if errDb != nil {
			log.Fatal("Erro ao salvar a mensagem no MySQL:", errDb)
		}

		fmt.Println("Mensagem salva com sucesso no MySQL!")

		err = reader.CommitMessages(context.Background(), message)
		if err != nil {
			fmt.Println("Falha ao marcar a mensagem como consumida: ", err)
		}
	}
}
