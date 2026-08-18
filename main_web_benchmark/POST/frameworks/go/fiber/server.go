package main

import (
	"database/sql"
	"fmt"
	"log"
	"math/rand"
	"os"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gofiber/fiber/v2"
)

var db *sql.DB
var once sync.Once

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

	if err := db.Ping(); err != nil {
		return err
	}

	return initSchema()
}

func initSchema() error {
	schemas := []string{
		`CREATE TABLE IF NOT EXISTS users (
			id INT AUTO_INCREMENT PRIMARY KEY,
			name VARCHAR(100),
			email VARCHAR(100) UNIQUE
		);`,
		`CREATE TABLE IF NOT EXISTS profiles (
			id INT AUTO_INCREMENT PRIMARY KEY,
			user_id INT,
			age INT,
			bio VARCHAR(255),
			phone VARCHAR(20),
			address VARCHAR(255)
		);`,
		`CREATE TABLE IF NOT EXISTS orders (
			id INT AUTO_INCREMENT PRIMARY KEY,
			user_id INT,
			total_amount DECIMAL(10, 2)
		);`,
		`CREATE TABLE IF NOT EXISTS order_items (
			id INT AUTO_INCREMENT PRIMARY KEY,
			order_id INT,
			product_name VARCHAR(100),
			price DECIMAL(10, 2)
		);`,
	}

	for _, s := range schemas {
		if _, err := db.Exec(s); err != nil {
			return err
		}
	}

	return nil
}

func randomString(n int) string {
	var letters = []rune("abcdefghijklmnopqrstuvwxyz0123456789")
	b := make([]rune, n)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return string(b)
}

func main() {
	rand.Seed(time.Now().UnixNano())
	if err := initDB(); err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	app := fiber.New(fiber.Config{
		DisableStartupMessage: true,
	})

	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "success", "message": "Go Fiber POST Benchmark"})
	})

	app.Post("/raw/post/1table", func(c *fiber.Ctx) error {
		randID := randomString(8)
		email := fmt.Sprintf("go_test_%s_%d@example.com", randID, time.Now().UnixNano())
		res, err := db.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%s", randID), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		userID, _ := res.LastInsertId()
		return c.Status(201).JSON(fiber.Map{"user_id": userID})
	})

	app.Post("/raw/post/2table", func(c *fiber.Ctx) error {
		tx, err := db.Begin()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer tx.Rollback()

		randID := randomString(8)
		email := fmt.Sprintf("go_test_%s_%d@example.com", randID, time.Now().UnixNano())
		res, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%s", randID), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		userID, _ := res.LastInsertId()

		if _, err := tx.Exec("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)", userID, 25, "123 St", fmt.Sprintf("Bio %d", userID), fmt.Sprintf("555-%s", randID)); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		if err := tx.Commit(); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"user_id": userID})
	})

	app.Post("/raw/post/3table", func(c *fiber.Ctx) error {
		tx, err := db.Begin()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer tx.Rollback()

		randID := randomString(8)
		email := fmt.Sprintf("go_test_%s_%d@example.com", randID, time.Now().UnixNano())
		res, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%s", randID), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		userID, _ := res.LastInsertId()

		tx.Exec("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)", userID, 25, "123 St", fmt.Sprintf("Bio %d", userID), fmt.Sprintf("555-%s", randID))
		tx.Exec("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", userID, 100.00)

		if err := tx.Commit(); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"user_id": userID})
	})

	app.Post("/raw/post/4table", func(c *fiber.Ctx) error {
		tx, err := db.Begin()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer tx.Rollback()

		randID := randomString(8)
		email := fmt.Sprintf("go_test_%s_%d@example.com", randID, time.Now().UnixNano())
		res, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%s", randID), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		userID, _ := res.LastInsertId()

		tx.Exec("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)", userID, 25, "123 St", fmt.Sprintf("Bio %d", userID), fmt.Sprintf("555-%s", randID))
		resOrd, _ := tx.Exec("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", userID, 100.00)
		orderID, _ := resOrd.LastInsertId()

		tx.Exec("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)", orderID, fmt.Sprintf("Prod1_%s", randID), 25.00)
		tx.Exec("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)", orderID, fmt.Sprintf("Prod2_%s", randID), 75.00)

		if err := tx.Commit(); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"user_id": userID})
	})

	log.Fatal(app.Listen(":8004"))
}
