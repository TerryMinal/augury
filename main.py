# remember to source GOOGLE_APPLICATION_CREDENTIALS=PATH TO AUGURY JSON
import ml
import time
from generate_post import create_post
import twitter

def updateModel():
    # UPDATE TWITTER HERE
    twitter.run()
    ml.updateModel()

def generatePost():
    # put in a desired rating into recommend
    rec = ml.recommend(0)
    # rec[0] is company name, rec[1] is rating
    create_post(rec[0], rec[1])

def main():
    while True:
        updateModel()
        generatePost()

        time.sleep(60*15)

main()
