-- Advanced:
-- Calculate the percentage contribution of each pizza type to total revenue.
SELECT 
    pt.category,
    (SUM(o.quantity * p.price) / (SELECT 
            ROUND(SUM((o.quantity * p.price)), 2) AS total_revenue
        FROM
            order_details o
                JOIN
            pizzas p ON o.pizza_id = p.pizza_id)) * 100 AS percentage_contribution
FROM
    pizza_types pt
        JOIN
    pizzas p ON pt.pizza_type_id = p.pizza_type_id
        JOIN
    order_details o ON p.pizza_id = o.pizza_id
GROUP BY pt.category
ORDER BY SUM(o.quantity * p.price) DESC;


-- Analyze the cumulative revenue generated over time.

select order_date , 
sum(revenue) over(order by order_date) as cumm_revenue
from 
(select o.order_date,sum(od.quantity*p.price) as revenue
 from orders o
 join order_details od
 on o.order_id = od.order_id
 join pizzas p
 on p.pizza_id = od.pizza_id 
 group by o.order_date) as sales;

-- Determine the top 3 most ordered pizza types based on revenue for each pizza category.
select name, revenue from
(select category , name , revenue,
rank() over(partition by category order by revenue desc)  as rnk
from 
(select pt.category,pt.name,sum(od.quantity*p.price) as revenue
 from pizza_types pt
 join pizzas p 
 on pt.pizza_type_id = p.pizza_type_id
 join order_details od
 on p.pizza_id = od.pizza_id
 group by pt.category,pt.name) as b) as a
 where rnk <=3;
