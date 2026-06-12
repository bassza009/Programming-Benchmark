package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"log"

	"github.com/gofiber/fiber/v2"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var db *gorm.DB

// Models
type User struct {
	ID    int    `gorm:"primaryKey;autoIncrement"`
	Name  string `gorm:"size:100"`
	Email string `gorm:"size:100;unique"`
}

type Profile struct {
	ID     int `gorm:"primaryKey;autoIncrement"`
	UserID int
	Bio    string `gorm:"size:255"`
	Phone  string `gorm:"size:20"`
}

type Order struct {
	ID          int `gorm:"primaryKey;autoIncrement"`
	UserID      int
	TotalAmount float64 `gorm:"type:decimal(10,2)"`
}

type OrderItem struct {
	ID          int `gorm:"primaryKey;autoIncrement"`
	OrderID     int
	ProductName string  `gorm:"size:100"`
	Price       float64 `gorm:"type:decimal(10,2)"`
}

func getRandHex() string {
	bytes := make([]byte, 4)
	rand.Read(bytes)
	return hex.EncodeToString(bytes)
}

func main() {
	dsn := "admin:secret@tcp(127.0.0.1:3306)/benchmark_db?charset=utf8mb4&parseTime=True&loc=Local"
	var err error
	db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{
		SkipDefaultTransaction: true, // เพิ่มความเร็วให้ GORM
	})
	if err != nil {
		log.Fatal(err)
	}

	sqlDB, _ := db.DB()
	sqlDB.SetMaxOpenConns(10)
	sqlDB.SetMaxIdleConns(10)

	app := fiber.New(fiber.Config{DisableStartupMessage: true})

	app.Post("/orm/post/1table", func(c *fiber.Ctx) error {
		randID := getRandHex()
		user := User{Name: "User_" + randID, Email: "test_" + randID + "@example.com"}
		if err := db.Create(&user).Error; err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"user_id": user.ID})
	})

	app.Post("/orm/post/2table", func(c *fiber.Ctx) error {
		randID := getRandHex()
		user := User{Name: "User_" + randID, Email: "test_" + randID + "@example.com"}

		err := db.Transaction(func(tx *gorm.DB) error {
			if err := tx.Create(&user).Error; err != nil {
				return err
			}
			profile := Profile{UserID: user.ID, Bio: fmt.Sprintf("Bio for user %d", user.ID), Phone: "555-" + randID}
			return tx.Create(&profile).Error
		})

		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"user_id": user.ID})
	})

	app.Post("/orm/post/3table", func(c *fiber.Ctx) error {
		randID := getRandHex()
		user := User{Name: "User_" + randID, Email: "test_" + randID + "@example.com"}

		err := db.Transaction(func(tx *gorm.DB) error {
			if err := tx.Create(&user).Error; err != nil {
				return err
			}
			profile := Profile{UserID: user.ID, Bio: fmt.Sprintf("Bio for user %d", user.ID), Phone: "555-" + randID}
			if err := tx.Create(&profile).Error; err != nil {
				return err
			}
			order := Order{UserID: user.ID, TotalAmount: 100.00}
			return tx.Create(&order).Error
		})

		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"user_id": user.ID})
	})

	app.Post("/orm/post/4table", func(c *fiber.Ctx) error {
		randID := getRandHex()
		user := User{Name: "User_" + randID, Email: "test_" + randID + "@example.com"}

		err := db.Transaction(func(tx *gorm.DB) error {
			if err := tx.Create(&user).Error; err != nil {
				return err
			}
			profile := Profile{UserID: user.ID, Bio: fmt.Sprintf("Bio for user %d", user.ID), Phone: "555-" + randID}
			if err := tx.Create(&profile).Error; err != nil {
				return err
			}
			order := Order{UserID: user.ID, TotalAmount: 100.00}
			if err := tx.Create(&order).Error; err != nil {
				return err
			}

			items := []OrderItem{
				{OrderID: order.ID, ProductName: "Product_" + randID + "_1", Price: 25.00},
				{OrderID: order.ID, ProductName: "Product_" + randID + "_2", Price: 75.00},
			}
			return tx.Create(&items).Error
		})

		if err != nil {
			return c.Status(500).JSON(fiber.Map{"error": err.Error()})
		}
		return c.Status(201).JSON(fiber.Map{"user_id": user.ID})
	})

	app.Listen(":8004")
}
