package main

import (
	"log"
	"net/http"
	"os"

	"goDial/internal/router"
)

func main() {
	r := router.NewRouter()

	// Only show startup message in non-development mode or first startup
	if os.Getenv("GO_ENV") != "development" || os.Getenv("AIR_ENABLED") != "1" {
		log.Println("Starting server on :8081")
	}

	if err := http.ListenAndServe(":8081", r); err != nil {
		log.Fatal(err)
	}
}
