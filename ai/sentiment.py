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
        if ent.name == entity:
            return [ent.sentiment.score, ent.sentiment.magnitude]
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
# assumes data is sorted
# uses x = (x-xmin)/(xmax - xmin)
def normalizeData(data):
    xmax = data[len(data) - 1]
    xmin = data[0]
    for index in range(0, len(data)):
        data[i] = float( (data[i]-xmin)/(xmax - xmin) )
    return data

# takes the median of the data
def aggregateData(data):
    midpoint = len(data)/2
    return data[midpoint]

# returns list of sentiment data
def sentimentList(data, entity):
    ret = []
    for text in data:
        ret.append(sentimentText(text, entity))
    return ret

if __name__ == "__main__":
    str = "Stocks on Wall Street tumbled again on Thursday, as choppy early trading gave way to another bout of broad-based selling.\
    The declines were widespread, touching everything from previously high-flying tech shares to usually insulated sectors like consumer staples and utilities. \
    When the dust settled, every sector of the Standard & Poor’s 500-stock index had dropped, leaving the stock market benchmark down an additional 2.1 percent. \
    That slump followed Wednesday’s 3.3 percent decline, which was the market’s biggest dive in eight months."
    print(sentimentText(str, "stocks"))
