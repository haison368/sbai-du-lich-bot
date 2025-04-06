
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("API KEY OPENAI")

def ask_gpt_travel(question):
    prompt = f"Bạn là trợ lý du lịch AI thông minh. Hãy trả lời ngắn gọn và thực tế.\n\n{question}\n\nTrả lời:"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=400
    )
    return response.choices[0].message.content.strip()

@app.route("/chatbot_ai/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_input = data.get("message", "")
    reply = ask_gpt_travel(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
