from flask import Flask, render_template, jsonify
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

GOPHISH_API_KEY = "120ff98129f538e26c25840c67c71925a4fe626742c391b757a16fd32ca87e7b"
GOPHISH_URL = "https://localhost:3333/api/campaigns/"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def get_data():
    try:
        headers = {"Authorization": GOPHISH_API_KEY}
        r = requests.get(GOPHISH_URL, headers=headers, verify=False, timeout=10)
        campaigns = r.json()

        names, opens, clicks, submissions = [], [], [], []

        for camp in campaigns:
            names.append(camp.get("name", "N/A"))
            results = camp.get("results", [])
            o, c, s = 0, 0, 0
            for res in results:
                status = res.get("status", "")
                if status == "Submitted Data":
                    s += 1; c += 1; o += 1
                elif status == "Clicked Link":
                    c += 1; o += 1
                elif status == "Email Opened":
                    o += 1
            opens.append(o)
            clicks.append(c)
            submissions.append(s)

        return jsonify({"names": names, "opens": opens, "clicks": clicks, "submissions": submissions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)