from config import FIRESTORE_CERT

import pprint

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def main():
    cred = credentials.Certificate(FIRESTORE_CERT)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    docs = db.collection('companies').get()

    print(docs)
    for doc in docs:
        print(doc)
        pprint(doc.to_dict())

main()
