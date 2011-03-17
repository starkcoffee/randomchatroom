import unittest
import textfilter 

class FormatLinksTest(unittest.TestCase):

    samples = ( 
                ('check out http://foo.com', 
                'check out <a href="http://foo.com">http://foo.com</a>'),

                ('http://foo.com is great', 
                '<a href="http://foo.com">http://foo.com</a> is great'),

                ('hey http://foo.com is great', 
                'hey <a href="http://foo.com">http://foo.com</a> is great'),

                ('check out http://www.foo.com', 
                'check out <a href="http://www.foo.com">http://www.foo.com</a>'),

                ('http://www.foo.com is great', 
                '<a href="http://www.foo.com">http://www.foo.com</a> is great'),

                ('hey http://www.foo.com is great', 
                'hey <a href="http://www.foo.com">http://www.foo.com</a> is great'),

                ('check out www.foo.com', 
                 'check out <a href="http://www.foo.com">www.foo.com</a>'),

                ('www.foo.com is great', 
                 '<a href="http://www.foo.com">www.foo.com</a> is great'),

                ('hey www.foo.com is great', 
                 'hey <a href="http://www.foo.com">www.foo.com</a> is great'),
              )
    
    def testFormatLinks(self):
        """should wrap html a tags around links in comments"""
        for input, expected in self.samples:
            actual = textfilter.formatLinks(input)
            self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main() 

