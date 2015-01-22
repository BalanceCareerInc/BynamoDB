# -*-coding:utf8-*-
import inspect
import json
import os
from boto.dynamodb2.layer1 import DynamoDBConnection
from bynamodb.model import Model


def init_tables(models_module):
    models = [getattr(models_module, name) for name in dir(models_module)]
    models = [model for model in models
              if inspect.isclass(model) and issubclass(model, Model) and not model == Model]

    conn = DynamoDBConnection()
    table_names = conn.list_tables()['TableNames']
    for model in models:
        if getattr(model, 'skip_create', False):
            continue
        if model.get_table_name() in table_names:
            continue
        model.create_table()
        [load_fixture(model, fixture) for fixture in getattr(model, '__fixtures__', [])]


def load_fixture(model, fixture):
    with open(os.path.join('fixtures', '%s.json' % fixture), 'r') as f:
        for row in json.loads(f.read()):
            model.put_item(**row)
