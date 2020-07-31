from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        return redirect(url_for("results", youtubeUrl=url))
    else:
        return render_template("index.html")

@app.route("/<youtubeUrl>/")
def results(youtubeUrl):
    return f"<h1>{youtubeUrl}</h1>"

if __name__ == "__main__":
    app.run(debug=True) 