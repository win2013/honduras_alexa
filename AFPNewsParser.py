import os

___author__   = "Edwin Hernandez, PhD"
__copyright__ = "Copyright 2017, EDWIN HERNADNEZ LLC"
__version__   = "0.1"


from time import time
from lxml import html
from lxml import etree
from urllib import quote
import urllib2
from hashlib import sha1


class NewsML:
    newsmlCount = 0;

    def __init__(self):
      self.filename = ""
      self.text     = ""
      self.subjects = []
      NewsML.newsmlCount += 1
      self.newsml_content = ""


    def find_text_and_subjects(self, newsml_content,
                              subject_tags=('SubjectMatter', 'SubjectDetail'),
                              text_tags=('HeadLine',),
                              html_tags=('body.content',)):
    # First parse of the document as XML for the structured attributes
       xtree = etree.ElementTree(etree.fromstring(newsml_content))
       text_items = [e.text.strip()
                  for tag in text_tags
                  for e in xtree.findall('//' + tag)]
       text = "\n\n".join(text_items)
       subjects = [ e.get('FormalName')
                 for tag in subject_tags
                 for e in xtree.findall('//' + tag)]

       # Then use HTML parser to find the that looks like HTML hence can leverage
       # the text_content method.
       htree = etree.ElementTree(html.document_fromstring(newsml_content))

       text_items += [e.text_content().strip()
                   for tag in html_tags
                   for e in htree.findall('//' + tag)]

       text = "\n\n".join(text_items)
       self.text = text
       self.subjects = subjects
       return text, subjects

    def fetchdata(self, topfolder, dirpath, filename):
       full_path = os.path.join(topfolder, dirpath, filename)
       newsml_content = open(full_path, 'rb').read()
       text, codes = self.find_text_and_subjects(newsml_content)
       return text, codes

    def retrieve_news():
       return True

    def __repr__(self):
        return "<NewsML>::::: TEXT:\n %s \n:::: SUBJECT \n  %s"%(self.text.encode('utf-8').strip(), " * ".join(self.subjects,).encode('utf-8').strip())

if __name__ == '__main__':
      topfolder= "/Users/edwinhm/sources/Alexa App /"

      for dirpath, dirnames, filenames in os.walk(topfolder):
        for f in filenames:
             if f.endswith(".xml"):
                    newsML = NewsML();
                    print f
                    newsML.fetchdata(topfolder, dirpath, f);
                    print newsML
