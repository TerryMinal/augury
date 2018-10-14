# Importing Modules
import csv
from db import get_tweets
from stock_data import company_info
from sklearn import datasets
import numpy as np
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import sentiment

companies = {}
with open('companies.txt', 'r') as f:
    file = csv.reader(f, delimiter=',')
    for row in file:
        if "#" not in row[0]:
            companies[row[len(row) - 1]] = row[0]

# print("companies", companies)
# Loading dataset
def getData(comp, limiter):
    # print(comp)
    # make dataList and ret
    ret = []
    tweetsList = []
    # get data from sql
    tweets = get_tweets()
    count = 0
    # print("comp", comp)
    for tweet in tweets:
        if count == limiter:
            break
        # print(tweet[1])
        if tweet[1].rstrip("\n") == comp:
            tweetsList.append(tweet[2])
        count += 1
    # print(tweetsList)
    sent = sentiment.sentimentList(tweetsList, comp)
    # print(sent["score"])
    sent["magnitude"] = sentiment.normalize(sent["magnitude"])
    sent = sentiment.aggregateData(sent)
    global companies
    sym = companies[comp]
    cmp = company_info(sym)
    # print(cmp)
    ret = [sent["score"], sent["magnitude"], cmp["revenue"], cmp["eps"], cmp["roe"]]
    return ret
    # get data from stock info and put into dataList
    # append dataList to ret

def getAllData(companies, limiter):
    ret = []
    for company in companies:
        ret.append(getData(company, limiter))
    return ret

def trainModel(dataset):
    # Declaring Model
    model = KMeans(n_clusters=3, random_state = 0)
    model.fit(dataset)
    joblib.dump(model, "model.joblib")
    return model


def getModel():
    return joblib.load("model.joblib")

# pass in array in this form: [score, magnitude, revenue, earnings per share, return on equity]
def predict(arr):
    model = getModel()
    return model.predict(arr)
# b is an int of desired prediction. 0: sell, 1:neutral, 2: buy
def recommend(b):
    global companies
    for comp in companies.keys():
        x = np.array(getData(comp, 100))
        pred = predict([x])
        pred = pred.tolist()
        if pred == [b]:
            return comp

if __name__ == "__main__":
    # dataset = np.array(getAllData(companies.keys(), 400))
    # trainModel(dataset)
    # print(predict([np.array(getData("Tesla", 300))]))
    print(recommend(1))
# print(dataset)
# dataset = getAllData(companies.keys())
# use np.array
# parameters: semantic analysis score, semantic analysis magnitude, revenue, earnings per share, return on equity
# Fitting Model

# Predicitng a single input
# pred = model.predict([[-.25, 40000000000000, 15000000000000, 15000000, 150000000]])
# print(pred)

# Prediction on the entire data
# all_predictions = model.predict()

# Printing Predictions
# print(predicted_label)
# print(all_predictions)
