-- Database: supply_chain_db

-- DROP DATABASE IF EXISTS supply_chain_db;

CREATE DATABASE supply_chain_db;

CREATE TABLE stg_supply_chain (
    type VARCHAR(50),
    days_for_shipping_real INT,
    days_for_shipment_scheduled INT,
    benefit_per_order FLOAT,
    sales_per_customer FLOAT,
    delivery_status VARCHAR(50),
    late_delivery_risk INT,
    category_id INT,
    category_name VARCHAR(100),
    customer_city VARCHAR(100),
    customer_country VARCHAR(100),
    customer_segment VARCHAR(50),
    department_name VARCHAR(100),
    market VARCHAR(50),
    order_city VARCHAR(100),
    order_country VARCHAR(100),
    order_date_dateorders TIMESTAMP,
    order_id INT,
    order_item_product_price FLOAT,
    order_item_quantity INT,
    sales FLOAT,
    order_region VARCHAR(100),
    order_status VARCHAR(50),
    product_name VARCHAR(255),
    product_price FLOAT,
    shipping_date_dateorders TIMESTAMP,
    shipping_mode VARCHAR(50)
);

SELECT count(*) FROM stg_supply_chain;


SELECT 
    category_name,
    shipping_mode,
    COUNT(*) AS total_late_orders,
    ROUND(AVG(days_for_shipping_real - days_for_shipment_scheduled), 2) AS avg_delay_days
FROM stg_supply_chain
WHERE late_delivery_risk = 1
GROUP BY category_name, shipping_mode
HAVING AVG(days_for_shipping_real - days_for_shipment_scheduled) > 0
ORDER BY avg_delay_days DESC
LIMIT 10;


--The "CEO’s Dashboard" Query
SELECT 
    order_region,
    COUNT(*) AS total_orders,
    ROUND(SUM(benefit_per_order)::numeric, 2) AS total_profit,
    ROUND(AVG(late_delivery_risk) * 100, 2) AS late_delivery_rate_pct,
    -- This calculates profit lost on orders that were late
    ROUND(SUM(CASE WHEN late_delivery_risk = 1 THEN benefit_per_order ELSE 0 END)::numeric, 2) AS profit_at_risk
FROM stg_supply_chain
GROUP BY order_region
ORDER BY profit_at_risk DESC;


--The "Technical Flex" (Window Functions)
SELECT 
    category_name,
    department_name,
    days_for_shipping_real,
    -- The MNC favorite: Window Function
    ROUND(AVG(days_for_shipping_real) OVER(PARTITION BY department_name), 2) as dept_avg_days,
    (days_for_shipping_real - AVG(days_for_shipping_real) OVER(PARTITION BY department_name)) as variance
FROM stg_supply_chain
WHERE late_delivery_risk = 1
ORDER BY variance DESC
LIMIT 15;

--