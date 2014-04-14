from scrapy import log
from scrapy.utils.decorator import inthread
from scrapy.utils.misc import load_object

from .http import WebdriverActionRequest, WebdriverRequest, WebdriverResponse

FALLBACK_HANDLER = 'scrapy.core.downloader.handlers.http.HttpDownloadHandler'


class WebdriverDownloadHandler(object):
    """This download handler uses webdriver, deferred in a thread.

    Falls back to the stock scrapy download handler for non-webdriver requests.

    """
    def __init__(self, settings):
        self._enabled = settings.get('WEBDRIVER_BROWSER') is not None
        self._fallback_handler = load_object(FALLBACK_HANDLER)(settings)

    def download_request(self, request, spider):
        """Return the result of the right download method for the request."""
        if self._enabled and isinstance(request, WebdriverRequest):
            if isinstance(request, WebdriverActionRequest):
                download = self._do_action_request
            else:
                download = self._download_request
        else:
            download = self._fallback_handler.download_request
        return download(request, spider)

    @inthread
    def _download_request(self, request, spider):
        """Download a request URL using webdriver."""
        log.msg('Downloading %s with webdriver' % request.url, level=log.DEBUG)
        request.manager.webdriver.get(request.url)
        return WebdriverResponse(request.url, request.manager.webdriver)

    @inthread
    def _do_action_request(self, request, spider):
        """Perform an action on a previously webdriver-loaded page."""
        log.msg('Running webdriver actions %s' % request.url, level=log.DEBUG)
        request.actions.perform()
        return WebdriverResponse(request.url, request.manager.webdriver)
