package kafka

import (
	"app/metric"
	"context"
	"fmt"
	"os"
	"time"

	"github.com/segmentio/kafka-go"
)

func Listen() {
	kafkaURL := os.Getenv("KAFKA_URL")

	config := kafka.ReaderConfig{
		Brokers:        []string{kafkaURL},
		GroupID:        "groupId",
		Topic:          "tweets-topico",
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

		metric.GetMetricMessage(string(message.Value))

		err = reader.CommitMessages(context.Background(), message)
		if err != nil {
			fmt.Println("Falha ao marcar a mensagem como consumida: ", err)
		}
	}
}
