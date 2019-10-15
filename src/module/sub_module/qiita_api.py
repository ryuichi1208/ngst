import requests
import yaml


class QiitaClientBase():
    HOST = 'qiita.com'
    USER_AGENT = 'Qiita python3 binding'
    ACCEPT = 'application/json'
    HEADER = {
        'Accept': ACCEPT,
        'User-Agent': USER_AGENT,
    }

    def __init__(self, config_file=None, access_token=None, team=None):
        if not config_file and (not access_token):
            raise Exception('input config_file or access_token')
        self.access_token = access_token
        self.team = team
        if config_file:
            with open(config_file, 'r') as f:
                config = yaml.load(f)
                if 'ACCESS_TOKEN' in config:
                    self.access_token = config['ACCESS_TOKEN']
                if 'TEAM' in config:
                    self.team = config['TEAM']

    def _url_prefix(self):
        if self.team:
            return 'https://{}.{}/api/v2'.format(self.team, self.HOST)
        else:
            return 'https://{}/api/v2'.format(self.HOST)

    def header(self):
        if self.access_token:
            self.HEADER.update(
                {'Authorization': 'Bearer {}'.format(self.access_token)})
        return self.HEADER

    def _request(self, method, url, params=None, headers=None):
        headers = self.header() if headers is None else headers
        if type(headers) is not dict:
            return TypeError('headers must be dictionary')

        method = method.upper()
        if method in ('GET', 'DELETE'):
            response = requests.request(
                method=method, url=url, headers=headers, params=params)
        elif method in ('POST', 'PUT', 'PATCH'):
            response = requests.request(
                method=method, url=url, headers=headers, json=params)
        else:
            raise Exception('Unknown method')

        if response.ok:
            return QiitaResponse(response)
        else:
            raise QiitaApiException(response.json())

    def request(self, method, path, params=None, headers=None):
        url = self._url_prefix() + path
        return self._request(method, url, params, headers)

    def get(self, path, params=None, headers=None):
        return self.request('GET', path, params, headers)

    def post(self, path, params=None, headers=None):
        return self.request('POST', path, params, headers)

    def put(self, path, params=None, headers=None):
        return self.request('PUT', path, params, headers)

    def patch(self, path, params=None, headers=None):
        return self.request('PATCH', path, params, headers)

    def delete(self, path, params=None, headers=None):
        return self.request('DELETE', path, params, headers)

def test(access_token):
    import doctest
    doctest.testmod(
        extraglobs={'client': QiitaClientBase(access_token=access_token)})

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            if len(sys.argv) > 2:
                access_token = sys.argv[2]
            else:
                import os
                access_token = os.environ['QIITA_ACCESS_TOKEN']
            test(access_token)
