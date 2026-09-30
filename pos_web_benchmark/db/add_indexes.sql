-- Secondary Indexes for PostgreSQL Benchmark Tables
-- Creates indexes on all 4 tables for the With-Index suite and general production querying

CREATE INDEX IF NOT EXISTS idx_factory_name ON factory (name);
CREATE INDEX IF NOT EXISTS idx_factory_country ON factory (country);

CREATE INDEX IF NOT EXISTS idx_product_factory_id ON product (factory_id);
CREATE INDEX IF NOT EXISTS idx_product_category ON product (category);
CREATE INDEX IF NOT EXISTS idx_product_price ON product (price);

CREATE INDEX IF NOT EXISTS idx_customer_email ON customer (email);
CREATE INDEX IF NOT EXISTS idx_customer_city ON customer (city);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders (customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_product_id ON orders (product_id);
CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders (order_date);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders (status);

VACUUM ANALYZE factory;
VACUUM ANALYZE product;
VACUUM ANALYZE customer;
VACUUM ANALYZE orders;
