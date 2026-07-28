"""
charts.py
Reads results.json (created by app.py) and generates a handful of
charts using matplotlib/seaborn. Saves each chart as a PNG in the
charts/ folder, so generate_pdf_report.py can drop them into the
final PDF.

Nothing fancy here -- this is the same matplotlib/seaborn workflow
you already know: build a figure, plot the data, save it as an image.
"""

import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- 1. SETUP ----------
sns.set_theme(style="whitegrid")

CHARTS_FOLDER = "charts"
os.makedirs(CHARTS_FOLDER, exist_ok=True)

with open("results.json", "r") as f:
    data = json.load(f)

results = data["results"]


# ---------- 2. CHART 1: Top 5 Pizzas by Revenue ----------
top_pizzas = results.get("top_3_by_revenue")
if top_pizzas:
    names = [row["name"] for row in top_pizzas]
    revenues = [float(row["revenue"]) for row in top_pizzas]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=revenues, y=names, color="#d62828")
    plt.title("Top Pizzas by Revenue")
    plt.xlabel("Revenue ($)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_FOLDER}/top_pizzas.png", dpi=150)
    plt.close()
    print("Saved top_pizzas.png")


# ---------- 3. CHART 2: Revenue by Category ----------
category_data = results.get("quantity_by_category")
if category_data:
    # Sort so the tallest bar is first -- makes the chart easy to read
    # and avoids any ordering mismatch between labels and bars.
    category_data = sorted(category_data, key=lambda row: float(row["total_quantity"]), reverse=True)

    categories = [row["category"] for row in category_data]
    quantities = [float(row["total_quantity"]) for row in category_data]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories, quantities, color="#f77f00")
    plt.title("Total Pizzas Sold by Category")
    plt.xlabel("Category")
    plt.ylabel("Quantity Sold")

    # Force the y-axis to always start at 0. Without this, matplotlib
    # sometimes auto-scales the axis to start near the smallest value,
    # which makes bars look clipped or missing.
    plt.ylim(0, max(quantities) * 1.15)

    # Print the exact number on top of each bar so the chart is
    # unambiguous even without reading the axis.
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + (max(quantities) * 0.02),
                  f"{int(height):,}", ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(f"{CHARTS_FOLDER}/category_quantity.png", dpi=150)
    plt.close()
    print("Saved category_quantity.png")


# ---------- 4. CHART 3: Monthly Revenue Trend ----------
trend_data = results.get("monthly_revenue_trend")
if trend_data:
    months = [row["month"] for row in trend_data]
    revenues = [float(row["revenue"]) for row in trend_data]

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=months, y=revenues, marker="o", color="#003049")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{CHARTS_FOLDER}/monthly_trend.png", dpi=150)
    plt.close()
    print("Saved monthly_trend.png")


# ---------- 5. CHART 4: Revenue by Weekday ----------
weekday_data = results.get("revenue_by_weekday")
if weekday_data:
    weekdays = [row["weekday"] for row in weekday_data]
    revenues = [float(row["revenue"]) for row in weekday_data]

    plt.figure(figsize=(8, 5))
    sns.barplot(x=revenues, y=weekdays, color="#219ebc")
    plt.title("Revenue by Day of Week")
    plt.xlabel("Revenue ($)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_FOLDER}/revenue_by_weekday.png", dpi=150)
    plt.close()
    print("Saved revenue_by_weekday.png")


# ---------- 6. CHART 5: Peak Order Hours ----------
peak_hours = results.get("peak_hours")
if peak_hours:
    hours = [str(row["hour"]) + ":00" for row in peak_hours]
    counts = [row["order_count"] for row in peak_hours]

    plt.figure(figsize=(7, 5))
    sns.barplot(x=hours, y=counts, color="#8ecae6")
    plt.title("Peak Order Hours")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(f"{CHARTS_FOLDER}/peak_hours.png", dpi=150)
    plt.close()
    print("Saved peak_hours.png")

print(f"\nAll charts saved to the '{CHARTS_FOLDER}/' folder.")