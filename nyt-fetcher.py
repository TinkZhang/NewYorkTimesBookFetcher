import firebase_admin
import requests
import json
import sys
from types import SimpleNamespace
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("readkeeper-1322-firebase-adminsdk-vlxo8-25085b88e6.json")
firebase_admin.initialize_app(cred, {
    'projectId': "readkeeper-1322"
})

db = firestore.client()

# Fiction
doc_ref = db.collection(u'Fictions')
response = requests.get('https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-fiction.json?api-key='+sys.argv[1]).text
re = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
print(re.results.published_date)
books = re.results.books
list = []
def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(batch_size).stream()
    deleted = 0

    for doc in docs:
        doc.reference.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

delete_collection(doc_ref, 15)
for i in range(len(books)):
    book = {
        'title': books[i].title, 
        'author': books[i].author, 
        'bookImage': books[i].book_image,
        'description': books[i].description,
        'rank': books[i].rank,
        'rankLastWeek': books[i].rank_last_week,
        'weeksOnList': books[i].weeks_on_list,
        'amazonProductUrl': books[i].amazon_product_url,
    }
    doc_ref.add(book)
# NonFiction
doc_ref = db.collection(u'NonFictions')

response = requests.get('https://api.nytimes.com/svc/books/v3/lists/current/combined-print-and-e-book-nonfiction.json?api-key='+sys.argv[1]).text
re = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
print(re.results.published_date)
books = re.results.books
list = []
delete_collection(doc_ref, 15)
for i in range(len(books)):
    book = {
        'title': books[i].title, 
        'author': books[i].author, 
        'bookImage': books[i].book_image,
        'description': books[i].description,
        'rank': books[i].rank,
        'rankLastWeek': books[i].rank_last_week,
        'weeksOnList': books[i].weeks_on_list,
        'amazonProductUrl': books[i].amazon_product_url,
    }
    doc_ref.add(book)