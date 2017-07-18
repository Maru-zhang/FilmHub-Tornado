import requests
from core.cache.tokencache import TokenCache

class WdAPI(self):
    
    baseURL = 'https://api.vdian.com/api'
    _token_cache = TokenCache()
    
    def fetch

    def getAccessToken(self):
        return _token_cache.get_cache(self._token_cache.KEY_WD_ACCESS_TOKEN)
