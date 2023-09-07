from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", launches=launches)

@app.template_filter("date_only")
def date_only_filter(s):
    date_object = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return date_object.date()

def fetch_spacex_launches():
    url = "https://api.spacexdata.com/v4/launches" # this url has json object of all launches
    response = requests.get(url)
    if response.status_code == 200:
        return response.json() # will contain python dictionary of launches
    else:
        return []
    
def categorize_launches(launches):

    successful = list(filter(lambda x: x["success"] and not x["upcoming"], launches)) # filter will take all of the launches, look at the anonymous lambda function, and if function returns true it will take that data and add it into the filtered list. x represents the current iteration launch, and ["upcoming"] sees if that launch object has an "upcoming" key, if it does the expression will return true
    failed = list(filter(lambda x: not x["success"] and not x["upcoming"], launches))
    upcoming = list(filter(lambda x: x["upcoming"], launches))


    return {
        "successful": successful,
        "failed": failed,
        "upcoming": upcoming

    }
    
launches = categorize_launches(fetch_spacex_launches())


if __name__ == "__main__":
    app.run(debug=True)