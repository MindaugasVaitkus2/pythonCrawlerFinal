import os
import sys
import subprocess
from urllib.request import urlopen
from urllib.error import HTTPError

#Global variables.
h1Tag, h1Tag_E = '<h1>', '</h1>'
h2Tag, h2Tag_E = '<h2>', '</h2>'
pTag,  pTag_E = '<p>', '</p>'
aTag, aTag_E = '<a', '</a>'
preTag, preTag_E = '<pre>', '</pre>'
liTag, liTag_E = '<li>', '</li>'
src, jpg = 'src="', '.jp'
new_Line = ' \n'
href, href_E = 'href="', '">'

#Returns a page that has been split on linebreaks.
def requestHTML(link):
  res = urlopen(link)
  html = res.read().decode('utf-8')
  html = html.split('\n')
  return html

#Extract links from the HTML returned from our 'requestHTML' method.
def getLinks():
    page_Name = 'https://clbokea.github.io/exam/'
    html = requestHTML(page_Name)
    file = open('linksToScrape.md', 'a')

    for e in html:
      if 'nav-link' in e:
        link_Start = e.find(href) + len(href)
        link_End = e.find(href_E)
        link_Name = e[e.find(href_E) : e.find(aTag_E)]
        link = page_Name + e[link_Start : link_End]
        file.write(link[:-5] + new_Line)
    file.close()

#Creates a file for each link found in  'linksToScrape'
def crawlLinks():
  file = open('linksToScrape.md', 'r')

  for link in file:
    fileName = link[31:-1]+'.md'
    file = open('%s' % fileName,'w')
    html = requestHTML(link)

    #Replace the html with markdown
    for e in html:
      if h1Tag in e:
        string = e[e.find(h1Tag) + len(h1Tag) : e.find(h1Tag_E)] + new_Line
        file.write('# ' + string)

      if jpg in e:      
        string = e[e.find(src) + len(src) : e.find(jpg)]
        file.write('![alt text](' + string + ' "picture") ' + new_Line)

      if h2Tag in e:                 
        string = e[e.find(h2Tag) + len(h2Tag) : e.find(h2Tag_E)] + new_Line
        file.write('## ' + string)

      if liTag in e:   
        string = e[e.find(liTag) + len(liTag) : e.find(liTag_E)] + new_Line
        file.write('- ' + string)
  
      if pTag in e:
        if aTag in e:
          linkDescription = e[e.find(href_E) + len(href_E) : e.find(aTag_E)]
          link = e[e.find(href) + len(href) : e.find(href_E)]
          markdownLink = '[' + linkDescription + ']' + '(' + link + ' "' + linkDescription + '") '
          e = e.strip()
          md_Start = e[len(pTag): e.find(aTag)]
          md_End = e[e.find(aTag_E):-4]
          string = md_Start + markdownLink + md_End
          file.write('> ' + string + new_Line)
        elif aTag not in e:
          string = e[e.find(pTag) + len(pTag) : e.find(pTag_E)] + new_Line
          file.write('> ' + string)
      
      if preTag in e:       
        string = e[e.find(preTag) + len(preTag_E) : e.find(preTag_E)] + new_Line
        file.write(string)

