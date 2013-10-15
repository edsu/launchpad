from django.test import TestCase

from ui.templatetags.launchpad_extras import clean_isbn, clean_lccn
from ui.voyager import insert_sid


class CleanIsbnTest(TestCase):

    def test_bad_isbns(self):
        """ensure some odd cases come out right."""
        bad_isbn1 = '0080212472. 0080212464'
        self.assertEqual(clean_isbn(bad_isbn1), '0080212472')
        bad_isbn2 = '0679302603; 0679302611 (papbk)'
        self.assertEqual(clean_isbn(bad_isbn2), '0679302603')


class CleanLccnTest(TestCase):

    examples = [
            ('89-456', '89000456'),
            ('2001-1114', '2001001114'),
            ('gm 71-2450', 'gm71002450'),
            ('n 79-18774', 'n79018774'),
            ('sh 85026371', 'sh85026371'),
            ('sn2006058112', 'sn2006058112'),
            ('n 2011033569', 'n2011033569'),
            ('sh2006006990', 'sh2006006990'),
            ('n78-890351', 'n78890351'),
            ('n78-89035', 'n78089035'),
            ('n 78890351', 'n78890351'),
            (' 85000002', '85000002'),
            ('85-2', '85000002'),
            ('2001-000002', '2001000002'),
            ('75-425165//r75', '75425165'),
            (' 79139101 /AC/r932', '79139101'),
            ]

    def test_normalized_lccns(self):
        """ensure example cases are handled correctly"""
        for in_lccn, out_lccn in self.examples:
            self.assertEqual(clean_lccn(in_lccn), out_lccn)

class IlliadSidTest(TestCase):

    def test_illiad_sid(self):

        # expected is a list of tuples, each tuple includes the data to call 
        # insert_sid with and the expected output of the call

        expected = [
                (
                    'genre=article&issn=0010194X&title=Columbia%20Journalism%20Review&volume=52&issue=1&date=20130501&atitle=Streams%20of%20consciousness.&spage=24&pages=24-36&sid=EBSCO:Communication%20&%20Mass%20Media%20Complete&aulast=ADLER,%20BEN',
                    'https://www.aladin.wrlc.org/Z-WEB/ILLAuthClient?genre=article&issn=0010194X&title=Columbia%20Journalism%20Review&volume=52&issue=1&date=20130501&atitle=Streams%20of%20consciousness.&spage=24&pages=24-36&sid=EBSCO:Communication%20and%20Mass%20:GWLP&aulast=ADLER,%20BEN',
                ),
                (
                    'genre=article&issn=01644297&title=Arizona+State+Law+Journal&volume=1974&issue=&date=19740101&atitle=Closing+the+gap%3a+protection+for+mobile+home+owners.&spage=101&pages=101-127&sid=EBSCO:Index+to+Legal+Periodicals+Retrospective%3a+1908-1981+&', 
                    'https://www.aladin.wrlc.org/Z-WEB/ILLAuthClient?genre=article&issn=01644297&title=Arizona+State+Law+Journal&volume=1974&issue=&date=19740101&atitle=Closing+the+gap%3a+protection+for+mobile+home+owners.&spage=101&pages=101-127&sid=EBSCO:Index+to+Legal+Periodical:GWLP&')
                ]

        for i, o in expected:
            result = insert_sid({'openurl': {'query_string_encoded': i}}, 0)
            self.assertEqual(o, result)
