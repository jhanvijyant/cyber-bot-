from flask import Flask, render_template, request
import google.generativeai as genai
import os
app = Flask(__name__)
GOOGLE_API_KEY = "your api key !!"  
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
@app.route("/", methods=["GET", "POST"])
def chat():
    response = ""
    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if question:
            try:
                chat = model.start_chat()
                result = chat.send_message(question)
                response = result.text
                print(f"📝 Generated Response: '{response}'")
            except Exception as e:
                response = f"Error generating response: {e}"
    return render_template("index.html", response=response)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
