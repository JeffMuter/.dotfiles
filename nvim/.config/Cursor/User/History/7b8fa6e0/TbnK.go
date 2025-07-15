package main

import (
	"log"
	"net/http"

	"goDial/internal/router"
)

func main() {
	r := router.NewRouter()

	log.Println("Starting server on :8081")
	if err := http.ListenAndServe(":8081", r); err != nil {
		log.Fatal(err)
	}
}
