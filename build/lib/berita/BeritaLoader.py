from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join

class BeritaLoader(ItemLoader):

    default_output_processor = Join()

    name_in = MapCompose(unicode.title)
    name_out = Join()

    #price_in = MapCompose(unicode.strip)

    # ...