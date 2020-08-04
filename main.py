import getChannelInfo
from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("results", youtubeUrl = request.form["url"].split('.com/')[-1]))
    else:
        return render_template("home.html")

@app.route("/<youtubeUrl>/", methods=["POST","GET"])
def results(youtubeUrl):
    if request.method == "POST":
        return redirect(url_for("results", youtubeUrl = request.form["url"].split('.com/')[-1]))
    elif 'watch?v=' in youtubeUrl:
        channelInfos = getChannelInfo.getChannelInfo(youtubeUrl)
        return render_template("result.html", channelNameToHtml = channelInfos[0], channelViewsToHtml = channelInfos[1],
                                              channelSubsToHtml = channelInfos[2])
    else:
        return redirect(url_for("wrongUrl", channelNameToHtml = youtubeUrl))

@app.route("/erro/", methods=["POST", "GET"])
def wrongUrl():
    if request.method == "POST":
        return redirect(url_for("results", youtubeUrl = request.form["url"].split('.com/')[-1]))
    else:
        return render_template("erro.html")

if __name__ == "__main__":
    app.run(debug=True)