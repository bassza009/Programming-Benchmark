package main

import (
	"context"
	"fmt"
	"log"
	"math/rand"
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
		return c.JSON(fiber.Map{"status": "success", "message": "Go Fiber PostgreSQL POST Benchmark"})
	})

	app.Post("/raw/post/1table", func(c *fiber.Ctx) error {
		uid := fmt.Sprintf("%x_%d", rand.Int63(), time.Now().UnixNano())
		email := fmt.Sprintf("go_%s@example.com", uid)
		var customerID int
		err := pool.QueryRow(context.Background(),
			"INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id",
			fmt.Sprintf("Customer_%s", uid), email, "555-GO", "Benchmark City").Scan(&customerID)
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"customer_id": customerID})
	})

	app.Post("/raw/post/2table", func(c *fiber.Ctx) error {
		tx, err := pool.Begin(context.Background())
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer tx.Rollback(context.Background())

		uid := fmt.Sprintf("%x_%d", rand.Int63(), time.Now().UnixNano())
		email := fmt.Sprintf("go_%s@example.com", uid)
		var customerID int
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id",
			fmt.Sprintf("Customer_%s", uid), email, "555-GO", "Benchmark City").Scan(&customerID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		var orderID int64
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id",
			customerID, 1, 2, 150.00, "COMPLETED").Scan(&orderID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		if err := tx.Commit(context.Background()); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		return c.Status(201).JSON(fiber.Map{"customer_id": customerID, "order_id": orderID})
	})

	app.Post("/raw/post/3table", func(c *fiber.Ctx) error {
		tx, err := pool.Begin(context.Background())
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer tx.Rollback(context.Background())

		uid := fmt.Sprintf("%x_%d", rand.Int63(), time.Now().UnixNano())
		email := fmt.Sprintf("go_%s@example.com", uid)
		var customerID int
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id",
			fmt.Sprintf("Customer_%s", uid), email, "555-GO", "Benchmark City").Scan(&customerID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		var productID int
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO product (factory_id, name, category, price, stock) VALUES ($1, $2, $3, $4, $5) RETURNING id",
			1, fmt.Sprintf("Product_%s", uid), "Benchmark Category", 99.99, 100).Scan(&productID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		var orderID int64
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id",
			customerID, productID, 1, 99.99, "COMPLETED").Scan(&orderID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		if err := tx.Commit(context.Background()); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		return c.Status(201).JSON(fiber.Map{"customer_id": customerID, "product_id": productID, "order_id": orderID})
	})

	app.Post("/raw/post/4table", func(c *fiber.Ctx) error {
		tx, err := pool.Begin(context.Background())
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer tx.Rollback(context.Background())

		uid := fmt.Sprintf("%x_%d", rand.Int63(), time.Now().UnixNano())
		email := fmt.Sprintf("go_%s@example.com", uid)

		var factoryID int
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO factory (name, location, country) VALUES ($1, $2, $3) RETURNING id",
			fmt.Sprintf("Factory_%s", uid), "Industrial Estate", "Thailand").Scan(&factoryID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		var productID int
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO product (factory_id, name, category, price, stock) VALUES ($1, $2, $3, $4, $5) RETURNING id",
			factoryID, fmt.Sprintf("Product_%s", uid), "Benchmark Category", 99.99, 100).Scan(&productID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		var customerID int
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO customer (name, email, phone, city) VALUES ($1, $2, $3, $4) RETURNING id",
			fmt.Sprintf("Customer_%s", uid), email, "555-GO", "Benchmark City").Scan(&customerID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		var orderID int64
		if err := tx.QueryRow(context.Background(),
			"INSERT INTO orders (customer_id, product_id, quantity, total_amount, status) VALUES ($1, $2, $3, $4, $5) RETURNING id",
			customerID, productID, 1, 99.99, "COMPLETED").Scan(&orderID); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		if err := tx.Commit(context.Background()); err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}

		return c.Status(201).JSON(fiber.Map{
			"factory_id":  factoryID,
			"product_id":  productID,
			"customer_id": customerID,
			"order_id":    orderID,
		})
	})

	log.Fatal(app.Listen(":8004"))
}
