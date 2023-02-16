"""
Main page routes.
"""

from ..rapid.myapi import get_email
from flask import render_template, Blueprint, request
import requests
import json
import uuid
import os

from . import main


myBid = "162594"  # This value can be changed to use your own bot
myKey = "HfLCrXnUDD9vjUpz"  # This value can be changed to use your own bot

# main = Blueprint("main", __name__)


@main.route("/get-email/<url>")
def email(url):
    return get_email(url)


@main.route("/")
@main.route("/home")
def home():
    return render_template("index.html")


@main.route("/about")
def abouts():
    return render_template("about.html")


@main.route("/content")
def content():
    API_KEY = "AIzaSyCxc5Y6p6oGAzsDi0kD9rZGqSIlwHdIzh0"
    channel_id = "UCIFbnPw_X_gdz4ai2U9-TFQ"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=50&type=video&key={API_KEY}"
    response = requests.get(url)
    videos = []
    if response.status_code == 200:
        data = json.loads(response.content.decode("utf-8"))
        for item in data["items"]:
            video = {
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "video_id": item["id"]["videoId"],
            }
            videos.append(video)
    # return videos
    return render_template("content.html", videos=videos)


@main.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


def serial_num():
    var = str(uuid.uuid1(uuid.getnode(), 0))[24:]
    try:
        username = os.getlogin()
    except Exception as e:
        print(e)
        print("Unable to get username")
        username = "Unknown User"
    var = var + "+" + username
    print(var)
    return var


@main.route("/get")
# function for the bot response
def get_bot_response():
    userText = request.args.get('msg')
    answer = give_answer(userText)
    return str(answer)


def give_answer(givenText):
    uid = serial_num()
    url = "http://api.brainshop.ai/get?bid=" + myBid + "&key=" + myKey + "&uid=" + uid + "&msg=" + givenText
    response = requests.get(url)
    parsed = json.loads(response.text)['cnt']
    print(parsed)
    return parsed


@main.errorhandler(404)
def pageNotFound(error):
    page_title = f"{error.code} - page not found !"
    return render_template(
        'page/error.html',
        page_title=page_title,
        error=error
    ), 404


@main.errorhandler(500)
def internalServerError(error):
    page_title = f"{error.code} - few things went wrong"
    return render_template(
        'page/error.html',
        page_title=page_title,
        error=error
    ), 500


@main.errorhandler(400)
def keyError(error):
    page_title = f"{error.code} - invalid request resulted in KeyError."
    return render_template(
        'page/error.html',
        page_title=page_title,
        error=error
    ), 400
