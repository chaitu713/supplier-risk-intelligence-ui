from google import genai
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)


def ask_supplier_ai(question, performance_df):

    try:
        context_data = performance_df.sort_values(
            "risk_score", ascending=False
        )[[
            "supplier_name",
            "country",
            "category",
            "avg_delay",
            "avg_defect",
            "avg_cost_variance",
            "risk_score"
        ]].head(50)

        data_text = context_data.to_string(index=False)

        prompt = f"""
You are an expert AI procurement analyst.

Dataset:
{data_text}

User Question:
{question}

Instructions:
- Respond in EXACTLY 3 sections:
  Key Insights
  Risk Alerts
  Recommendations

- Use bullet points ONLY (no numbering like 1., 2.)
- Each bullet must be a COMPLETE single line (no line breaks inside sentences)
- Do NOT break numbers or parentheses across lines
- Keep everything clean and readable
- Max 6–8 bullets total
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error generating AI response: {str(e)}"