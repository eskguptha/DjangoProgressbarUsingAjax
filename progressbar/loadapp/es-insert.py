import json
import os
import csv
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch import client
from elasticsearch import exceptions
from elasticsearch import exceptions, ImproperlyConfigured, ElasticsearchException
from elasticsearch_dsl import connections, DocType, Search
connections.connections.configure(
    default={'hosts': "http://192.168.43.90:9200"},
)
class User(DocType):
    pass
es = Elasticsearch("192.168.43.90:9200")

account_id = "test_1"
doc_list = []
index_client = client.IndicesClient(es)
if not index_client.exists(index=account_id):
	index_client.create(index=account_id)
index_client.refresh(index=account_id)
doc = {
"_index": account_id,
"_type": 'user',
"_id": 2,
"doc": {"name":"test123","id":2}
    }
doc_list.append(doc)
helpers.bulk(es, doc_list)