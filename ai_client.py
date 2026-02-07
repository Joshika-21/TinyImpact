import os
from typing import List, Dict, Optional

from dotenv import load_dotenv
from google import genai

# -----------------------------
# Setup: load API key & client
# -----------------------------

# Load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # This will show up in your terminal if key is missing
    raise ValueError("❌ GEMINI_API_KEY not found. Make sure it's set in your .env file.")

# Create Gemini client (google-genai)
client = genai.Client(api_key=GEMINI_API_KEY)


# -----------------------------
# Main function for the app
# -----------------------------

def generate_challenge(
    living_situation: str,
    time_minutes: int,
    focus_areas: List[str],
    difficulty: str,
) -> Optional[Dict[str, str]]:
    """
    Calls Gemini to generate ONE eco challenge.

    Returns a dict with keys:
      - challenge
      - why_it_matters
      - impact_estimate
      - category

    Returns None if something goes wrong (so the app can fall back).
    """

    focus_text = ", ".join(focus_areas) if focus_areas else "any sustainability area"

    prompt = f"""
You are an assistant that creates ONE small, realistic daily sustainability challenge.

User context:
- Living situation: {living_situation}
- Time available today: {time_minutes} minutes
- Focus areas: {focus_text}
- Difficulty level: {difficulty}

Rules:
- The challenge must be achievable in ONE day.
- It must take no more than the given time.
- It must be beginner-friendly.
- Choose ONE category from: Waste, Energy, Food, Transport, Water, Digital.

Return your answer in EXACTLY this format:

Challenge: <short actionable challenge>
Why it matters: <2-3 sentences>
Impact estimate: <1 sentence with a concrete or numeric impact>
Category: <one category>

Do not add bullets, markdown, or extra text.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        text = response.text.strip()

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        data: Dict[str, str] = {}

        for line in lines:
            lower = line.lower()
            if lower.startswith("challenge:"):
                data["challenge"] = line.split(":", 1)[1].strip()
            elif lower.startswith("why it matters:"):
                data["why_it_matters"] = line.split(":", 1)[1].strip()
            elif lower.startswith("impact estimate:"):
                data["impact_estimate"] = line.split(":", 1)[1].strip()
            elif lower.startswith("category:"):
                data["category"] = line.split(":", 1)[1].strip()

        required_keys = {"challenge", "why_it_matters", "impact_estimate", "category"}
        if not required_keys.issubset(data.keys()):
            print("⚠️ Gemini response missing fields. Falling back to predefined challenges.")
            return None

        return data

    except Exception as e:
        print("❌ Error while calling Gemini:", e)
        return None


# -----------------------------
# Local test (run this file alone)
# -----------------------------
if __name__ == "__main__":
    test_result = generate_challenge(
        living_situation="Dorm",
        time_minutes=10,
        focus_areas=["Waste", "Water"],
        difficulty="Easy",
    )
    print("\nAI TEST OUTPUT:\n")
    print(test_result)
