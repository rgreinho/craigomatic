from datetime import datetime
import re

from django.utils import timezone
from lxml import html
import requests


class Craigslist:
    """
    Provides a nice interface to query Craigslist.

    :param str server: the CL server to query
    :param dict params: a dictionary caontianing the parameter of the requestS
    """
    RESULT_PER_PAGE = 100

    def __init__(self, server, query, params=None):
        self.server = server
        self.query = query
        self.params = {"s": 0, "sort": "date"}
        if params:
            self.params.update(params)
        self.current_page = 0
        self.url = "http://{}/search/{}".format(self.server, self.query)

    def html_document(self, page=0):
        """
        Returns an HTML document representing the result page of the query.

        :param int page: the page number to query
        :returns: The HTML elements containing the items.
        """
        # Set the page number to query.
        self.current_page = page

        # Request the page.
        r = requests.get(self.url, params=self.params)
        r.raise_for_status()

        # Parse the returned HTML.
        html_document = html.document_fromstring(r.text)

        # # Retrieve the HTML elements corresponding to the items.
        return html_document

    def items(self, html_document):
        """
        Returns all the items available on the requested page.

        :param html_document: HTML document containing the items
        :returns: a list of p html elements representing the all items on the requested page.
        """
        # Retrieve the HTML elements corresponding to the items.
        items = html_document.xpath("//div[@class='content']/p")
        return items

    def parse_items(self, items):
        """
        Parses all the items from the specified page.

        The dictionary produced by this function has a key represented by the post ID, and the value is a
        CraigslistItem object.

        This function ignores the items containing invalid data.

        :param items: a list of p html elements representing the all items on the requested page
        :returns: A dictionary containing all the parsed items from the specified page.
        """
        item_dict = {}
        for item in items:
            try:
                cl_item = CraigslistItem(item)
                cl_item_parsed = cl_item.to_dict()
                cl_item_parsed["full_link"] = "http://{}{}".format(self.server, cl_item_parsed["link"])
                item_dict[cl_item_parsed['clid']] = cl_item_parsed
            except ValueError:
                pass

        return item_dict

    def query_n_parse(self):
        """
        Queries and parses the items.

        This is a convenience function, making it easy to query a page and parse the results in one line.

        :returns: A dictionary containing all the parsed items from the specified page.
        """
        # Retrieve the items.
        html_document = self.html_document()
        items = self.items(html_document)

        # Parse the items.
        requested_items = self.parse_items(items)
        return requested_items


class CraigslistItem:
    """
    Represents a generic CraigsList item.

    This class can parse any CL item from any section. It handles only the values that are common between all of them.

    :param html_item: the html p element containing the summary of the item to parse.
    """
    COMPILED_PRICE_PATTERN = re.compile('([0-9]+)')

    def __init__(self, html_item):
        self.item = html_item

    def link(self, raw=False):
        """
        Returns the link of the post.

        This link is relative to the server where the search was performed. For instance,
        if the ful URL was http://austin.craigslist.org/apa/5510825755.html, this functions would return only
        the 'apa/5510825755.html' part.

        :param bool raw: if True, returns the raw value, otherwise returns the sanatized one
        :returns: the link of the post.
        """
        # Xpath query to find the link within the item.
        link_raw = self.item.xpath('span[@class="txt"]//span[@class="pl"]//a/@href')

        # Return the raw value if necessary.
        if raw:
            return link_raw

        # Sanitize the link.
        if not link_raw:
            raise ValueError
        elif not link_raw[0].startswith("/"):
            raise ValueError

        # Return the sanitized link.
        return link_raw[0]

    def pnr(self, raw=False):
        """
        Returns the pnr of the post.

        :param bool raw: if True, returns the raw value, otherwise returns the sanatized one
        :returns: the pnr of the post.
        """
        # Xpath query to find the pnr within the item.
        pnr_raw = self.item.xpath('span[@class="txt"]//span[@class="l2"]//span[@class="pnr"]//small/text()')

        # Return the raw value if necessary.
        if raw:
            return pnr_raw

        # Sanitize the pnr.
        if not pnr_raw:
            raise ValueError
        else:
            pnr_sane = ' '.join(pnr_raw[0].strip(' ()').split())

        # Return the sanitized pnr.
        return pnr_sane

    def id(self, raw=False):
        """
        Returns the ID of the post.

        :param bool raw: if True, returns the raw value, otherwise returns the sanatized one
        :returns: the ID of the post.
        """
        # Xpath query to find the post id within the item.
        post_id_raw = self.item.attrib['data-pid']

        # Return the post ID.
        return post_id_raw

    def published_date(self, raw=False):
        """
        Returns the published date of the post.

        Represents the dat when the post was originally published.

        :param bool raw: if True, returns the raw value, otherwise returns the sanatized one
        :returns: the published date of the post.
        """
        # Xpath query to find the published date within the item.
        published_date_raw = self.item.xpath('span[@class="txt"]//span[@class="pl"]//time//@datetime')

        # Return the raw value if necessary.
        if raw:
            return published_date_raw

        # Sanitize the published date.
        published_date_sane = None if not published_date_raw else timezone.make_aware(datetime.strptime(
            published_date_raw[0], '%Y-%m-%d %H:%M'))

        # Return the sanitized published date.
        return published_date_sane

    def price(self, raw=False):
        """
        Returns the price of the item.

        :param bool raw: if True, returns the raw value, otherwise returns the sanatized one
        :returns: the price of the item.
        """
        # Xpath query to find the price within the item.
        price_raw = self.item.xpath('span[@class="txt"]//span[@class="l2"]//span[@class="price"]/text()')

        # Return the raw value if necessary.
        if raw:
            return price_raw

        # Sanitize the price.
        price_match = self.COMPILED_PRICE_PATTERN.search(price_raw[0]) if price_raw else None
        price_sane = price_match.group(0) if price_match else None

        # Return the price.
        return price_sane

    def title(self, raw=False):
        """
        Returns the title of the post.

        :param bool raw: if True, returns the raw value, otherwise returns the sanatized one
        :returns: the title of the post
        """
        # Xpath query to find the title within the item.
        title_raw = self.item.xpath('span[@class="txt"]//span[@class="pl"]//a/span[@id="titletextonly"]/text()')

        # Return the raw value if necessary.
        if raw:
            return title_raw

        # Sanitize the title.
        title_sane = ' '.join(title_raw[0].strip().split()) if title_raw else None

        # Return the title.
        return title_sane

    def to_dict(self):
        """
        Returns a dictionary representing this item.

        The key will be the a string representing the name of the property, the value a string representing its value.

        :return: a dictionary representing this item.
        """
        item_dict = {'clid': self.id(),
                     'link': self.link(),
                     'pnr': self.pnr(),
                     'post_date': self.published_date(),
                     'price': self.price(),
                     'title': self.title()}

        return item_dict


def querystring_to_dict(querystring):
    """
    Returns a dictionary representing the query string.

    The dictionary created by this function can then be consumed directly by the requests API.

    :param str querystring: querystring to process
    :returns:a dictionary representing the query string.
    """
    # Create en empty dictionary to store the results.
    params = {}

    # Return directly if there is no quesrystring to parse.
    if not querystring:
        return params

    # Split the full querystring into parameters.
    parameters = querystring.split('&')

    # Loop through them.
    for parameter in parameters:
        # Try to split the query parameter to check whether it is a key/value pair.
        keyvalue = parameter.split('=', maxsplit=1)

        # Ensure we have a key/value pair.
        if len(keyvalue) == 2:
            existing_value = params.get(keyvalue[0])
            if existing_value:
                # Create a new or list or use the existing one.
                value_list = existing_value if isinstance(existing_value, list) else [existing_value]

                # Add the new value to the list.
                value_list.append(keyvalue[1])

                # Update the value in the dictionary.
                params[keyvalue[0]] = value_list
            else:
                params[keyvalue[0]] = keyvalue[1]
    return params
