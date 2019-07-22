from urllib.request import urlopen, URLError
from bs4 import BeautifulSoup
from soupsieve import SelectorSyntaxError
from aggregator.plugin import Plugin, StringParam


class FramePlugin(Plugin):

    __pluginname__ = 'frame'
    __location__ = __file__
    __paramschema__ = (
        StringParam('url', 'Address of page.'),
        StringParam('selector', 'CSS selector.')
    )

    def get_payload(self):
        payload = {'html': ''}
        if self.params['url']:
            try:
                response = urlopen(self.params['url'])
                if response.getcode() == 200:
                    soup = BeautifulSoup(response.read(), 'html.parser')
                    try:
                        selection = soup.select(self.params['selector'], limit=1)
                        if selection:
                            payload['html'] = selection[0].prettify(formatter='minimal')
                    except SelectorSyntaxError:
                        pass
            except URLError:
                pass
        return payload
