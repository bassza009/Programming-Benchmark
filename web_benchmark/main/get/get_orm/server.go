package main

import (
	"fmt"
	"log"
	"os"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"

	"github.com/gofiber/fiber/v2"
)

type User struct {
	ID      int32  `gorm:"primaryKey" json:"id"`
	Name    string `json:"name"`
	Email   string `json:"email"`
	Profile Profile
	Orders  []Order
}

type Profile struct {
	ID      int32  `gorm:"primaryKey" json:"-"`
	UserID  int32  `json:"-"`
	Age     int    `json:"age"`
	Address string `json:"address"`
}

type Order struct {
	ID          int32       `gorm:"primaryKey" json:"-"`
	UserID      int32       `json:"-"`
	TotalAmount float64     `json:"total_amount"`
	OrderItems  []OrderItem `json:"-"`
}

type OrderItem struct {
	ID          int32   `gorm:"primaryKey" json:"-"`
	OrderID     int32   `json:"-"`
	ProductName string  `json:"product_name"`
	Price       float64 `json:"price"`
}

type Join2Row struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

type Join3Row struct {
	Name        string  `json:"name"`
	Age         int     `json:"age"`
	TotalAmount float64 `json:"total_amount"`
}

type Join4Row struct {
	Name        string  `json:"name"`
	Age         int     `json:"age"`
	TotalAmount float64 `json:"total_amount"`
	ProductName string  `json:"product_name"`
}

var db *gorm.DB

func initDB() {
	dsn := "admin:secret@tcp(127.0.0.1:3306)/benchmark_db?charset=utf8mb4&parseTime=True&loc=Local"
	var err error
	db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		panic(err)
	}

	sqlDB, err := db.DB()
	if err != nil {
		panic(err)
	}

	sqlDB.SetMaxOpenConns(100)
	sqlDB.SetMaxIdleConns(50)

	if err := db.AutoMigrate(&User{}, &Profile{}, &Order{}, &OrderItem{}); err != nil {
		panic(err)
	}

	var count int64
	db.Model(&User{}).Count(&count)
	if count == 0 {
		insertMockData()
	}
}

func insertMockData() {
	log.Println("Initializing ORM benchmark data...")
	tx := db.Begin()
	for i := 1; i <= 10000; i++ {
		if err := tx.Exec("INSERT INTO users (name, email) VALUES (?, ?)", fmt.Sprintf("User%d", i), fmt.Sprintf("user%d@example.com", i)).Error; err != nil {
			tx.Rollback()
			panic(err)
		}
		if err := tx.Exec("INSERT INTO profiles (user_id, age, address) VALUES (?, ?, ?)", i, 20+(i%50), fmt.Sprintf("Address %d", i)).Error; err != nil {
			tx.Rollback()
			panic(err)
		}
		if err := tx.Exec("INSERT INTO orders (user_id, total_amount) VALUES (?, ?)", i, 100.0+float64(i)).Error; err != nil {
			tx.Rollback()
			panic(err)
		}

		if i%10 == 0 {
			for j := 0; j < 5; j++ {
				if err := tx.Exec("INSERT INTO order_items (order_id, product_name, price) VALUES (?, ?, ?)", i, fmt.Sprintf("Product%d", j), 10.0+float64(j)).Error; err != nil {
					tx.Rollback()
					panic(err)
				}
			}
		}
	}
	tx.Commit()
}

func main() {
	log.SetOutput(os.Stdout)
	initDB()

	app := fiber.New(fiber.Config{DisableStartupMessage: true})

	app.Get("/", func(c *fiber.Ctx) error {
		return c.JSON(fiber.Map{"status": "success", "message": "Hello Benchmark"})
	})

	app.Get("/orm/1table", func(c *fiber.Ctx) error {
		var users []User
		db.Limit(100).Find(&users)
		return c.JSON(users)
	})

	app.Get("/orm/2join", func(c *fiber.Ctx) error {
		var rows []Join2Row
		db.Table("users").Select("users.name AS name, profiles.age AS age").Joins("JOIN profiles ON users.id = profiles.user_id").Limit(100).Scan(&rows)
		return c.JSON(rows)
	})

	app.Get("/orm/3join", func(c *fiber.Ctx) error {
		var rows []Join3Row
		db.Table("users").Select("users.name AS name, profiles.age AS age, orders.total_amount AS total_amount").Joins("JOIN profiles ON users.id = profiles.user_id").Joins("JOIN orders ON users.id = orders.user_id").Limit(100).Scan(&rows)
		return c.JSON(rows)
	})

	app.Get("/orm/4join", func(c *fiber.Ctx) error {
		var rows []Join4Row
		db.Table("users").Select("users.name AS name, profiles.age AS age, orders.total_amount AS total_amount, order_items.product_name AS product_name").Joins("JOIN profiles ON users.id = profiles.user_id").Joins("JOIN orders ON users.id = orders.user_id").Joins("JOIN order_items ON orders.id = order_items.order_id").Limit(100).Scan(&rows)
		return c.JSON(rows)
	})

	app.Listen(":8004")
}
