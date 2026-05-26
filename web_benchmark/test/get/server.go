package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
)

type Response struct {
	Status    string `json:"status,omitempty"`
	Message   string `json:"message,omitempty"`
	Language  string `json:"language,omitempty"`
	Error     string `json:"error,omitempty"`
	Data      string `json:"data,omitempty"`
	Timestamp int64  `json:"timestamp,omitempty"`
	Value     int    `json:"value,omitempty"`
}

func handleGET(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusMethodNotAllowed)
		json.NewEncoder(w).Encode(Response{Error: "Method Not Allowed"})
		return
	}

	w.Header().Set("Content-Type", "application/json")

	switch r.URL.Path {
	case "/":
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(Response{
			Status:   "ok",
			Message:  "Hello from Go GET Server",
			Language: "Go",
		})
	case "/health":
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(Response{Status: "healthy"})
	case "/api/data":
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(Response{
			Data:      "benchmark_data",
			Timestamp: 1234567890,
			Value:     42,
		})
	default:
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(Response{Error: "Not found"})
	}
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8004"
	}

	_, err := strconv.Atoi(port)
	if err != nil {
		log.Fatal("Invalid PORT:", port)
	}

	http.HandleFunc("/", handleGET)
	http.HandleFunc("/health", handleGET)
	http.HandleFunc("/api/data", handleGET)

	fmt.Fprintf(os.Stderr, "Go GET Server running on port %s\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
