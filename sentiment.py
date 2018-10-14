import sys
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#text and entity are both strings
def sentimentText(text, entity):
    text = text.lower()
    entity = entity.lower()
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(content=text.encode('utf-8'),type=enums.Document.Type.HTML, language="EN")

    # Detect and send native Python encoding to receive correct word offsets.
    encoding = enums.EncodingType.UTF32 #checks encoding is correct
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    result = client.analyze_entity_sentiment(document, encoding)
    entities = result.entities
    for ent in entities:
        if ent.name == entity and ent is not None:
            return {"score": ent.sentiment.score, "magnitude": ent.sentiment.magnitude}
    return {"score": 0.0, "magnitude": 0.0}
    # ret = result.entities[]
    #     returns a format similar to this: ranked by salience
    #     {
    #   "entities": [
    #     {
    #       "name": "R&B music",
    #       "type": "WORK_OF_ART",
    #       "metadata": {},
    #       "salience": 0.5306305,
    #       "mentions": [
    #         {
    #           "text": {
    #             "content": "R&B music",
    #             "beginOffset": 7
    #           },
    #           "type": "COMMON",
    #           "sentiment": {
    #             "magnitude": 0.9,
    #             "score": 0.9
    #           }
    #         }
    #       ],
    #       "sentiment": {
    #         "magnitude": 0.9,
    #         "score": 0.9
    #       }
    #     },
    #   ],
    #   "language": "en"
    # }
    # for entity in result.entities:
    #     print('Mentions: ')
    #     print(u'Name: "{}"'.format(entity.name))
    #     for mention in entity.mentions:
    #         print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
    #         print(u'  Content : {}'.format(mention.text.content))
    #         print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
    #         print(u'  Sentiment : {}'.format(mention.sentiment.score))
    #         print(u'  Type : {}'.format(mention.type))
    #     print(u'Salience: {}'.format(entity.salience))
    #     print(u'Sentiment: {}\n'.format(entity.sentiment))

# returns list of sentiment data in form [score, magnitude]
def sentimentList(data, entity):
    score = []
    magnitude = []
    for text in data:
        curSent = sentimentText(text, entity)
        # print("cursent",curSent)
        score.append(curSent["score"])
        magnitude.append(curSent["magnitude"])
    magnitude.sort()
    return {"score":score, "magnitude":magnitude}

# assumes data is sorted
# uses x = (x-xmin)/(xmax - xmin)
# perform on magnitude
def normalize(data):
    if len(data) == 0:
        return [0]
    xmax = data[len(data) - 1]
    xmin = data[0]
    if xmax - xmin <= 0:
        return data
    for index in range(0, len(data)):
        data[index] = float( (data[index]-xmin)/(xmax - xmin) )
    return data

# adds up all the scores takes the median of the list of magnitude
def aggregateData(data):
    totalScore = 0
    for score in data["score"]:
        totalScore += score
    midpoint = len(data["magnitude"])/2
    return {"score": totalScore, "magnitude": data["magnitude"][int(midpoint)]}

if __name__ == "__main__":
    str = "Stocks on Wall Street tumbled again on Thursday, as choppy early trading gave way to another bout of broad-based selling.\
    The declines were widespread, touching everything from previously high-flying tech shares to usually insulated sectors like consumer staples and utilities. \
    When the dust settled, every sector of the Standard & Poor’s 500-stock index had dropped, leaving the stock market benchmark down an additional 2.1 percent. \
    That slump followed Wednesday’s 3.3 percent decline, which was the market’s biggest dive in eight months."
    li = ["But the short bet against Tesla has worked out well for Einhorn. The stock plunged nearly 25% during the third quarter and #Einhorn wrote that it was his fund's second best performer. Tesla shares were down another 7% on Friday",\
    "Tesla needs over $1 billion in cash over the next 6 months, and Wall Street is going nuts figuring out where it's going to come from"]
    # print(sentimentText(li[1], "tesla"))
    # print(sentimentList(li, "tesla"))
    # print(normalize([1,2,3,4,7,9,11,12,71, 52]))
    # print(aggregateData(sentimentList(li, "tesla")))
