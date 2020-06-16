from scrapy.extensions.httpcache import FilesystemCacheStorage as FCS

class FilesystemCacheStorage(FCS):
    def __init__(self, *a, **kw):
        super(FilesystemCacheStorage, self).__init__(*a, **kw)

    def _read_meta(self, spider, request):
        meta = super(FilesystemCacheStorage, self)._read_meta(spider, request)
        request.meta['stored_meta'] = meta
        return meta
