package router

import (
	"fmt"
	"net/http"
	"os"
)

func NewRouter() http.Handler {
	mux := http.NewServeMux()

	// Serve static files
	fs := http.FileServer(http.Dir("static"))
	mux.Handle("/static/", http.StripPrefix("/static/", fs))

	// Live reload endpoint for development
	mux.HandleFunc("/live-reload", handleLiveReload)

	// Routes
	mux.HandleFunc("/", handleHomePage)
	mux.HandleFunc("/stripePage", handleStripePage)

	return mux
}

// handleLiveReload provides server-sent events for live reload functionality
func handleLiveReload(w http.ResponseWriter, r *http.Request) {
	// Only enable in development (when running through Air)
	if os.Getenv("AIR_ENABLED") == "" && os.Getenv("GO_ENV") != "development" {
		http.NotFound(w, r)
		return
	}

	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	// Send a reload message immediately (Air will restart the server when files change)
	fmt.Fprintf(w, "data: reload\n\n")

	// Flush the response
	if flusher, ok := w.(http.Flusher); ok {
		flusher.Flush()
	}
}
