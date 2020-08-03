from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("results", youtubeUrl=request.form["url"]))
    else:
        return render_template("home.html")

@app.route("/<youtubeUrl>/", methods=["POST","GET"])
def results(youtubeUrl):
    if request.method == "POST":
        return redirect(url_for("results", youtubeUrl=request.form["url"]))
    elif 'youtube.com' in youtubeUrl:
        return render_template("result.html", urlToHtml=youtubeUrl)
    else:
        return render_template("erro.html")

if __name__ == "__main__":
    app.run(debug=True) 

