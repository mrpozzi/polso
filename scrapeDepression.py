import urllib2
from bs4 import BeautifulSoup
#import sys
#import os
#import couchdb
#import jsonlib2 as json
import MySQLdb
import re




# Let's crawl
HOMEURL = "http://www.depressionforums.org/forums/blogs/?type=all"


class ScrapeDepression:
    
    def __init__(self):
        self.blogPosts =  dict()
        self.blogLinks =  dict()
        
    def getLinks(self,url,fileName=''):
        
        n = 1
        
        print "Scraping links to blogs"
        
        while 1:
            #if n>1:
            #        break
            try:
                flob = urllib2.urlopen(url)
                #print "Reading Page {0}".format(n)
                n += 1
                s = flob.read()
                flob.close()
                soup = BeautifulSoup(s)
                
                for item in soup.find_all('td'):
                    if not item.get('class') is None:
                        if 'blog_title' in item.get('class'):
                            link = item.find_all('a')[0].get('href')
                        if 'col_f_starter' in item.get('class'):
                            name = item.get_text().replace("\n","").replace("\t","").encode('utf8')
                            #print name
                            self.blogLinks[name] = link
                
                # otherwise we keep on using the last link...
                next = False
                for item in soup.find_all('li'):
                    if not item.get('class') is None:
                        if 'next' in item.get('class'):
                            try:
                                url = item.find_all('a')[0].get('href')
                                next = True
                            except IndexError:
                                print item.find_all('a')
                                break
                        
                # if there is a next page, of course...
                if not next:
                    print "{0} pages scraped".format(n)
                    break
                
            except urllib2.HTTPError:
                print "{0} pages scraped".format(n)
                break
        
        if fileName != '':
            print "Saving links..."
            f = open(fileName,"wb")
            import cPickle
            cPickle.dump(self.blogLinks,f)
            f.close()
    
    def getPosts(self,fileName=''):
        
        print "Scraping Blogs"
        # loop on the blogs
        for name in self.blogLinks.keys():
            
            print "Reading {0} Blog".format(name)
            self.blogPosts[name] = dict()
            self.blogPosts[name]['posts'] = []
            self.blogPosts[name]['title'] = []
            self.blogPosts[name]['date'] = []
            url = self.blogLinks[name]
            
            nPages = 1
            nPosts = 1
            
            # loop on the pages within the blog
            while 1:
                
                try:
                        
                        #print "Reading Page {0}\n".format(url)
                        
                        flob = urllib2.urlopen(url)
                        s = flob.read()
                        flob.close()
                        soup = BeautifulSoup(s)
                        
                        nPages +=1
                        
                        # within the page we read we want to loop through the posts
                        for item in soup.find_all('h2'):
                                if not item.get('class') is None:
                                        if 'ipsType_pagetitle' in item.get('class'):
                                                link = item.find_all('a')[0].get('href')
                                                
                                                # loop on the posts
                                                flob2 = urllib2.urlopen(link)
                                                #print "Reading Post {0}\n".format(nPosts)
                                                nPosts += 1
                                                s2 = flob2.read()
                                                flob2.close()
                                                soup2 = BeautifulSoup(s2)
                                                
                                                # get the post content
                                                for item2 in soup2.find_all('div', {"class": "entry_content"}):
                                                        self.blogPosts[name]['posts'].append(item2.get_text().encode('utf8').replace('\n','').replace('\t',''))
                                                        
                                                for item2 in soup2.find_all('h1', {"class": "ipsType_pagetitle"}):
                                                        self.blogPosts[name]['title'].append(item2.get_text().encode('utf8').replace('\n','').replace('\t',''))
                                                        
                                                #Marco# I noticed that "Posted by" is present only in div with type of class "desc", so I take just the class desc
                                                for item2 in soup2.find_all('div', {"class": "desc"}):
                                                        ## Extract the date
                                                        text = item2.get_text()
                                                        pat = re.compile(r'\s+')
                                                        # Remove all space, tab and new line
                                                        no_tab = pat.sub('', text)
                                                        # Check if "Postedby" is present (now it's without space)
                                                        if no_tab.find('Postedby')>=0:
                                                                #print no_tab
                                                                date = re.search(r'\d{2}\D{3,9}\d{4}', no_tab)
                                                                self.blogPosts[name]['date'].append(date.string[date.start():date.end()])
                                                
                                                
                        # end loop on entries
                        # move to next page
                        next = False
                        #urlOld = url
                        for item in soup.find_all('link'):
                                if not item.get('rel') is None:
                                        if 'next' in item.get('rel'):
                                            link = item.get('href')

                        # if there is a next page, of course...
                        if not next : #or urlOld==url
                                print "{0} blog has {1} post{2}\n".format(name,nPosts,'s' if nPosts>1 else '')
                                break
                        
                                
                except urllib2.HTTPError:
                    print "{0} blog has {1} post{2}\n".format(name,nPosts,'s' if nPosts>1 else '')
                    break

        if fileName != '':
            f = open(fileName,"wb")
            cPickle.dump(self.blogPosts,f)
            f.close()





#scraper = ScrapeDepression()
#scraper.getLinks(HOMEURL,'pickledDepressionLinks')
#scraper.getLinks(HOMEURL)
#scraper.getPosts()

#[len(post) for post in blogPosts]
#sum([len(post) for post in blogPosts])


if __name__ == "__main__":
        scraper = ScrapeDepression()
        #scraper.getLinks(HOMEURL,'pickledDepressionLinks')
        scraper.getLinks(HOMEURL)
        scraper.getPosts('pickledDepressionPosts')

