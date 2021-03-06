from meniscus.data.datastore import datasource_handler, DEFAULT_SINK
from meniscus import env
from meniscus.queue import celery


_LOG = env.get_logger(__name__)

_db_handler = datasource_handler(DEFAULT_SINK)


@celery.task(acks_late=True, max_retries=None,
             ignore_result=True, serializer="json")
def persist_message(message):
    """Takes a message and persists it to the default datastore."""
    try:
        sink = _db_handler
        sink.put('tenant/{}'.format(message['meniscus']['tenant']), message)
    except Exception as ex:
        _LOG.exception(ex.message)
        persist_message.retry()
