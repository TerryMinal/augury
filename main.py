# remember to source GOOGLE_APPLICATION_CREDENTIALS=PATH TO AUGURY JSON
import ml
from generate_post import create_post

def updateModel():
    # UPDATE TWITTER HERE
    ml.updateModel()

def generatePost():
    # put in a desired rating into recommend
    rec = ml.recommend(0)
    # rec[0] is company name, rec[1] is rating
    create_post(rec[0], rec[1])
