package main

import (
	"database/sql"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql"
)

var db *sql.DB

func initDB() error {
	dbHost := os.Getenv("DB_HOST")
	if dbHost == "" {
		dbHost = "127.0.0.1"
	}
	dbPort := os.Getenv("DB_PORT")
	if dbPort == "" {
		dbPort = "3306"
	}
	dbUser := os.Getenv("DB_USER")
	if dbUser == "" {
		dbUser = "admin"
	}
	dbPass := os.Getenv("DB_PASS")
	if dbPass == "" {
		dbPass = "secret"
	}
	dbName := os.Getenv("DB_NAME")
	if dbName == "" {
		dbName = "benchmark_db"
	}

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?parseTime=true", dbUser, dbPass, dbHost, dbPort, dbName)
	var err error
	db, err = sql.Open("mysql", dsn)
	if err != nil {
		return err
	}
	db.SetMaxOpenConns(100)
	db.SetMaxIdleConns(50)
	return db.Ping()
}

func main() {
	if err := initDB(); err != nil {
		log.Fatalf("Database error: %v", err)
	}

	gin.SetMode(gin.ReleaseMode)
	r := gin.New()

	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "success", "language": "Go", "framework": "Gin", "port": 8014})
	})

	r.GET("/raw/1table", func(c *gin.Context) {
		rows, err := db.Query("SELECT id, name, email FROM users LIMIT 100")
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer rows.Close()

		type User struct {
			ID    int    `json:"id"`
			Name  string `json:"name"`
			Email string `json:"email"`
		}
		var users []User
		for rows.Next() {
			var u User
			if err := rows.Scan(&u.ID, &u.Name, &u.Email); err == nil {
				users = append(users, u)
			}
		}
		c.JSON(http.StatusOK, users)
	})

	r.POST("/raw/post/1table", func(c *gin.Context) {
		randomID := rand.Intn(1000000)
		email := fmt.Sprintf("gin_%d_%d@example.com", randomID, time.Now().UnixNano())
		res, err := db.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%d", randomID), email)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		id, _ := res.LastInsertId()
		c.JSON(http.StatusCreated, gin.H{"user_id": id})
	})

	log.Fatal(r.Run(":8014"))
}
