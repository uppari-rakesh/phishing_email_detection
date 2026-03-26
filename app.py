from flask import Flask, render_template, request
import pickle
from scipy.sparse import hstack, csr_matrix

app = Flask(__name__)

model = pickle.load(open("model/phishing_model.pkl","rb"))
tfidf = pickle.load(open("model/tfidf.pkl","rb"))

@app.route("/", methods=["GET","POST"])
def index():
    prediction = None
    probability = None

    if request.method == "POST":
        email = request.form.get("email")

        # ✅ EMPTY INPUT HANDLE
        if not email:
            return render_template("index.html",
                                   prediction="No input provided ❌",
                                   probability=0)

        vec = tfidf.transform([email])

        meta = csr_matrix([[len(email), email.count("http")]])
        final = hstack([vec, meta])

        pred = model.predict(final)[0]
        prob = model.predict_proba(final)[0][1]

        prediction = "Phishing " if pred == 1 else "Legitimate "
        probability = round(prob * 100, 2)

    return render_template("index.html",
                           prediction=prediction,
                           probability=probability)

if __name__ == "__main__":
    app.run(debug=True)