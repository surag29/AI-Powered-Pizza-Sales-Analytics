"""
queries.py
All SQL queries for the Pizza Sales Analytics project, in one place.

To add a new query: just add a new key to the QUERIES dictionary below,
following the same pattern. app.py will automatically pick it up,
run it, and it will automatically flow into the AI insights too.
"""

QUERIES = {

    # ---------------- BASIC ----------------

    "total_orders": """
        SELECT COUNT(order_id) AS total_orders
        FROM orders;
    """,

    "total_revenue": """
        SELECT ROUND(SUM((o.quantity * p.price)), 2) AS total_revenue
        FROM order_details o
        JOIN pizzas p ON o.pizza_id = p.pizza_id;
    """,

    "highest_priced_pizza": """
        SELECT pt.name, p.price
        FROM pizza_types pt
        JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
        ORDER BY p.price DESC
        LIMIT 1;
    """,

    "most_common_size": """
        SELECT p.size, COUNT(o.order_details_id) AS order_count
        FROM pizzas p
        JOIN order_details o ON p.pizza_id = o.pizza_id
        GROUP BY p.size
        ORDER BY order_count DESC;
    """,

    "top_5_pizzas": """
        SELECT pt.name, SUM(o.quantity) AS total_quantity
        FROM pizza_types pt
        JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
        JOIN order_details o ON p.pizza_id = o.pizza_id
        GROUP BY pt.name
        ORDER BY total_quantity DESC
        LIMIT 5;
    """,

    # ---------------- INTERMEDIATE ----------------

    "quantity_by_category": """
        SELECT pt.category, SUM(o.quantity) AS total_quantity
        FROM pizza_types pt
        JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
        JOIN order_details o ON p.pizza_id = o.pizza_id
        GROUP BY pt.category;
    """,

    "orders_by_hour": """
        SELECT HOUR(order_time) AS hour, COUNT(order_id) AS order_count
        FROM orders
        GROUP BY HOUR(order_time);
    """,

    "pizza_count_by_category": """
        SELECT category, COUNT(name) AS pizza_count
        FROM pizza_types
        GROUP BY category;
    """,

    "avg_pizzas_per_day": """
        SELECT AVG(Quantity) AS avg_pizzas_per_day
        FROM (
            SELECT o.order_date, SUM(od.quantity) AS Quantity
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            GROUP BY o.order_date
        ) AS order_quantity;
    """,

    "top_3_by_revenue": """
        SELECT pt.name, SUM(o.quantity * p.price) AS revenue
        FROM pizza_types pt
        JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
        JOIN order_details o ON p.pizza_id = o.pizza_id
        GROUP BY pt.name
        ORDER BY revenue DESC
        LIMIT 3;
    """,

    # ---------------- ADVANCED ----------------

    "revenue_percentage_by_category": """
        SELECT
            pt.category,
            (SUM(o.quantity * p.price) /
                (SELECT ROUND(SUM((o.quantity * p.price)), 2)
                 FROM order_details o
                 JOIN pizzas p ON o.pizza_id = p.pizza_id)
            ) * 100 AS percentage_contribution
        FROM pizza_types pt
        JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
        JOIN order_details o ON p.pizza_id = o.pizza_id
        GROUP BY pt.category
        ORDER BY SUM(o.quantity * p.price) DESC;
    """,

    "cumulative_revenue": """
        SELECT order_date,
               SUM(revenue) OVER (ORDER BY order_date) AS cumm_revenue
        FROM (
            SELECT o.order_date, SUM(od.quantity * p.price) AS revenue
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            JOIN pizzas p ON p.pizza_id = od.pizza_id
            GROUP BY o.order_date
        ) AS sales;
    """,

    "top_3_by_revenue_per_category": """
        SELECT name, revenue FROM (
            SELECT category, name, revenue,
                   RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rnk
            FROM (
                SELECT pt.category, pt.name, SUM(od.quantity * p.price) AS revenue
                FROM pizza_types pt
                JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
                JOIN order_details od ON p.pizza_id = od.pizza_id
                GROUP BY pt.category, pt.name
            ) AS b
        ) AS a
        WHERE rnk <= 3;
    """,

    # ---------------- NEW: BUSINESS-FOCUSED ADVANCED QUERIES ----------------

    "monthly_revenue_trend": """
        SELECT
            DATE_FORMAT(o.order_date, '%Y-%m') AS month,
            ROUND(SUM(od.quantity * p.price), 2) AS revenue,
            ROUND(
                (SUM(od.quantity * p.price) - LAG(SUM(od.quantity * p.price))
                    OVER (ORDER BY DATE_FORMAT(o.order_date, '%Y-%m')))
                / LAG(SUM(od.quantity * p.price))
                    OVER (ORDER BY DATE_FORMAT(o.order_date, '%Y-%m')) * 100,
            2) AS growth_percent
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        GROUP BY month
        ORDER BY month;
    """,

    "revenue_by_weekday": """
        SELECT
            DAYNAME(order_date) AS weekday,
            ROUND(SUM(od.quantity * p.price), 2) AS revenue,
            COUNT(DISTINCT o.order_id) AS total_orders
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        GROUP BY weekday
        ORDER BY revenue DESC;
    """,

    "avg_order_value": """
        SELECT
            ROUND(SUM(od.quantity * p.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id;
    """,

    "revenue_by_size": """
        SELECT
            p.size,
            ROUND(SUM(od.quantity * p.price), 2) AS revenue,
            ROUND(SUM(od.quantity * p.price) * 100.0 /
                (SELECT SUM(od2.quantity * p2.price)
                 FROM order_details od2
                 JOIN pizzas p2 ON od2.pizza_id = p2.pizza_id), 2) AS revenue_percent
        FROM order_details od
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        GROUP BY p.size
        ORDER BY revenue DESC;
    """,

    "worst_5_pizzas": """
        SELECT
            pt.name,
            SUM(od.quantity) AS total_quantity,
            ROUND(SUM(od.quantity * p.price), 2) AS revenue
        FROM pizza_types pt
        JOIN pizzas p ON pt.pizza_type_id = p.pizza_type_id
        JOIN order_details od ON p.pizza_id = od.pizza_id
        GROUP BY pt.name
        ORDER BY total_quantity ASC
        LIMIT 5;
    """,

    "weekend_vs_weekday": """
        SELECT
            CASE
                WHEN DAYOFWEEK(o.order_date) IN (1, 7) THEN 'Weekend'
                ELSE 'Weekday'
            END AS day_type,
            ROUND(SUM(od.quantity * p.price), 2) AS revenue,
            COUNT(DISTINCT o.order_id) AS total_orders,
            ROUND(SUM(od.quantity * p.price) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        GROUP BY day_type;
    """,

    "peak_month": """
        SELECT
            MONTHNAME(order_date) AS month_name,
            ROUND(SUM(od.quantity * p.price), 2) AS revenue
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        JOIN pizzas p ON od.pizza_id = p.pizza_id
        GROUP BY month_name
        ORDER BY revenue DESC
        LIMIT 1;
    """,

    "peak_hours": """
        SELECT
            HOUR(order_time) AS hour,
            COUNT(order_id) AS order_count
        FROM orders
        GROUP BY hour
        ORDER BY order_count DESC
        LIMIT 3;
    """,

    "highest_growth_month": """
        SELECT month, revenue, growth_percent
        FROM (
            SELECT
                DATE_FORMAT(o.order_date, '%Y-%m') AS month,
                ROUND(SUM(od.quantity * p.price), 2) AS revenue,
                ROUND(
                    (SUM(od.quantity * p.price) - LAG(SUM(od.quantity * p.price))
                        OVER (ORDER BY DATE_FORMAT(o.order_date, '%Y-%m')))
                    / LAG(SUM(od.quantity * p.price))
                        OVER (ORDER BY DATE_FORMAT(o.order_date, '%Y-%m')) * 100,
                2) AS growth_percent
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            JOIN pizzas p ON od.pizza_id = p.pizza_id
            GROUP BY month
        ) AS monthly
        WHERE growth_percent IS NOT NULL
        ORDER BY growth_percent DESC
        LIMIT 1;
    """,

    "biggest_decline_month": """
        SELECT month, revenue, growth_percent
        FROM (
            SELECT
                DATE_FORMAT(o.order_date, '%Y-%m') AS month,
                ROUND(SUM(od.quantity * p.price), 2) AS revenue,
                ROUND(
                    (SUM(od.quantity * p.price) - LAG(SUM(od.quantity * p.price))
                        OVER (ORDER BY DATE_FORMAT(o.order_date, '%Y-%m')))
                    / LAG(SUM(od.quantity * p.price))
                        OVER (ORDER BY DATE_FORMAT(o.order_date, '%Y-%m')) * 100,
                2) AS growth_percent
            FROM orders o
            JOIN order_details od ON o.order_id = od.order_id
            JOIN pizzas p ON od.pizza_id = p.pizza_id
            GROUP BY month
        ) AS monthly
        WHERE growth_percent IS NOT NULL
        ORDER BY growth_percent ASC
        LIMIT 1;
    """,

    # 👉 ADD FUTURE QUERIES HERE — just follow the same pattern:
    # "your_query_name": """
    #     SELECT ...
    # """,

}