"""
ai_insights.py
Loads results.json (created by app.py), builds a text prompt from the
SQL query results, sends it to Groq's LLM API, and saves the AI's
business insights to ai_insights.md.

Why this version is simple:
Finding the "peak month" or the "worst pizza" is a sorting problem.
SQL is already great at sorting (ORDER BY ... LIMIT), so the queries
in queries.py do that work themselves (see peak_month, peak_hours,
worst_5_pizzas, highest_growth_month, biggest_decline_month -- they
all use ORDER BY + LIMIT to hand back the answer already found).

Because of that, this script does NOT need to search for the highest
or lowest value in Python. It just reads the results MySQL already
sorted, turns them into readable text, and sends that text to the AI.
"""

import json
import os
from groq import Groq
from dotenv import load_dotenv

# ---------- 1. CONFIGURE GROQ ----------
load_dotenv()   # reads the .env file in the same folder

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

# ---------- 2. LOAD YOUR SQL RESULTS ----------
with open("results.json", "r") as f:
    data = json.load(f)

results = data["results"]

# ---------- 3. TRIM LISTS THAT ARE TOO LONG FOR THE PROMPT ----------
# Some results (like cumulative_revenue) can have hundreds of daily
# rows. The AI doesn't need every row, just a sense of the trend. So
# if a list has more than 15 items, we only keep the count, the first
# item, and the last item.

TRUNCATE_THRESHOLD = 15
trimmed_results = {}

for name, value in results.items():
    if isinstance(value, list) and len(value) > TRUNCATE_THRESHOLD:
        first_item = value[0]
        last_item = value[-1]
        trimmed_results[name] = f"{len(value)} records. First: {first_item}. Last: {last_item}."
    else:
        trimmed_results[name] = value

# ---------- 4. BUILD THE PROMPT ----------
lines = ["Here are the KPIs for a pizza restaurant, calculated from SQL queries:\n"]

for name, value in trimmed_results.items():
    readable_name = name.replace("_", " ").title()
    lines.append(f"{readable_name}: {value}")

kpi_text = "\n".join(lines)

prompt = f"""
You are a senior restaurant business analyst preparing a report for management.

{kpi_text}

Using ALL the data above -- including revenue trends, monthly growth, weekday
patterns, weekend vs weekday performance, order value, pizza size performance,
best/worst selling pizzas, peak month, and peak hours -- write a detailed report
with the following sections:

1. **Executive Summary** (3-4 sentences covering overall performance and trend direction)

2. **Revenue & Growth Insights** (3-4 bullet points, reference the Highest Growth Month
   and Biggest Decline Month figures given above)

3. **Product Performance Insights** (3-4 bullet points on best/worst selling pizzas,
   pizza sizes, and category performance)

4. **Customer Behavior & Timing Insights** (3-4 bullet points on peak hours, weekday
   vs weekend patterns, and average order value)

5. **Recommendations** (5 specific, actionable recommendations -- each should tie back
   to a specific number or trend from the data above, not generic advice)

6. **Risks to Watch** (2-3 bullet points on any concerning patterns, e.g. underperforming
   pizzas, weak days/months, or slowing growth, if the data suggests them)

IMPORTANT: Only state numbers that appear explicitly in the data above. Do not
estimate, round unusually, or invent a number for any month, day, or pizza not
shown.

Use clear bullet points and bold section headers.
"""

# ---------- 5. SEND TO GROQ ----------
print("Sending data to Groq... please wait.\n")

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

ai_text = response.choices[0].message.content

# ---------- 6. SHOW + SAVE THE RESPONSE ----------
print("AI BUSINESS INSIGHTS\n")
print(ai_text)

with open("ai_insights.md", "w", encoding="utf-8") as f:
    f.write(ai_text)

print("\nInsights saved to ai_insights.md")