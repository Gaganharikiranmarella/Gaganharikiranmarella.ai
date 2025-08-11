import os
import requests
from flask import Flask, request, render_template_string
from dotenv import load_dotenv
import docx2txt
import pdfplumber

# Load API Key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML Templates with Bootstrap and minor branding tweaks
HTML_INDEX = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Smart Resume Analyzer (OpenRouter LLM)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-7">
                <div class="card shadow">
                    <div class="card-body">
                        <h2 class="mb-4 text-primary text-center">Smart Resume Analyzer</h2>
                        <form method="post" enctype="multipart/form-data">
                            <div class="mb-3">
                                <input class="form-control" type="file" name="resume" accept=".pdf,.docx,.txt" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-success btn-lg">Analyze Resume</button>
                            </div>
                        </form>
                        {% if error %}
                        <div class="alert alert-danger mt-4">{{ error }}</div>
                        {% endif %}
                        <p class="mt-4 text-secondary small text-center">Robotics & Defense Research Resume AI<br>
                        Powered by DeepSeek via OpenRouter</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

HTML_RESULT = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Analysis Result</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h3 class="mb-0">AI-Powered Resume Analysis</h3>
                    </div>
                    <div class="card-body">
                        <pre style="white-space: pre-wrap; font-size: 1.1em;">{{ analysis }}</pre>
                        <div class="d-grid mt-4">
                            <a href="/" class="btn btn-outline-primary btn-lg">Analyze Another Resume</a>
                        </div>
                    </div>
                </div>
                <p class="mt-4 text-secondary small text-center">
                    Robotics & Defense Resume Analyzer | Powered by DeepSeek (OpenRouter)
                </p>
            </div>
        </div>
    </div>
</body>
</html>
'''

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

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        file = request.files.get('resume')
        if not file or file.filename == '':
            return render_template_string(HTML_INDEX, error="No file selected!")
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)

        resume_text = extract_text(save_path)
        if not resume_text.strip():
            return render_template_string(HTML_INDEX, error="Could not extract text from file.")

        # LLM Prompt
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

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek/deepseek-r1",  # Using DeepSeek as requested
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
    return render_template_string(HTML_INDEX, error=error)

if __name__ == '__main__':
    app.run(debug=True)
