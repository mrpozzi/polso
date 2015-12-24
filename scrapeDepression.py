#!/usr/bin/python


import urllib2
from bs4 import BeautifulSoup
import MySQLdb
import re
import cPickle
import numpy as np
import string, getopt, sys, random, time, pprint

class ScrapeDepression:
    """
    Class for scraping the depression forum.
    Sample use:
    scraper = scrapeDepression.ScrapeDepression()
    scraper.getLinks()
    scraper.getPosts('pickledDepressionPosts.pkl')
    #scraper.loadPosts('pickledDepressionPosts.pkl')
    scraper.createDB()
    scraper.topics()
    """
    
    def __init__(self):
        self.blogPosts =  dict()
        self.blogLinks =  dict()
        self.numPosts = 0
        
    def getLinks(self, url="http://www.depressionforums.org/forums/blogs/?type=all", fileName=''):
        
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
                            #self.blogLinks[name] = link
                        if 'col_f_views' in item.get('class'):
                            if item.find_all('li', {'class':'views desc'})[0].get_text()!='0 entries':
                                self.blogLinks[name] = link
                            #else:
                            #    print "{0} has 0 blog entries".format(name)
                        
                
                # otherwise we keep on using the last link...
                next = False
                for item in soup.find_all('li',{"class": "next"}):
                    try:
                        url = item.find_all('a')[0].get('href')
                        next = True
                    except IndexError:
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
        
        page = 1
        
        print "Scraping Blogs"
        # loop on the blogs
        for name in self.blogLinks.keys():
            
            print "Reading {0} Blog".format(name)
            self.blogPosts[name] = dict()
            self.blogPosts[name]['post'] = []
            self.blogPosts[name]['title'] = []
            self.blogPosts[name]['date'] = []
            url = self.blogLinks[name]
            
            nPages = 0
            nPosts = 0
            
            # loop on the pages within the blog
            while 1:
                
                try:
                        
                        #print "Reading Page {0}\n".format(url)
                        
                        flob = urllib2.urlopen(url)
                        s = flob.read()
                        flob.close()
                        soup = BeautifulSoup(s)
                        
                        nPages += 1
                        
                        # within the page we read we want to loop through the posts
                        for item in soup.find_all('h2', {"class": "ipsType_pagetitle"}):
                            link = item.find_all('a')[0].get('href')

                            # loop on the posts
                            flob2 = urllib2.urlopen(link)
                            #print "Reading Post {0}\n".format(nPosts)
                            nPosts += 1
                            self.numPosts += 1
                            s2 = flob2.read()
                            flob2.close()
                            soup2 = BeautifulSoup(s2)
                            
                            # get the post content
                            for item2 in soup2.find_all('div', {"class": "entry_content"}):
                                self.blogPosts[name]['post'].append(item2.get_text().encode('utf8').replace('\n','').replace('\t',''))
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
                                    self.blogPosts[name]['date'].append(date.string[date.start():date.end()].encode('utf8'))
                        
                        
                        
                        # end loop on entries
                        # move to next page
                        next = False
                        #urlOld = url
                        for item in soup.find_all('link'):
                                if not item.get('rel') is None:
                                        if 'next' in item.get('rel'):
                                            url = item.get('href')
                                            next = True
                                            

                        # if there is a next page, of course...
                        if not next : #or urlOld==url
                                print "{0} blog has {1} post{2}\n".format(name,nPosts,'s' if nPosts>1 else '')
                                break
                        
                                
                except urllib2.HTTPError:
                    print "{0} blog has {1} post{2}\n".format(name,nPosts,'s' if nPosts>1 else '')
                    break
        
        print "{0} blog  post{1} read\n".format(self.numPosts,'s' if self.numPosts>1 else '')
        
        if fileName != '':
            f = open(fileName,"wb")
            cPickle.dump(self.blogPosts,f)
            f.close()
    
    
    def loadPosts(self,fileName):
        self.blogPosts = cPickle.load(open(fileName))
        self.numPosts = sum([len(self.blogPosts[name]['post']) for name in self.blogPosts.keys()])
    
    
    def createDB(self):
        """
        For this function to be used you need to install mysql then
        start the server with the command:
        sudo /usr/local/bin/mysql.server restart
        (the path depends on your installation)
        
        Then you need to configure the user and create the database

        mysql --user=root mysql
        CREATE USER 'luca'@'localhost';
        GRANT ALL PRIVILEGES ON *.* TO 'luca'@'localhost' WITH GRANT OPTION;
        CREATE SCHEMA depressiondb;
        
        """
        # Open database connection
        db = MySQLdb.connect(host="localhost", # your host, usually localhost
                        user="luca", # your username
                        passwd="", # your password
                        db="depressiondb") # name of the data base
        
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        
        # Drop table if it already exist using execute() method.
        cursor.execute("DROP TABLE IF EXISTS DEPRESSION")
        
        # Create table as per requirement
        sql = """CREATE TABLE DEPRESSION (
        NAME  CHAR(100) NOT NULL,
        DATE  CHAR(20),
        TITLE  CHAR(200) NOT NULL,
        POST  TEXT)"""
        
        cursor.execute(sql)
        
        for name in self.blogPosts.keys():
            print "Inserting {0}'s blog in db".format(name)
            for k in np.arange(0,len(self.blogPosts[name]['date'])):
                
                # Prepare SQL query to INSERT a record into the database.
                #sql = """INSERT INTO DEPRESSION (NAME, DATE, TITLE, POST)
                #VALUES ('{0}', '{1}', '{2}', '{3}')""".format(name,self.blogPosts[name]['date'][k],
                #                                                    self.blogPosts[name]['title'][k],
                #                                                    str(MySQLdb.escape_string(self.blogPosts[name]['post'][k])))
                sql = """INSERT INTO DEPRESSION (NAME, DATE, TITLE, POST)
                VALUES (%s, %s, %s, %s)"""
                #print sql
                try:
                    # Execute the SQL command
                    cursor.execute(sql,(name,self.blogPosts[name]['date'][k],self.blogPosts[name]['title'][k],str(MySQLdb.escape_string(self.blogPosts[name]['post'][k]))))
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()
                    print sql
        
        # disconnect from server
        db.close()
    
    def topics(self,nTopic=100,batchsize = 64,stream=True):
        
        """
        Analyzes the blog posts using
        onlineldavb.py: Package of functions for fitting Latent Dirichlet
        Allocation (LDA) with online variational Bayes (VB).
        
        Copyright (C) 2010  Matthew D. Hoffman
        """
                
        # The number of documents to analyze each iteration
        
        # The total number of blog posts
        D = self.numPosts
        # The number of topics
        K = nTopic
        
        # Our vocabulary
        vocab = file('./dictnostops.txt').readlines()
        W = len(vocab)
        
        if stream:
            import streaminglda as ldavb
            lda = ldavb.StreamingLDA(vocab, K, 1./K, 1./K)
        else:
            # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
            import onlineldavb as ldavb
            lda = ldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
        
        # Run until we've seen D documents. (Feel free to interrupt *much*
        # sooner than this.)
        #for iteration in range(0, docmentstoanalyze):
        iteration = 0
        doc_buffer = []
        for name in self.blogPosts.keys():
            
            docset = self.blogPosts[name]['post']
            
            #docset batchsize
            # Give them to online LDA
            #print "{0} posts by {1}".format(len(docset),name)
            if len(doc_buffer) !=0:
                docset = docset + doc_buffer
                doc_buffer = []
            if len(docset) < batchsize:
                doc_buffer = docset
                continue
                
            (gamma, bound) = lda.update_lambda(docset)
            # Compute an estimate of held-out perplexity
            (wordids, wordcts) = ldavb.parse_doc_list(docset, lda._vocab)
            perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
            print '%d:  held-out perplexity estimate = %f' % (iteration, np.exp(-perwordbound))
            
            # Save lambda, the parameters to the variational distributions
            # over topics, and gamma, the parameters to the variational
            # distributions over topic weights for the articles analyzed in
            # the last iteration.
            if (iteration % 10 == 0):
                np.savetxt('lambda-%d.dat' % iteration, lda._lambda)
                np.savetxt('gamma-%d.dat' % iteration, gamma)
            
            iteration += 1


if __name__ == "__main__":
    """
    This main method scrapes the website and then
    creates a mySQL database with the results
    """
    scraper = ScrapeDepression()
    scraper.getLinks()
    scraper.getPosts()
    scraper.createDB()

