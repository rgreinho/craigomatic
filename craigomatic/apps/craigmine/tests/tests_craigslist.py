from datetime import datetime

from django.utils import timezone
from django.test import TestCase
from lxml import html

from craigmine.craigslist import Craigslist
from craigmine.craigslist import CraigslistItem
from craigmine.craigslist import querystring_to_dict
from craigmine.tests.ad_samples import FULL_RESULT_PAGE_FIXIES
from craigmine.tests.ad_samples import HOUSING_AD_00
from craigmine.tests.ad_samples import HOUSING_AD_01


class CraigslistTestCase(TestCase):
    def setUp(self):
        self.doc = html.document_fromstring(FULL_RESULT_PAGE_FIXIES)
        self.cl = Craigslist('fake_server', 'fake_query')

    def test_items(self):
        items = self.cl.items(self.doc)
        self.assertIsNotNone(items)

    def test_parse_items(self):
        items = self.cl.items(self.doc)
        parsed_items = self.cl.parse_items(items)
        self.assertIsNotNone(parsed_items)


class CraigslistItemTestCase_02(TestCase):
    def setUp(self):
        doc = html.document_fromstring(HOUSING_AD_00)
        item_root = doc.xpath('//p')
        self.cl_item = CraigslistItem(item_root[0])

    def test_link(self):
        actual = self.cl_item.link()
        expected = '/apa/5505576050.html'
        self.assertEqual(actual, expected)

    def test_pnr(self):
        actual = self.cl_item.pnr()
        expected = 'Round Rock / Pflugerville'
        self.assertEqual(actual, expected)

    def test_post_id(self):
        actual = self.cl_item.id()
        expected = '5505576050'
        self.assertEqual(actual, expected)

    def test_post_date(self):
        actual = self.cl_item.published_date()
        expected = timezone.make_aware(datetime(2016, 3, 27, 19, 3))
        self.assertEqual(actual, expected)

    def test_price(self):
        actual = self.cl_item.price()
        expected = '1029'
        self.assertEqual(actual, expected)

    def test_title(self):
        actual = self.cl_item.title()
        expected = 'Round Rock, Forest Creek Area,'
        self.assertEqual(actual, expected)


class CraigslistItemTestCase_01(TestCase):
    def setUp(self):
        doc = html.document_fromstring(HOUSING_AD_01)
        item_root = doc.xpath('//p')
        self.cl_item = CraigslistItem(item_root[0])

    def test_link(self):
        actual = self.cl_item.link()
        expected = '/apa/5458670201.html'
        self.assertEqual(actual, expected)

    def test_pnr(self):
        actual = self.cl_item.pnr()
        expected = 'East Campus'
        self.assertEqual(actual, expected)

    def test_post_id(self):
        actual = self.cl_item.id()
        expected = '5458670201'
        self.assertEqual(actual, expected)

    def test_post_date(self):
        actual = self.cl_item.published_date()
        expected = timezone.make_aware(datetime(2016, 2, 21, 19, 34))
        self.assertEqual(actual, expected)

    def test_price(self):
        actual = self.cl_item.price()
        expected = '2695'
        self.assertEqual(actual, expected)

    def test_title(self):
        actual = self.cl_item.title()
        expected = 'Prelease For August 2016 - 4 Bedroom Close To UT campus'
        self.assertEqual(actual, expected)


class OtherFunctionsTestCase(TestCase):
    def test_querystring_to_dict_00(self):
        querystring = 'sort=date&bathrooms=3'
        actual = querystring_to_dict(querystring)
        expected = {'sort': 'date', 'bathrooms': '3'}
        self.assertEqual(actual, expected)

    def test_querystring_to_dict_01(self):
        querystring = 'housing_type=6&housing_type=9&max_price=1000'
        actual = querystring_to_dict(querystring)
        expected = {'housing_type': ['6', '9'], 'max_price': '1000'}
        self.assertEqual(actual, expected)
