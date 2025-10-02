"""
AI-powered chat helper using Google Gemini
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class AIChatHelper:
    """AI-powered chat helper for natural language booking queries"""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                # Use the new model naming format with balanced config
                generation_config = {
                    "temperature": 0.7,  # Higher for more natural conversation
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 500,  # More tokens for better responses
                }
                self.model = genai.GenerativeModel(
                    'gemini-2.0-flash',
                    generation_config=generation_config
                )
                self.enabled = True
                print("AI chat enabled with Gemini 2.0 Flash")
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
                self.enabled = False
        else:
            self.enabled = False
            print("Warning: GEMINI_API_KEY not found. AI chat disabled.")

    def parse_query(self, user_message: str, chat_history: list = None) -> Dict:
        """
        Use Gemini AI to parse user query and extract booking intent

        Returns:
            {
                "intent": "check_availability" | "book" | "help" | "greeting" | "unknown",
                "date": "2024-10-04" or None,
                "time": "18:00" or None,
                "response_text": "Friendly response if needed"
            }
        """
        if not self.enabled:
            return {"intent": "unknown", "date": None, "time": None}

        try:
            today = datetime.now()

            # Build conversation context if history exists
            context = ""
            if chat_history and len(chat_history) > 1:
                context = "\n\nConversation history (for context):\n"
                # Include last 3 exchanges for better context
                for msg in chat_history[-6:]:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    context += f"{role}: {msg['content']}\n"

            prompt = f"""You are a friendly badminton court booking assistant and you are working at MSAC Sport Center. Today is {today.strftime('%A, %B %d, %Y')}.
{context}

User's message: "{user_message}"

Your task:
1. Understand what the user wants (check availability, book a court, ask for help, greeting, or other)
2. Extract any date and time mentioned (use conversation context for follow-ups like "what about the next day")
3. Provide a friendly, natural response

Date parsing rules:
- "tomorrow" = {(today + timedelta(days=1)).strftime('%Y-%m-%d')}
- "today" = {today.strftime('%Y-%m-%d')}
- Day names (Monday, Tuesday, etc) = next occurrence of that day
- "next Friday" = the upcoming Friday
- If user says "what about Friday" after asking about Thursday, they mean THIS Friday

Time parsing rules:
- "6pm", "6 pm", "18:00" = 18:00
- "morning" = null (show all morning slots)
- "evening" = null (show all evening slots)
- Be flexible with time formats

Intent rules:
- "check_availability": User wants to see what's available
- "book": User wants to book a court
- "help": User needs assistance
- "greeting": User is saying hi/hello
- "unknown": You're not sure

Response in JSON format:
{{
  "intent": "check_availability" | "book" | "help" | "greeting" | "unknown",
  "date": "YYYY-MM-DD" or null,
  "time": "HH:MM" or null,
  "friendly_response": "A warm, natural response that acknowledges what they asked and shows you understood"
}}

JSON response:"""

            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # Clean up response (remove markdown code blocks if present)
            if result_text.startswith("```json"):
                result_text = result_text.replace("```json", "").replace("```", "").strip()
            elif result_text.startswith("```"):
                result_text = result_text.replace("```", "").strip()

            # Parse JSON response
            parsed = json.loads(result_text)

            return {
                "intent": parsed.get("intent", "unknown"),
                "date": parsed.get("date"),
                "time": parsed.get("time"),
                "friendly_response": parsed.get("friendly_response", "")
            }

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {result_text if 'result_text' in locals() else 'No response'}")
            return {
                "intent": "unknown",
                "date": None,
                "time": None,
                "friendly_response": "I had trouble parsing the AI response. Using fallback mode."
            }
        except Exception as e:
            print(f"AI parsing error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "intent": "unknown",
                "date": None,
                "time": None,
                "friendly_response": f"AI Error: {str(e)[:100]}"
            }

    def format_slots_for_chat(self, slots: list, max_slots: int = 8) -> str:
        """Format available slots into a readable message"""
        if not slots:
            return "No available slots found."

        def format_duration(iso_duration: str) -> str:
            """Convert PT30M to '30 min'"""
            import re
            hours = re.search(r'(\d+)H', iso_duration)
            minutes = re.search(r'(\d+)M', iso_duration)
            h = int(hours.group(1)) if hours else 0
            m = int(minutes.group(1)) if minutes else 0
            parts = []
            if h > 0:
                parts.append(f"{h} hour" if h == 1 else f"{h} hours")
            if m > 0:
                parts.append(f"{m} min")
            return " ".join(parts) if parts else "Unknown"

        lines = []
        for i, slot in enumerate(slots[:max_slots]):
            start_dt = datetime.fromisoformat(slot['start_time'])
            end_dt = datetime.fromisoformat(slot['end_time'])
            duration = format_duration(slot['duration'])
            lines.append(
                f"{i+1}. **{start_dt.strftime('%I:%M %p')}** - {end_dt.strftime('%I:%M %p')} "
                f"({duration})"
            )

        result = "\n".join(lines)

        if len(slots) > max_slots:
            result += f"\n\n...and **{len(slots) - max_slots} more slots** available"

        return result
