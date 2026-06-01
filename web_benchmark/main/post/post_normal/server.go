package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"sync"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gofiber/fiber/v2"
	"github.com/google/uuid"
)

var db *sql.DB
var once sync.Once

func initDB() error {
	var err error
	db, err = sql.Open("mysql", "admin:secret@tcp(127.0.0.1:3306)/benchmark_db")
	if err != nil {
		return err
	}
	db.SetMaxOpenConns(100)
	db.SetMaxIdleConns(50)

	if err := db.Ping(); err != nil {
		return err
	}

	if err := initSchema(); err != nil {
		return err
	}

	return nil
}

func initSchema() error {
	for _, stmt := range []string{
		`CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100) UNIQUE)`,
		`CREATE TABLE IF NOT EXISTS profiles (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, bio VARCHAR(255), phone VARCHAR(20))`,
		`CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, total_amount DECIMAL(10, 2))`,
		`CREATE TABLE IF NOT EXISTS order_items (id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, product_name VARCHAR(100), price DECIMAL(10, 2))`,
	} {
		if _, err := db.Exec(stmt); err != nil {
			return err
		}
	}
	return nil
}

func main() {
	log.SetOutput(os.NewFile(1, "/dev/null"))

	once.Do(func() {
		if err := initDB(); err != nil {
			panic(err)
		}
	})

	app := fiber.New(fiber.Config{DisableStartupMessage: true})

	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "success", "message": "Hello Benchmark"})
	})

	app.Post("/raw/post/1table", func(c *fiber.Ctx) error {
		randomId := uuid.New().String()[:8]
		email := fmt.Sprintf("test_%s@example.com", randomId)

		result, err := db.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%s", randomId), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		userId, err := result.LastInsertId()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		return c.Status(201).JSON(fiber.Map{"user_id": userId})
	})

	app.Post("/raw/post/2table", func(c *fiber.Ctx) error {
		tx, err := db.Begin()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		randomId := uuid.New().String()[:8]
		email := fmt.Sprintf("test_%s@example.com", randomId)

		result, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%s", randomId), email)
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		userId, err := result.LastInsertId()
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		_, err = tx.Exec("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)",
			userId, fmt.Sprintf("Bio for user %d", userId), fmt.Sprintf("555-%s", randomId))
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		if err := tx.Commit(); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		return c.Status(201).JSON(fiber.Map{"user_id": userId})
	})

	app.Post("/raw/post/3table", func(c *fiber.Ctx) error {
		tx, err := db.Begin()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		randomId := uuid.New().String()[:8]
		email := fmt.Sprintf("test_%s@example.com", randomId)

		result, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%s", randomId), email)
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		userId, err := result.LastInsertId()
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		_, err = tx.Exec("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)",
			userId, fmt.Sprintf("Bio for user %d", userId), fmt.Sprintf("555-%s", randomId))
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		_, err = tx.Exec("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", userId, 100.00)
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		if err := tx.Commit(); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		return c.Status(201).JSON(fiber.Map{"user_id": userId})
	})

	app.Post("/raw/post/4table", func(c *fiber.Ctx) error {
		tx, err := db.Begin()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		randomId := uuid.New().String()[:8]
		email := fmt.Sprintf("test_%s@example.com", randomId)

		result, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%s", randomId), email)
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		userId, err := result.LastInsertId()
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		_, err = tx.Exec("INSERT INTO profiles (user_id, bio, phone) VALUES (?, ?, ?)",
			userId, fmt.Sprintf("Bio for user %d", userId), fmt.Sprintf("555-%s", randomId))
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		orderResult, err := tx.Exec("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", userId, 100.00)
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		orderId, err := orderResult.LastInsertId()
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		_, err = tx.Exec("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)",
			orderId, fmt.Sprintf("Product_%s_1", randomId), 25.00)
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		_, err = tx.Exec("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)",
			orderId, fmt.Sprintf("Product_%s_2", randomId), 75.00)
		if err != nil {
			tx.Rollback()
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		if err := tx.Commit(); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		return c.Status(201).JSON(fiber.Map{"user_id": userId})
	})

	app.Listen(":8004")
}
