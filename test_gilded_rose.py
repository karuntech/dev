# -*- coding: utf-8 -*-
import unittest

import gilded_rose
from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("foo", items[0].name)
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual("foo, -1, 0", str(items[0]))

    def test_agedbrie(self):
        items = [Item("Aged Brie", 10, 49)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)
        self.assertEqual(9, items[0].sell_in)

        items = [Item("Aged Brie", -1, 48)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)
        self.assertEqual(-2, items[0].sell_in)


        #gilded_rose.update_quality()
        #self.assertEqual(50, items[0].quality)



    def test_qualit_not_morethan50(self):
        items = [Item("foo", 1, 51), Item("Aged Brie", 1, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)
        self.assertEqual(50, items[1].quality)

    def test_spoilspeed(self):
        items = [Item("foo", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(9, items[0].quality)
        gilded_rose.update_quality()
        self.assertEqual(-1, items[0].sell_in)
        self.assertEqual(7, items[0].quality)

    def test_Sulfuras(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 1000, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(1000, items[0].sell_in)

    def test_backstage(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 11, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(11, items[0].quality)
        self.assertEqual(10, items[0].sell_in)

        gilded_rose.update_quality()
        self.assertEqual(13, items[0].quality)
        self.assertEqual(9, items[0].sell_in)

        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        self.assertEqual(21, items[0].quality)
        self.assertEqual(5, items[0].sell_in)

        gilded_rose.update_quality()
        self.assertEqual(24, items[0].quality)
        self.assertEqual(4, items[0].sell_in)

        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)


if __name__ == '__main__':
    unittest.main()
