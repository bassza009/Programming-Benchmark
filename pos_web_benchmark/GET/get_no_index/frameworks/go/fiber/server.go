package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/jackc/pgx/v5/pgxpool"
)

var pool *pgxpool.Pool

func initDB() error {
	dbHost := os.Getenv("DB_HOST")
	if dbHost == "" {
		dbHost = "127.0.0.1"
	}
	dbPort := os.Getenv("DB_PORT")
	if dbPort == "" {
		dbPort = "5432"
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

	connStr := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable&pool_max_conns=200&pool_min_conns=20",
		dbUser, dbPass, dbHost, dbPort, dbName)

	config, err := pgxpool.ParseConfig(connStr)
	if err != nil {
		return err
	}
	config.MaxConns = 200
	config.MinConns = 20
	config.MaxConnLifetime = 30 * time.Minute

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	pool, err = pgxpool.NewWithConfig(ctx, config)
	if err != nil {
		return err
	}

	return pool.Ping(ctx)
}

func main() {
	if err := initDB(); err != nil {
		log.Fatalf("Failed to connect to PostgreSQL: %v", err)
	}
	defer pool.Close()

	app := fiber.New(fiber.Config{
		DisableStartupMessage: true,
	})

	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "success", "message": "Go Fiber PostgreSQL GET Benchmark"})
	})

	app.Get("/raw/1table", func(c *fiber.Ctx) error {
		rows, err := pool.Query(context.Background(), "SELECT id, name, email, phone, city, created_at FROM customer LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		type Customer struct {
			ID        int       `json:"id"`
			Name      string    `json:"name"`
			Email     string    `json:"email"`
			Phone     string    `json:"phone"`
			City      string    `json:"city"`
			CreatedAt time.Time `json:"created_at"`
		}
		var list []Customer
		for rows.Next() {
			var item Customer
			if err := rows.Scan(&item.ID, &item.Name, &item.Email, &item.Phone, &item.City, &item.CreatedAt); err == nil {
				list = append(list, item)
			}
		}
		return c.JSON(list)
	})

	app.Get("/raw/2join", func(c *fiber.Ctx) error {
		rows, err := pool.Query(context.Background(), `
			SELECT o.id, c.name, o.quantity, o.total_amount, o.order_date
			FROM orders o
			JOIN customer c ON o.customer_id = c.id
			LIMIT 100
		`)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		type Result struct {
			ID          int64     `json:"id"`
			Name        string    `json:"name"`
			Quantity    int       `json:"quantity"`
			TotalAmount float64   `json:"total_amount"`
			OrderDate   time.Time `json:"order_date"`
		}
		var list []Result
		for rows.Next() {
			var r Result
			if err := rows.Scan(&r.ID, &r.Name, &r.Quantity, &r.TotalAmount, &r.OrderDate); err == nil {
				list = append(list, r)
			}
		}
		return c.JSON(list)
	})

	app.Get("/raw/3join", func(c *fiber.Ctx) error {
		rows, err := pool.Query(context.Background(), `
			SELECT o.id, c.name, p.name, o.quantity, o.total_amount
			FROM orders o
			JOIN customer c ON o.customer_id = c.id
			JOIN product p ON o.product_id = p.id
			LIMIT 100
		`)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		type Result struct {
			ID          int64   `json:"id"`
			Name        string  `json:"name"`
			ProductName string  `json:"product_name"`
			Quantity    int     `json:"quantity"`
			TotalAmount float64 `json:"total_amount"`
		}
		var list []Result
		for rows.Next() {
			var r Result
			if err := rows.Scan(&r.ID, &r.Name, &r.ProductName, &r.Quantity, &r.TotalAmount); err == nil {
				list = append(list, r)
			}
		}
		return c.JSON(list)
	})

	app.Get("/raw/4join", func(c *fiber.Ctx) error {
		rows, err := pool.Query(context.Background(), `
			SELECT o.id, c.name, p.name, f.name, o.quantity, o.total_amount
			FROM orders o
			JOIN customer c ON o.customer_id = c.id
			JOIN product p ON o.product_id = p.id
			JOIN factory f ON p.factory_id = f.id
			LIMIT 100
		`)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		type Result struct {
			ID          int64   `json:"id"`
			Name        string  `json:"name"`
			ProductName string  `json:"product_name"`
			FactoryName string  `json:"factory_name"`
			Quantity    int     `json:"quantity"`
			TotalAmount float64 `json:"total_amount"`
		}
		var list []Result
		for rows.Next() {
			var r Result
			if err := rows.Scan(&r.ID, &r.Name, &r.ProductName, &r.FactoryName, &r.Quantity, &r.TotalAmount); err == nil {
				list = append(list, r)
			}
		}
		return c.JSON(list)
	})

	log.Fatal(app.Listen(":8004"))
}
