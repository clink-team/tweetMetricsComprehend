package main

import (
	"app/kafka"
	"fmt"
	"net/http"

	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func main() {
	fmt.Print("Iniciando o servidor...ss")
	// metric.GetMetric()
	// http.ListenAndServe(":8080", nil)

	http.Handle("/metrics", promhttp.Handler())
	go kafka.Listen()
	http.ListenAndServe(":8080", nil)

}
