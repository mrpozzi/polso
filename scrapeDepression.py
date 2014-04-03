import urllib2
from bs4 import BeautifulSoup


# Let's crawl
HOMEURL = "http://www.depressionforums.org/forums/blogs/?type=all"

blogPosts = dict()
blogLinks = dict()

url = HOMEURL
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
                    blogLinks[name] = link

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

print "Saving links..."
f = open("pickledDepressionLinks","wb")
import cPickle
cPickle.dump(blogLinks,f)
f.close()

#print cpickle


print "Scraping Blogs"
# loop on the blogs
for name in blogLinks.keys():
        
        print "Reading {0} Blog".format(name)
        blogPosts[name] = []
        url = blogLinks[name]
        
        nPages = 1
        nPosts = 1
        
        # loop on the pages within the blog
        while 1:
        
                try:
                        
                        #print "Reading Page {0}\n".format(nPages)
                        
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
                                                for item2 in soup2.find_all('div'):
                                                        if not item2.get('class') is None:
                                                                if 'entry_content' in item2.get('class') :
                                                                        blogPosts[name].append(item2.get_text().encode('utf8'))
                        # end loop on entries
                        # move to next page
                        next = False
                        for item in soup.find_all('link'):
                                if not item.get('rel') is None:
                                        if 'next' in item.get('rel'):
                                                url = item.get('href')
                                                next = True
                                                
                        # if there is a next page, of course...
                        if not next:
                                print "{0} blog has {1} post{2}\n".format(name,nPosts,'s' if nPosts>1 else '')
                                break
                                
                        
                except urllib2.HTTPError:
                        print "{0} blog has {1} post{2}\n".format(name,nPosts,'s' if nPosts>1 else '')
                        break


f = open("pickledDepressionBlogs","wb")
cPickle.dump(blogPosts,f)
f.close()

#import cPickle
#blogPosts = cPickle.load(open("pickledDepressionBlogs"))
#blogLinks = cPickle.load(open("pickledDepressionLinks"))



[len(post) for post in blogPosts]
sum([len(post) for post in blogPosts])
