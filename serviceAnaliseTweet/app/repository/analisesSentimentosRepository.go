package repository

import (
	"database/sql"
	"fmt"
	"os"

	_ "github.com/go-sql-driver/mysql"
)

type Message struct {
	Sentiment *string
	Tweet     string
	Mixed     *float64
	Negative  *float64
	Neutral   *float64
	Positive  *float64
}

func SaveMessageToMySQL(message *Message) error {
	dbUser := os.Getenv("DB_USER")
	dbPass := os.Getenv("DB_PASSWORD")
	dbHost := os.Getenv("DB_URL")
	dbPort := os.Getenv("DB_PORT")
	dbName := os.Getenv("DB_DATABASE")

	connectionString := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", dbUser, dbPass, dbHost, dbPort, dbName)
	fmt.Println("string de conexao = " + connectionString)
	db, err := sql.Open("mysql", connectionString)
	if err != nil {
		return err
	}
	defer db.Close()

	stmt, err := db.Prepare("INSERT INTO analises_sentimentos (sentiment, tweet, mixed, negative, neutral, positive) VALUES (?, ?, ?, ?, ?, ?)")
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.Exec(message.Sentiment, message.Tweet, message.Mixed, message.Negative, message.Neutral, message.Positive)
	if err != nil {
		return err
	}

	return nil
}
