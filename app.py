import pandas as pd
import pandas as pd
import socket
from urllib.parse import urlparse
from flask import Flask, request, render_template_string
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("phishing.csv")

X = data.drop("Result", axis=1)
y = data["Result"]

model = RandomForestClassifier()
model.fit(X, y)

print("Model trained successfully")

# Feature extraction
def extract_features_from_url(url):
    features = []

    try:
        socket.gethostbyname(urlparse(url).netloc)
        features.append(1)
    except:
        features.append(-1)

    if len(url) < 54:
        features.append(1)
    else:
        features.append(-1)

    if "@" in url:
        features.append(-1)
    else:
        features.append(1)

    if "-" in urlparse(url).netloc:
        features.append(-1)
    else:
        features.append(1)

    if url.startswith("https"):
        features.append(1)
    else:
        features.append(-1)

    while len(features) < X.shape[1]:
        features.append(1)

    return features

# Flask app
app = Flask(__name__)

HTML_PAGE = """
<html>
<head>
<title>Phishing Detector</title>
</head>
<body style="text-align:center; font-family:Arial;">
<h2>Phishing Website Detection System</h2>

<form method="post">
<input type="text" name="url" placeholder="Enter website URL" size="40" required>
<br><br>
<input type="submit" value="Check Website">
</form>

<h3>{{ result }}</h3>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    result = ""
    if request.method == "POST":
        url = request.form["url"]
        try:
            features = extract_features_from_url(url)
            prediction = model.predict([features])[0]

            if prediction == -1:
                result = "This Website is PHISHING"
            else:
                result = "This Website is SAFE"
        except:
            result = "Invalid URL or error"

    return render_template_string(HTML_PAGE, result=result)

if __name__ == "__main__":
    app.run(debug=True)
