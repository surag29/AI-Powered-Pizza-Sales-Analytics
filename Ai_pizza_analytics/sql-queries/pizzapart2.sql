-- Intermediate:
-- Join the necessary tables to find the total quantity of each pizza category ordered.
select * from pizza_types;
select * from pizzas;
select * from order_details;

SELECT 
    pt.category, SUM(o.quantity) AS total_quantity
FROM
    pizza_types pt
        JOIN
    pizzas p ON pt.pizza_type_id = p.pizza_type_id
        JOIN
    order_details o ON p.pizza_id = o.pizza_id
GROUP BY pt.category;
-- Determine the distribution of orders by hour of the day.
 
SELECT 
    HOUR(order_time) AS hour, COUNT(order_id) AS order_count
FROM
    orders
GROUP BY HOUR(order_time);
 
-- Join relevant tables to find the category-wise distribution of pizzas.

SELECT 
    category, COUNT(name)
FROM
    pizza_types
GROUP BY category;
 
-- Group the orders by date and calculate the average number of pizzas ordered per day.
SELECT 
    AVG(Quantity)
FROM
    (SELECT 
        o.order_date, SUM(od.quantity) AS Quantity
    FROM
        orders o
    JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.order_date) AS order_quantity;
-- Determine the top 3 most ordered pizza types based on revenue.

SELECT 
    pt.name, SUM(o.quantity * p.price) AS revenue
FROM
    pizza_types pt
        JOIN
    pizzas p ON pt.pizza_type_id = p.pizza_type_id
        JOIN
    order_details o ON p.pizza_id = o.pizza_id
GROUP BY pt.name
ORDER BY revenue DESC
LIMIT 3;

