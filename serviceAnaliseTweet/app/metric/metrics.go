package metric

import (
	"fmt"
	"io/ioutil"
	"net/http"

	"app/awsClient"

	"github.com/prometheus/client_golang/prometheus"
)

var (
	sentimentCount = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "sentiment_count",
			Help: "Number of sentiment analysis results",
		},
		[]string{"sentiment"},
	)
)

func init() {
	// Registrar a métrica
	prometheus.MustRegister(sentimentCount)
}

func GetMetricMessage(message string) {

	output, err := awsClient.AnaliseSentimento(message)
	if err != nil {
		fmt.Println("Erro ano analisar sentimento: ", err)
		return
	}

	fmt.Print(output)

	sentimentCount.WithLabelValues(*output.Sentiment).Inc()

}

func GetMetricApi() {

	http.HandleFunc("/analyze", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}

		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("Erro ao ler o corpo da solicitação"))
			return
		}

		texto := string(body)

		output, err := awsClient.AnaliseSentimento(texto)
		if err != nil {
			w.WriteHeader(http.StatusInternalServerError)
			w.Write([]byte("Erro ao analisar sentimento"))
			return
		}

		fmt.Print(output)

		sentimentCount.WithLabelValues(*output.Sentiment).Inc()

		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Sentimento analisado e métricas incrementadas"))
	})

}
