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
		`CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100))`,
		`CREATE TABLE IF NOT EXISTS profiles (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, age INT, address VARCHAR(255))`,
		`CREATE TABLE IF NOT EXISTS orders (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, total_amount DECIMAL(10, 2))`,
		`CREATE TABLE IF NOT EXISTS order_items (id INT AUTO_INCREMENT PRIMARY KEY, order_id INT, product_name VARCHAR(100), price DECIMAL(10, 2))`,
	} {
		if _, err := db.Exec(stmt); err != nil {
			return err
		}
	}

	// Check if data exists and populate if empty
	var count int
	db.QueryRow("SELECT COUNT(*) FROM users").Scan(&count)
	if count == 0 {
		insertMockData()
	}

	return nil
}

func insertMockData() {
	fmt.Println("⏳ [Go] กำลังสร้างข้อมูลจำลอง 35,000 แถว (รอสักครู่นะครับ)...")
	tx, err := db.Begin()
	if err != nil {
		panic(err)
	}
	for i := 1; i <= 10000; i++ {
		name := fmt.Sprintf("User%d", i)
		email := fmt.Sprintf("user%d@example.com", i)
		address := fmt.Sprintf("Address %d", i)

		tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", name, email)
		tx.Exec("INSERT INTO profiles (user_id, age, address) VALUES (?, ?, ?)", i, 20+i%50, address)
		tx.Exec("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", i, 100.0+float64(i))

		if i%10 == 0 {
			for j := 0; j < 5; j++ {
				prodName := fmt.Sprintf("Product%d", j)
				tx.Exec("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)", i, prodName, 10.0+float64(j))
			}
		}
	}
	tx.Commit()
	fmt.Println("[Go] สร้างข้อมูลจำลองเสร็จสิ้น!")
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

	app.Get("/raw/1table", func(c *fiber.Ctx) error {
		rows, err := db.Query("SELECT * FROM users LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		var results []map[string]interface{}
		for rows.Next() {
			var id int
			var name, email string
			if err := rows.Scan(&id, &name, &email); err != nil {
				return c.Status(500).JSON(fiber.Map{"error": err.Error()})
			}
			results = append(results, map[string]interface{}{"id": id, "name": name, "email": email})
		}
		return c.JSON(results)
	})

	app.Get("/raw/2join", func(c *fiber.Ctx) error {
		rows, err := db.Query("SELECT u.name, p.age FROM users u JOIN profiles p ON u.id = p.user_id LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		var results []map[string]interface{}
		for rows.Next() {
			var name string
			var age int
			if err := rows.Scan(&name, &age); err != nil {
				return c.Status(500).JSON(fiber.Map{"error": err.Error()})
			}
			results = append(results, map[string]interface{}{"name": name, "age": age})
		}
		return c.JSON(results)
	})

	app.Get("/raw/3join", func(c *fiber.Ctx) error {
		rows, err := db.Query("SELECT u.name, p.age, o.total_amount FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		var results []map[string]interface{}
		for rows.Next() {
			var name string
			var age int
			var total float64
			if err := rows.Scan(&name, &age, &total); err != nil {
				return c.Status(500).JSON(fiber.Map{"error": err.Error()})
			}
			results = append(results, map[string]interface{}{"name": name, "age": age, "total_amount": total})
		}
		return c.JSON(results)
	})

	app.Get("/raw/4join", func(c *fiber.Ctx) error {
		rows, err := db.Query("SELECT u.name, p.age, o.total_amount, oi.product_name FROM users u JOIN profiles p ON u.id = p.user_id JOIN orders o ON u.id = o.user_id JOIN order_items oi ON o.id = oi.order_id LIMIT 100")
		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		defer rows.Close()

		var results []map[string]interface{}
		for rows.Next() {
			var name, productName string
			var age int
			var total float64
			if err := rows.Scan(&name, &age, &total, &productName); err != nil {
				return c.Status(500).JSON(fiber.Map{"error": err.Error()})
			}
			results = append(results, map[string]interface{}{"name": name, "age": age, "total_amount": total, "product_name": productName})
		}
		return c.JSON(results)
	})

	// 💡 เพิ่มข้อความยืนยันเมื่อเซิร์ฟเวอร์เปิดสำเร็จ
	fmt.Println("Go Server running port 8004!")
	app.Listen(":8004")
}
