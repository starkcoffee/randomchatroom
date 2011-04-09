import testhelper
import unittest
import filter


def runAgainstSamples(testCase, samples, testFunction):
    for input, expected in samples:
        actual = testFunction(input)
        testCase.assertEqual(expected, actual)


class HtmlFilterTest(unittest.TestCase):

    samples = [ 
                ("http://filter.com is great", 
                "<a href='http://filter.com'>filter.com</a> is great"),

                ("hey http://filter.com is great", 
                "hey <a href='http://filter.com'>filter.com</a> is great"),

                ("http://www.filter.com", 
                "<a href='http://www.filter.com'>www.filter.com</a>"),

                ("www.filter.com", 
                 "<a href='http://www.filter.com'>www.filter.com</a>"),

                ("https://www.filter.com", 
                    "<a href='https://www.filter.com'>https://www.filter.com</a>"),
              ]

    def testHtmlFilter(self):
        runAgainstSamples(self, self.samples, lambda input: filter.html(input))

class SwearFilterTest(unittest.TestCase):
    
    samples = [("fuck you" , "banana you"), ("no swears", "no swears")]


    def testSwearFilter(self):
        runAgainstSamples(self, self.samples, lambda input: filter.swears(input))

if __name__ == "__main__":
    unittest.main() 

