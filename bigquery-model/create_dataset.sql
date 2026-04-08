-- Crear dataset (schema)
CREATE SCHEMA IF NOT EXISTS ecommerce_dataset
OPTIONS(location="US");

-- Crear tabla orders
CREATE TABLE IF NOT EXISTS ecommerce_dataset.orders (
  order_id INT64,
  user_id INT64,
  product STRING,
  price NUMERIC
);

-- Crear tabla users
CREATE TABLE IF NOT EXISTS ecommerce_dataset.users (
  user_id INT64,
  name STRING,
  email STRING
);

-- Insertar datos en users
INSERT INTO ecommerce_dataset.users (user_id, name, email)
VALUES
  (1, 'Javier Valdes', 'jvaldes@gmail.com'),
  (2, 'Arturo Coello', 'acoello@gmail.com'),
  (3, 'Agustin Tapia', 'atapia@gmail.co,');

-- Insertar datos en orders
INSERT INTO ecommerce_dataset.orders (order_id, user_id, product, price)
VALUES
  (101, 1, 'Computador', 1200.50),
  (102, 1, 'Mouse', 25.75),
  (103, 2, 'Teclado', 45.00),
  (104, 3, 'Monitor', 300.00),
  (105, 2, 'Cable HDMI', 10.00);

-- Crear vista
CREATE OR REPLACE VIEW ecommerce_dataset.denormalized_view AS
SELECT 
  o.user_id,
  o.order_id,
  o.product,
  o.price,
  u.name,
  u.email
FROM ecommerce_dataset.orders o
JOIN ecommerce_dataset.users u
ON o.user_id = u.user_id;