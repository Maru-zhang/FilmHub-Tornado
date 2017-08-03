from core.cache.basecache import BaseCache
from core.logger_helper import logger


class WxMediaCache(BaseCache):
    """
    media缓存

    set_cache               添加redis
    get_cache               获取redis
    """
    _expire_media_token = 3 * 24 * 3600

    def set_cache(self, key, value):
        """添加微信Media相关redis"""
        res = self.redis_ctl.set(key, value)
        self.redis_ctl.expire(key, self._expire_media_token)
        logger.debug('【微信media缓存】setCache>>>key[' + key + '],value[' + value + ']')
        return res

    def get_cache(self, key):
        """获取redis"""
        try:
            v = (self.redis_ctl.get(key)).decode('utf-8')
            logger.debug(v)
            logger.debug('【微信Meida缓存】getCache>>>key[' + key + '],value[' + v + ']')
            return v
        except Exception:
            return None
