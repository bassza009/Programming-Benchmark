package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"sync"

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
			email VARCHAR(100)
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

	var dummy int
	err := db.QueryRow("SELECT 1 FROM users LIMIT 1").Scan(&dummy)
	if err == sql.ErrNoRows {
		return seedMockData()
	} else if err != nil {
		return err
	}
	return nil
}

func seedMockData() error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	stmtUser, _ := tx.Prepare("INSERT INTO users (name, email) VALUES (?, ?)")
	stmtProf, _ := tx.Prepare("INSERT INTO profiles (user_id, age, address, bio, phone) VALUES (?, ?, ?, ?, ?)")
	stmtOrd, _ := tx.Prepare("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)")
	stmtItem, _ := tx.Prepare("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)")

	for i := 1; i <= 10000; i++ {
		res, err := stmtUser.Exec(fmt.Sprintf("User%d", i), fmt.Sprintf("user%d@example.com", i))
		if err != nil {
			return err
		}
		userID, _ := res.LastInsertId()
		stmtProf.Exec(userID, 20+(i%50), fmt.Sprintf("Address %d", i), fmt.Sprintf("Bio %d", i), fmt.Sprintf("555-%d", i))
		stmtOrd.Exec(userID, 100.0+float64(i))

		if i%10 == 0 {
			for j := 0; j < 5; j++ {
				stmtItem.Exec(userID, fmt.Sprintf("Product%d", j), 10.0+float64(j))
			}
		}
	}

	return tx.Commit()
}

func main() {
	if err := initDB(); err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	app := fiber.New(fiber.Config{
		DisableStartupMessage: true,
	})

	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "success", "message": "Go Fiber GET No-Index Benchmark"})
	})

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

	log.Fatal(app.Listen(":8004"))
}
