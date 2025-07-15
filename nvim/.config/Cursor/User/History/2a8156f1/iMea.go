package router

import (
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

func NewRouter() http.Handler {
	r := chi.NewRouter()

	// Middleware
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	// Serve static files
	fileServer := http.FileServer(http.Dir("static"))
	r.Handle("/static/*", http.StripPrefix("/static/", fileServer))

	// Routes
	r.Get("/", handleHome)

	return r
}

func handleHome(w http.ResponseWriter, r *http.Request) {
	// For now, just return a simple message
	w.Write([]byte("Welcome to goDial!"))
}
