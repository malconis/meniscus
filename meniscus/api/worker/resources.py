import json
import falcon
import uwsgi

from meniscus.api import ApiResource, load_body


class VersionResource(ApiResource):
    """ Return the current version of the Worker API """

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'v1': 'current'})


class ConfigurationResource(ApiResource):
    """
    Webhook callback for the Coordinator to send the
    latest configuration settings
    """

    def on_post(self, req, resp):
        body = load_body(req)

        if uwsgi.cache_exists('configuration'):
            uwsgi.cache_update('configuration', str(body))
        else:
            uwsgi.cache_set('configuration', str(body))

        resp.status = falcon.HTTP_202
