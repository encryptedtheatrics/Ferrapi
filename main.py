from fastapi import FastAPI, Response
import requests
import random
import datetime

app = FastAPI()#
app_start = datetime.datetime.now()
@app.get("/")
def root():
    uptime = datetime.datetime.now() - app_start;
    return {"what": "This is an API that returns images of Ferrets!", "who": "made by @transfem on github (https://github.com/transfem)", "uptime": "{} days, {} hours, {} minutes, {} seconds".format(uptime.days, uptime.seconds//3600, (uptime.seconds//60)%60, uptime.seconds%60)}

@app.get("/ferret")
def get_ferret(display: str = "false"):
    # fetch posts from ferrets subreddit
    posts = requests.get("https://www.reddit.com/r/ferrets.json?limit=100", headers = {'User-agent': 'ferret-api'}).json()
    
    #sort the posts to only include images
    sorted_posts = []
    for post in posts["data"]["children"]:
        try:
            if post["data"]["post_hint"] == "image":
                sorted_posts.append(post)
        except KeyError:
            continue
            
    # get a random post from the list of posts
    random_post = random.choice(sorted_posts)

    # get the image url from the random post
    image_url = random_post["data"]["url"]
      
    # if the display parameter is set, request the image from the url and return it
    if display == "true":
        image = requests.get(image_url)
        return Response(content=image.content, media_type=image.headers["Content-Type"])
    
    return {"post_title": random_post["data"]["title"], "image_url": image_url}