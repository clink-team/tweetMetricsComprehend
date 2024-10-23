package awsClient

import (
	"fmt"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/comprehend"
)

func AnaliseSentimento(texto string) (*comprehend.DetectSentimentOutput, error) {
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("ap-northeast-2"),
	})

	if err != nil {
		fmt.Println("Erro ao criar sessão da AWS:", err)
		return nil, err
	}

	comprehendClient := comprehend.New(sess)

	input := &comprehend.DetectSentimentInput{
		Text:         aws.String(texto),
		LanguageCode: aws.String("pt"),
	}

	output, err := comprehendClient.DetectSentiment(input)
	if err != nil {
		fmt.Println("Erro ao analisar sentimento:", err)
		return nil, err
	}

	return output, nil
}
