from boto.dynamodb2.layer1 import DynamoDBConnection

from .settings import conf

__all__ = 'init_bynamodb'


def init_bynamodb(config=None, **kwargs):
    if config is None:
        config = dict()
    config.update(kwargs)
    conf.load_settings_from(config)
    _patch_dynamodb_connection(
        host=conf.get('host'),
        port=conf.get('port'),
        is_secure=conf.get('is_secure')
    )


def _patch_dynamodb_connection(**kwargs):
    """:class:`boto.dynamodb2.layer1.DynamoDBConnection` patcher.

    It partially applies the keyword arguments to the
    :class:`boto.dynamodb2.layer1.DynamoDBConnection` initializer method.
    The common usage of this function would be patching host and port
    to the local DynamoDB or remote DynamoDB as the project configuration
    changes.

    """
    if hasattr(DynamoDBConnection, '__original_init__'):
        return

    DynamoDBConnection.__original_init__ = DynamoDBConnection.__init__

    def init(self, **fkwargs):
        fkwargs.update(kwargs)
        self.__original_init__(**fkwargs)

    DynamoDBConnection.__init__ = init
