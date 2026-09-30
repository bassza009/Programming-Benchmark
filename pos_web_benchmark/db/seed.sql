-- High-Performance PostgreSQL Seeding Script
-- Total Volume: 11,110,000 Records
-- Target Tables:
--   1. factory: 10,000 records
--   2. product: 100,000 records
--   3. customer: 1,000,000 records
--   4. orders: 10,000,000 records

-- Disable synchronous commit during bulk loading for speed
SET synchronous_commit = OFF;

---------------------------------------------------------
-- 1. Seed Factory (10,000 records)
---------------------------------------------------------
INSERT INTO factory (id, name, location, country, created_at)
SELECT 
    i AS id,
    'Factory ' || i AS name,
    'Industrial Zone ' || (i % 500) AS location,
    'Country ' || (i % 50) AS country,
    (NOW() - ((i % 1000) || ' hours')::interval) AS created_at
FROM generate_series(1, 10000) AS i;

SELECT setval('factory_id_seq', 10000, true);

---------------------------------------------------------
-- 2. Seed Product (100,000 records)
---------------------------------------------------------
INSERT INTO product (id, factory_id, name, category, price, stock, created_at)
SELECT 
    i AS id,
    1 + (i % 10000) AS factory_id,
    'Product ' || i AS name,
    'Category ' || (i % 100) AS category,
    ROUND((10.0 + (i % 1000) * 0.5)::numeric, 2) AS price,
    10 + (i % 500) AS stock,
    (NOW() - ((i % 2000) || ' hours')::interval) AS created_at
FROM generate_series(1, 100000) AS i;

SELECT setval('product_id_seq', 100000, true);

---------------------------------------------------------
-- 3. Seed Customer (1,000,000 records)
---------------------------------------------------------
INSERT INTO customer (id, name, email, phone, city, created_at)
SELECT 
    i AS id,
    'Customer ' || i AS name,
    'customer' || i || '@example.com' AS email,
    '555-' || LPAD((i % 10000)::text, 4, '0') AS phone,
    'City ' || (i % 200) AS city,
    (NOW() - ((i % 5000) || ' hours')::interval) AS created_at
FROM generate_series(1, 1000000) AS i;

SELECT setval('customer_id_seq', 1000000, true);

---------------------------------------------------------
-- 4. Seed Orders (10,000,000 records in 10 batches of 1M)
---------------------------------------------------------
DO $$
DECLARE
    batch INT;
    start_id BIGINT;
    end_id BIGINT;
BEGIN
    FOR batch IN 0..9 LOOP
        start_id := (batch * 1000000) + 1;
        end_id := (batch + 1) * 1000000;
        RAISE NOTICE 'Inserting Orders batch % / 10 (IDs % to %)...', batch + 1, start_id, end_id;

        INSERT INTO orders (id, customer_id, product_id, quantity, total_amount, status, order_date)
        SELECT 
            i AS id,
            1 + (i % 1000000) AS customer_id,
            1 + (i % 100000) AS product_id,
            1 + (i % 10) AS quantity,
            ROUND((25.0 + (i % 500) * 1.5)::numeric, 2) AS total_amount,
            CASE (i % 4)
                WHEN 0 THEN 'PENDING'
                WHEN 1 THEN 'PROCESSING'
                WHEN 2 THEN 'COMPLETED'
                ELSE 'SHIPPED'
            END AS status,
            (NOW() - ((i % 10000) || ' minutes')::interval) AS order_date
        FROM generate_series(start_id, end_id) AS i;
    END LOOP;
END $$;

SELECT setval('orders_id_seq', 10000000, true);

RESET synchronous_commit;
