import os
import requests
from flask import Flask, request, render_template_string
from dotenv import load_dotenv
import docx2txt
import pdfplumber

# ----------------------
# Load API Key from .env
# ----------------------
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------
# HTML Templates
# ----------------------
HTML_INDEX = '''
<!doctype html>
<title>Smart Resume Analyzer (OpenRouter LLM)</title>
<h2>Upload your Resume (PDF, DOCX, or TXT)</h2>
<form method=post enctype=multipart/form-data>
  <input type=file name=resume accept=".pdf,.docx,.txt"><br><br>
  <input type=submit value=Analyze>
</form>
'''

HTML_RESULT = '''
<!doctype html>
<title>Analysis Result</title>
<h2>Analysis Result</h2>
<pre>{{ analysis }}</pre>
<br>
<a href="/">Analyze another Resume</a>
'''

# ----------------------
# Helper: Extract text from DOCX, PDF, TXT
# ----------------------
def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    elif ext == ".docx":
        return docx2txt.process(file_path)
    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    else:
        return ""

# ----------------------
# Flask Routes
# ----------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('resume')
        if not file or file.filename == '':
            return render_template_string(HTML_INDEX + '<p style="color:red;">No file selected!</p>')

        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)

        resume_text = extract_text(save_path)
        if not resume_text.strip():
            return render_template_string(HTML_INDEX + '<p style="color:red;">Could not extract text from file.</p>')

        # Prompt for the LLM
        prompt = (
            "You are an AI assistant specializing in resume analysis for robotics and defense roles.\n"
            "Analyze the following resume for:\n"
            "- Key skills and experience in Robotics/Defense\n"
            "- ATS compatibility suggestions\n"
            "- Suggestions for improvements\n"
            "--- Resume Text Start ---\n"
            f"{resume_text}\n"
            "--- Resume Text End ---"
        )

        # OpenRouter API Call
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek/deepseek-r1",  # Change to other models if needed
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            analysis = response.json()["choices"][0]["message"]["content"]
        else:
            analysis = f"Error {response.status_code}: {response.text}"

        return render_template_string(HTML_RESULT, analysis=analysis)

    return render_template_string(HTML_INDEX)

if __name__ == '__main__':
    app.run(debug=True)