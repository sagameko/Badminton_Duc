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
                # Use the new model naming format with speed optimizations
                generation_config = {
                    "temperature": 0.3,  # Lower = more focused/faster
                    "top_p": 0.8,
                    "top_k": 20,
                    "max_output_tokens": 200,  # Limit output for speed
                }
                self.model = genai.GenerativeModel(
                    'gemini-2.0-flash',
                    generation_config=generation_config
                )
                self.enabled = True
                print("AI chat enabled with Gemini 2.0 Flash (optimized)")
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

            # Build conversation context if history exists (keep it short)
            context = ""
            if chat_history and len(chat_history) > 1:
                context = "\nRecent context:\n"
                # Include last 2 exchanges for context (reduced for speed)
                for msg in chat_history[-4:]:
                    role = "U" if msg["role"] == "user" else "A"
                    context += f"{role}: {msg['content'][:80]}\n"

            prompt = f"""Today: {today.strftime('%Y-%m-%d, %A')}
{context}
Message: "{user_message}"

Extract JSON: {{"intent": "check_availability"|"book"|"help"|"greeting"|"unknown", "date": "YYYY-MM-DD"|null, "time": "HH:MM"|null, "friendly_response": "short text"}}

Date rules: tomorrow={today + timedelta(days=1):%Y-%m-%d}, today={today:%Y-%m-%d}, day names=next occurrence
Time rules: 6pm=18:00, 10am=10:00, morning/evening=null
Intent: check_availability for "what's available", book for "I want to book", help/greeting as appropriate
Follow-ups: use context to determine date/time

JSON only:"""

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

        lines = []
        for i, slot in enumerate(slots[:max_slots]):
            start_dt = datetime.fromisoformat(slot['start_time'])
            end_dt = datetime.fromisoformat(slot['end_time'])
            lines.append(
                f"{i+1}. {start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')} "
                f"({slot['duration']})"
            )

        result = "\n".join(lines)

        if len(slots) > max_slots:
            result += f"\n\n...and {len(slots) - max_slots} more slots available"

        return result
