# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        aged_brie = "Aged Brie"
        legendary_item = "Sulfuras, Hand of Ragnaros"
        backstage_pass = "Backstage passes to a TAFKAL80ETC concert"
        conjured = "Conjured"

        max_quality_increase = 50

        for item in self.items:

            if item.name == aged_brie:
                if item.sell_in >= 0:
                    quality_delta = 1
                else:
                    quality_delta = 2

                # Decrement sell in time
                item.sell_in -= 1

            elif item.name == legendary_item:
                quality_delta = 0

            elif item.name == backstage_pass:
                if item.sell_in <= 0:
                    quality_delta = -1 * item.quality
                elif item.sell_in <= 5:
                    quality_delta = 3
                elif item.sell_in <= 10:
                    quality_delta = 2
                else:
                    quality_delta = 1

                item.sell_in -= 1

            # The rest of the items' behavior
            else:
                if item.sell_in <= 0:
                    quality_delta = -2
                else:
                    quality_delta = -1

                item.sell_in -= 1


            # We shouldn't be able to exceed 50
            if item.quality + quality_delta <= max_quality_increase:
                item.quality += quality_delta
            # Quality cannot go negative
            if item.quality < 0:
                item.quality = 0


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
