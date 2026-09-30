-- Drop Secondary Indexes for GET (No-Index) Suite
-- Preserves Primary Keys (PKs), drops foreign key / join relation indexes

DROP INDEX IF EXISTS idx_orders_customer_id;
DROP INDEX IF EXISTS idx_orders_product_id;
DROP INDEX IF EXISTS idx_orders_order_date;
DROP INDEX IF EXISTS idx_orders_status;

DROP INDEX IF EXISTS idx_product_factory_id;
DROP INDEX IF EXISTS idx_product_category;
DROP INDEX IF EXISTS idx_product_price;

DROP INDEX IF EXISTS idx_customer_email;
DROP INDEX IF EXISTS idx_customer_city;

DROP INDEX IF EXISTS idx_factory_name;
DROP INDEX IF EXISTS idx_factory_country;

VACUUM ANALYZE factory;
VACUUM ANALYZE product;
VACUUM ANALYZE customer;
VACUUM ANALYZE orders;
