#!/usr/bin/python2.4
# Copyright 2008 Google Inc. All Rights Reserved.

"""Tests for util functions."""

__author__ = 'Mark Roach (mrroach@google.com)'

import datetime
import decimal
import unittest
from pprint import pprint

from pyactiveresource import util


def diff_dicts(d1, d2):
    """Print the differences between two dicts. Useful for troubleshooting."""
    pprint([(k, v) for k, v in d2.items()
            if v != d1[k]])


class UtilTest(unittest.TestCase):
    def setUp(self):
        """Create test objects."""

    def test_xml_to_dict_single_record(self):
        """Test the xml_to_dict function."""
        topic_xml = '''<topic>
             <title>The First Topic</title>
             <author-name>David</author-name>
             <id type="integer">1</id>
             <approved type="boolean"> true </approved>
             <replies-count type="integer">0</replies-count>
             <replies-close-in type="integer">2592000000</replies-close-in>
             <written-on type="date">2003-07-16</written-on>
             <viewed-at type="datetime">2003-07-16T09:28:00+0000</viewed-at>
             <content type="yaml">--- \n1: should be an integer\n:message: Have a nice day\narray: \n- should-have-dashes: true\n  should_have_underscores: true\n</content>
             <author-email-address>david@loudthinking.com</author-email-address>
             <parent-id></parent-id>
             <ad-revenue type="decimal">1.5</ad-revenue>
             <optimum-viewing-angle type="float">135</optimum-viewing-angle>
             <resident type="symbol">yes</resident>
           </topic>'''

        expected_topic_dict = {
            'title': 'The First Topic',
            'author_name': 'David',
            'id': 1,
            'approved': True,
            'replies_count': 0,
            'replies_close_in': 2592000000L,
            'written_on': datetime.date(2003, 7, 16),
            'viewed_at': util.date_parse('2003-07-16T9:28Z'),
            'content': {':message': 'Have a nice day',
                        1: 'should be an integer',
                        'array': [{'should-have-dashes': True,
                                   'should_have_underscores': True}]},
            'author_email_address': 'david@loudthinking.com',
            'parent_id': None,
            'ad_revenue': decimal.Decimal('1.5'),
            'optimum_viewing_angle': 135.0,
            'resident': 'yes'}

        self.assertEqual(expected_topic_dict, util.xml_to_dict(topic_xml))
        self.assertEqual(expected_topic_dict,
                         util.xml_to_dict(topic_xml, saveroot=True)['topic'])

    def test_xml_to_dict_multiple_records(self):
        """Test the xml to dict function."""
        topics_xml = '''<topics type="array">
            <topic>
              <title>The First Topic</title>
              <author-name>David</author-name>
              <id type="integer">1</id>
              <approved type="boolean">false</approved>
              <replies-count type="integer">0</replies-count>
              <replies-close-in type="integer">2592000000</replies-close-in>
              <written-on type="date">2003-07-16</written-on>
              <viewed-at type="datetime">2003-07-16T09:28:00+0000</viewed-at>
              <content>Have a nice day</content>
              <author-email-address>david@loudthinking.com</author-email-address>
              <parent-id nil="true"></parent-id>
            </topic>
            <topic>
              <title>The Second Topic</title>
              <author-name>Jason</author-name>
              <id type="integer">1</id>
              <approved type="boolean">false</approved>
              <replies-count type="integer">0</replies-count>
              <replies-close-in type="integer">2592000000</replies-close-in>
              <written-on type="date">2003-07-16</written-on>
              <viewed-at type="datetime">2003-07-16T09:28:00+0000</viewed-at>
              <content>Have a nice day</content>
              <author-email-address>david@loudthinking.com</author-email-address>
              <parent-id></parent-id>
            </topic>
          </topics>'''

        expected_topic_dict = {
            'title': 'The First Topic',
            'author_name': 'David',
            'id': 1,
            'approved': False,
            'replies_count': 0,
            'replies_close_in': 2592000000L,
            'written_on': datetime.date(2003, 7, 16),
            'viewed_at': util.date_parse('2003-07-16T09:28Z'),
            'content': 'Have a nice day',
            'author_email_address': 'david@loudthinking.com',
            'parent_id': None}

        self.assertEqual(expected_topic_dict,
                         util.xml_to_dict(topics_xml)[0])
        self.assertEqual(
            expected_topic_dict,
            util.xml_to_dict(topics_xml, saveroot=True)['topics'][0])

    def test_xml_to_dict_empty_array(self):
        blog_xml = '''<blog>
            <posts type="array"></posts>
            </blog>'''
        expected_blog_dict = {'blog': {'posts': []}}
        self.assertEqual(expected_blog_dict,
                         util.xml_to_dict(blog_xml, saveroot=True))

    def test_xml_to_dict_empty_array_with_whitespace(self):
        blog_xml = '''<blog>
            <posts type="array">
            </posts>
          </blog>'''
        expected_blog_dict = {'blog': {'posts': []}}
        self.assertEqual(expected_blog_dict,
                         util.xml_to_dict(blog_xml, saveroot=True))

    def test_xml_to_dict_array_with_one_entry(self):
        blog_xml = '''<blog>
            <posts type="array">
              <post>a post</post>
            </posts>
          </blog>'''
        expected_blog_dict = {'blog': {'posts': ['a post']}}
        self.assertEqual(expected_blog_dict,
                         util.xml_to_dict(blog_xml, saveroot=True))

    def test_xml_to_dict_file(self):
        blog_xml = '''<blog>
            <logo type="file" name="logo.png" content_type="image/png">
            </logo>
          </blog>'''
        blog_dict = util.xml_to_dict(blog_xml, saveroot=True)
        self.assert_('blog' in blog_dict)
        self.assert_('logo' in blog_dict['blog'])
        blog_file = blog_dict['blog']['logo']
        self.assertEqual('logo.png', blog_file.name)
        self.assertEqual('image/png', blog_file.content_type)


    def test_xml_to_dict_file_with_defaults(self):
        blog_xml = '''<blog>
            <logo type="file">
            </logo>
          </blog>'''
        blog_dict = util.xml_to_dict(blog_xml, saveroot=True)
        self.assert_('blog' in blog_dict)
        self.assert_('logo' in blog_dict['blog'])
        blog_file = blog_dict['blog']['logo']
        self.assertEqual('untitled', blog_file.name)
        self.assertEqual('application/octet-stream', blog_file.content_type)

    def test_xml_to_dict_xsd_like_types(self):
        bacon_xml = '''<bacon>
            <weight type="double">0.5</weight>
            <price type="decimal">12.50</price>
            <chunky type="boolean"> 1 </chunky>
            <expires-at type="dateTime">2007-12-25T12:34:56+0000</expires-at>
            <notes type="string"></notes>
            <illustration type="base64Binary">YmFiZS5wbmc=</illustration>
            </bacon>'''
        expected_bacon_dict = {
            'weight': 0.5,
            'chunky': True,
            'price': decimal.Decimal('12.50'),
            'expires_at': util.date_parse('2007-12-25T12:34:56Z'),
            'notes': '',
            'illustration': 'babe.png'}

        self.assertEqual(expected_bacon_dict,
                         util.xml_to_dict(bacon_xml, saveroot=True)['bacon'])

    def test_xml_to_dict_should_parse_dictionaries_with_unknown_types(self):
        xml = '''<records type="array">
                   <record type="MiscData">
                     <name>misc_data1</name>
                   </record>
                 </records>'''
        expected = {'records': [{'type': 'MiscData', 'name': 'misc_data1'}]}
        self.assertEqual(expected, util.xml_to_dict(xml, saveroot=True))

    def test_xml_to_dict_parses_datetime_timezones(self):
        blog_xml = '''<blog>
            <posted_at type="datetime">2008-09-05T13:34-0700</posted_at>
          </blog>'''
        blog_dict = util.xml_to_dict(blog_xml, saveroot=True)
        self.assertEqual((2008, 9, 5, 20, 34, 0, 4, 249, 0),
                         blog_dict['blog']['posted_at'].utctimetuple())

    def test_xml_to_dict_unknown_type(self):
        product_xml = '''<product>
            <weight type="double">0.5</weight>
            <image type="ProductImage"><filename>image.gif</filename></image>
           </product>'''
        expected_product_dict = {
            'weight': 0.5,
            'image': {'type': 'ProductImage', 'filename': 'image.gif'}}
        self.assertEqual(
            expected_product_dict,
            util.xml_to_dict(product_xml, saveroot=True)['product'])

    def test_xml_to_dict_errors_on_empty_string(self):
        self.assertRaises(Exception, util.xml_to_dict, '')

    def test_xml_to_dict_parses_children_which_are_not_of_parent_type(self):
        product_xml = '''
          <products type="array">
            <shamwow><made-in>Germany</made-in></shamwow>
          </products>'''
        self.assertEqual({'products': [{'made_in': 'Germany'}]},
                         util.xml_to_dict(product_xml, saveroot=True))

    def test_to_xml_should_allow_unicode(self):
        xml = util.to_xml({'data': u'\xe9'})
        self.assert_('<data>&#233;</data>' in xml)


if __name__ == '__main__':
    unittest.main()
