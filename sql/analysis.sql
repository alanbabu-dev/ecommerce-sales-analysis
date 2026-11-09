
-- =====================================================
-- PROJECT: E-commerce Sales Data Analysis
-- DATABASE: ecommerce_sales
-- TABLE: sales
-- PURPOSE: Analyze sales performance and business trends
-- =====================================================


-- 1. TOTAL REVENUE
-- Business Question:
-- How much revenue did the business generate from delivered orders?

SELECT
    ROUND(
        SUM(quantity * unit_price * (1 - discount))::numeric,
        2
    ) AS total_revenue
FROM sales
WHERE order_status = 'Delivered';



-- =====================================================
-- 2. REVENUE ANALYSIS
-- =====================================================


-- 2.1 REVENUE BY PRODUCT
-- Business Question:
-- Which products generate the most revenue?

SELECT
    product,
    ROUND(
        SUM(quantity * unit_price * (1 - discount))::numeric,
        2
    ) AS total_revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY product
ORDER BY total_revenue DESC;


-- 2.2 REVENUE BY REGION
-- Business Question:
-- Which region generates the most revenue?

SELECT
    region,
    ROUND(
        SUM(quantity * unit_price * (1 - discount))::numeric,
        2
    ) AS total_revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY region
ORDER BY total_revenue DESC;


-- 2.3 REVENUE BY CATEGORY
-- Business Question:
-- Which product category generates the most revenue?

SELECT
    category,
    ROUND(
        SUM(quantity * unit_price * (1 - discount))::numeric,
        2
    ) AS total_revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY category
ORDER BY total_revenue DESC;


-- =====================================================
-- 3. MONTHLY REVENUE AND GROWTH ANALYSIS
-- =====================================================


-- 3.1 MONTHLY REVENUE
-- Business Question:
-- How much revenue does the business generate each month?

SELECT
    TO_CHAR(order_date, 'Mon') AS month,
    EXTRACT(MONTH FROM order_date) AS month_number,
    ROUND(
        SUM(quantity * unit_price * (1 - discount))::numeric,
        2
    ) AS monthly_revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY
    EXTRACT(MONTH FROM order_date),
    TO_CHAR(order_date, 'Mon')
ORDER BY month_number;


-- 3.2 MONTH-OVER-MONTH REVENUE GROWTH
-- Business Question:
-- Is revenue increasing or decreasing each month?

WITH monthly_sales AS (
    SELECT
        EXTRACT(MONTH FROM order_date)::int AS month_number,
        SUM(quantity * unit_price * (1 - discount)) AS revenue
    FROM sales
    WHERE order_status = 'Delivered'
    GROUP BY EXTRACT(MONTH FROM order_date)
),
monthly_comparison AS (
    SELECT
        month_number,
        revenue,
        LAG(revenue) OVER (ORDER BY month_number) AS previous_revenue
    FROM monthly_sales
)
SELECT
    month_number,
    ROUND(revenue::numeric, 2) AS revenue,
    ROUND(previous_revenue::numeric, 2) AS previous_revenue,
    ROUND(
        (
            (revenue - previous_revenue)
            / NULLIF(previous_revenue, 0) * 100
        )::numeric,
        2
    ) AS growth_percentage
FROM monthly_comparison
ORDER BY month_number;



-- =====================================================
-- 4. CUSTOMER ANALYSIS
-- =====================================================


-- 4.1 TOP 10 CUSTOMERS
-- Business Question:
-- Who are the most valuable customers?

SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(quantity * unit_price * (1 - discount))::numeric,
        2
    ) AS total_revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 4.2 AVERAGE ORDER VALUE (AOV)
-- Business Question:
-- How much revenue does the business generate per order?

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(quantity * unit_price * (1 - discount))::numeric,
        2
    ) AS total_revenue,
    ROUND(
        (
            SUM(quantity * unit_price * (1 - discount))
            / COUNT(DISTINCT order_id)
        )::numeric,
        2
    ) AS average_order_value
FROM sales
WHERE order_status = 'Delivered';



-- =====================================================
-- 5. ORDER STATUS AND PAYMENT ANALYSIS
-- =====================================================


-- 5.1 ORDER STATUS ANALYSIS
-- Business Question:
-- How many orders were delivered, cancelled, and returned?

SELECT
    order_status,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales
GROUP BY order_status
ORDER BY total_orders DESC;


-- 5.2 REVENUE BY PAYMENT METHOD
-- Business Question:
-- Which payment methods generate the most revenue?

SELECT
    payment_method,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        SUM(quantity * unit_price * (1 - discount))::numeric,
        2
    ) AS total_revenue
FROM sales
WHERE order_status = 'Delivered'
GROUP BY payment_method
ORDER BY total_revenue DESC;
