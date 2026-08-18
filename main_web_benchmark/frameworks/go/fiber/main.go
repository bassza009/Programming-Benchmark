package main

import (
	"database/sql"
	"fmt"
	"log"
	"math/rand"
	"os"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/gofiber/fiber/v2"
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
		log.Fatalf("Database connection failed: %v", err)
	}

	app := fiber.New(fiber.Config{
		DisableStartupMessage: true,
	})

	// ==================== Health Check ====================
	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "success", "language": "Go", "framework": "Fiber", "port": 8004})
	})

	// ==================== GET (Read) Endpoints ====================
	app.Get("/raw/1table", func(c *fiber.Ctx) error {
		rows, err := db.Query("SELECT id, name, email FROM users LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
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
		return c.JSON(users)
	})

	app.Get("/raw/2join", func(c *fiber.Ctx) error {
		rows, err := db.Query("SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		type Result struct {
			Name string `json:"name"`
			Age  int    `json:"age"`
		}
		var results []Result
		for rows.Next() {
			var r Result
			if err := rows.Scan(&r.Name, &r.Age); err == nil {
				results = append(results, r)
			}
		}
		return c.JSON(results)
	})

	app.Get("/raw/3join", func(c *fiber.Ctx) error {
		rows, err := db.Query("SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		type Result struct {
			Name        string  `json:"name"`
			Age         int     `json:"age"`
			TotalAmount float64 `json:"total_amount"`
		}
		var results []Result
		for rows.Next() {
			var r Result
			if err := rows.Scan(&r.Name, &r.Age, &r.TotalAmount); err == nil {
				results = append(results, r)
			}
		}
		return c.JSON(results)
	})

	app.Get("/raw/4join", func(c *fiber.Ctx) error {
		rows, err := db.Query("SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		type Result struct {
			Name        string  `json:"name"`
			Age         int     `json:"age"`
			TotalAmount float64 `json:"total_amount"`
			ProductName string  `json:"product_name"`
		}
		var results []Result
		for rows.Next() {
			var r Result
			if err := rows.Scan(&r.Name, &r.Age, &r.TotalAmount, &r.ProductName); err == nil {
				results = append(results, r)
			}
		}
		return c.JSON(results)
	})

	// ==================== POST (Write / Transaction) Endpoints ====================
	app.Post("/raw/post/1table", func(c *fiber.Ctx) error {
		randomID := rand.Intn(1000000)
		email := fmt.Sprintf("go_%d_%d@example.com", randomID, time.Now().UnixNano())
		res, err := db.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%d", randomID), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		id, _ := res.LastInsertId()
		return c.Status(201).JSON(fiber.Map{"user_id": id})
	})

	app.Post("/raw/post/2table", func(c *fiber.Ctx) error {
		tx, err := db.Begin()
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer tx.Rollback()

		randomID := rand.Intn(1000000)
		email := fmt.Sprintf("go_%d_%d@example.com", randomID, time.Now().UnixNano())
		res, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%d", randomID), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		userID, _ := res.LastInsertId()

		_, err = tx.Exec("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)",
			userID, 25, "123 Main St", fmt.Sprintf("Bio %d", userID), fmt.Sprintf("555-%d", randomID))
		if err != nil {
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

		randomID := rand.Intn(1000000)
		email := fmt.Sprintf("go_%d_%d@example.com", randomID, time.Now().UnixNano())
		res, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%d", randomID), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		userID, _ := res.LastInsertId()

		_, err = tx.Exec("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)",
			userID, 25, "123 Main St", fmt.Sprintf("Bio %d", userID), fmt.Sprintf("555-%d", randomID))
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		_, err = tx.Exec("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", userID, 100.00)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

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

		randomID := rand.Intn(1000000)
		email := fmt.Sprintf("go_%d_%d@example.com", randomID, time.Now().UnixNano())
		res, err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User_%d", randomID), email)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		userID, _ := res.LastInsertId()

		_, err = tx.Exec("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)",
			userID, 25, "123 Main St", fmt.Sprintf("Bio %d", userID), fmt.Sprintf("555-%d", randomID))
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		resOrder, err := tx.Exec("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", userID, 100.00)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		orderID, _ := resOrder.LastInsertId()

		_, err = tx.Exec("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)",
			orderID, fmt.Sprintf("Item1_%d", randomID), 25.00)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		_, err = tx.Exec("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)",
			orderID, fmt.Sprintf("Item2_%d", randomID), 75.00)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		if err := tx.Commit(); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"user_id": userID})
	})

	log.Fatal(app.Listen(":8004"))
}
