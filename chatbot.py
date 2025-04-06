from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def ask_gpt_travel(question):
    prompt = f"Bạn là trợ lý du lịch AI thông minh. Hãy trả lời ngắn gọn và thực tế:\n\n{question}\n\nTrả lời:"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print("🔥 OpenAI error:", e)
        print("✅ API key:", openai.api_key)
        print("✅ Prompt:", prompt)
        return "❌ Hệ thống gặp lỗi khi truy vấn AI. Vui lòng thử lại sau."

@app.route("/webhook", methods=["POST"])
def chatbot_webhook():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    reply = ask_gpt_travel(user_message)
    return jsonify({"reply": reply})
