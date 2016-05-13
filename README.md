# Facebook Trending RSS Feed Fetcher

A quickie Python 3.5 script that parses the [PDF-listing of RSS feeds](data/rss-urls.pdf) that Facebook uses to monitor for breaking news stories to add to its Trending Section.

# Background

On May 12, 2016, Gizmodo published an article titled, [Facebook Admits Its Trending Section Includes Topics Not Actually Trending on Facebook](http://gizmodo.com/facebook-admits-its-trending-section-includes-topics-no-1776319308), which covered the fallout from Gizmodo's previous reporting that [Facebook's Trending Section is mostly human-curated](http://gizmodo.com/former-facebook-workers-we-routinely-suppressed-conser-1775461006). As part of its response, Facebook released a list of 1,000 RSS feeds ([as a PDF file](https://fbnewsroomus.files.wordpress.com/2016/05/rss-urls.pdf)) that it says it uses to crawl for interesting news stories that may not have yet percolated through its social shares.

This repo contains code (and the results) to convert that PDF list into a machine-readable CSV ([data/rss-urls.csv](data/rss-urls.csv)) and then to fetch each RSS URL. A few of the URLs 404, but programmers who know how to parse XML can make use of the [retrieved data](data/feeds/) to do their own content analysis.


# About the collected data

The [data/feeds/](data/feeds/) folder already includes results from a fetch on __2016-05-12__, read the [directions further below](#mark-own-fetch) if you want to run it from scratch. The [data/feeds/](data/feeds/) contains JSON files that include the __metadata__ when requesting a given RSS URL. If successful, the serialized JSON object contains the raw, unparsed XML in a field named `response_text` (i.e. I haven't extracted the individual news items from each valid RSS feed).

Here's an example of how http://deadline.com/feed (saved as: [data/deadline.com_feed.json](data/deadline.com_feed.json)) is serialized:

~~~json
{
  "requested_url": "http://deadline.com/feed/",
  "fetched_at": "2016-05-12T23:35:52.197688",
  "status_code": 200,
  "response_text": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><rss version=\"2.0\"\n\txmlns:content=\"http://purl.org/rss/1.0/modules/content/\"\n\txmlns:wfw=\"http://wellformedweb.org/CommentAPI/\"\n\txmlns:dc=\"http://purl.org/dc/elements/1.1/\"\n...</channel>\n</rss>\n",
  "headers": {
    "Date": "Fri, 13 May 2016 06:33:29 GMT",
    "Vary": "Accept-Encoding, Accept-Encoding",
    "Last-Modified": "Fri, 13 May 2016 06:30:23 GMT",
    "Content-Type": "application/rss+xml; charset=UTF-8",
    "Server": "nginx",
    "X-nc": "HIT bur 209",
    "X-UA-Compatible": "IE=Edge",
    "X-hacker": "If you're reading this, you should visit automattic.com/jobs and apply to join the fun, mention this header.",
    "Connection": "keep-alive",
    "Content-Encoding": "gzip",
    "X-ac": "4.sjc _bur",
    "Transfer-Encoding": "chunked"
  },
  "response_url": "http://deadline.com/feed/"
}
~~~



<a id="mark-own-fetch"></a>

# Doing your own fetch

To re-populate the [data/](data) folder:


~~~sh
$ python scripts/fetch_pdf.py 
~~~

This will create the [data/rss-urls.csv](data/rss-urls.csv) file. The following script will run through each entry and fetch each RSS file and save the response to a corresponding JSON file in [data/feeds/](data/feeds/):

~~~sh
$ python scripts/fetch_feeds.py 
~~~

The JSON file for each fetch attempt includes metadata -- such as the headers, HTTP status code, and datetime of the request -- as well as a `response_text` that contains the raw text of the server response. The HTTP request will automatically follow redirects, so everything is either a `200` or some kind of error code. However, there is a `requested_url` -- which corresponds to the URL that came from Facebook's original document -- and a `response_url`, which can be used to compare against `requested_url` to see if a redirect occurred. This is a hacky way to deal with some redirects not pointing to actual RSS resources, e.g [http://www.nationaljournal.com/?rss=1](http://www.nationaljournal.com/?rss=1).
