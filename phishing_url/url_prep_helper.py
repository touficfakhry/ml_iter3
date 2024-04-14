from tld import get_tld
from urllib.parse import urlparse
import re

class URLPrepHelper():

    def __init__(self, df, url_column_name = 'url'):
        self.df = df
        self.url_column_name = url_column_name

    def remove_www(self):
        self.df[self.url_column_name] = self.df[self.url_column_name].str.replace('www.', '', regex=True)

    def add_extracted_url_length(self):
        self.df['url_len'] = self.df[self.url_column_name].apply(lambda x: len(str(x)))

    def process_tld(self, url):
        try:
            res = get_tld(url, as_object = True, fail_silently=False,fix_protocol=True)
            pri_domain= res.parsed_url.netloc
        except :
            pri_domain= None
        return pri_domain
    
    def add_processed_tld(self):
        self.df['domain'] = self.df[self.url_column_name].apply(lambda x: self.process_tld(x))

    def add_extracted_url_features(self):
        feature = ['@','?','-','=','.','#','%','+','$','!','*',',','//']
        for a in feature:
            self.df[a] = self.df[self.url_column_name].apply(lambda i: i.count(a))
    

    def abnormal_url(self, url):
        hostname = urlparse(url).hostname
        hostname = str(hostname)
        match = re.search(hostname, url)
        if match:
            # print match.group()
            return 1
        else:
            # print 'No matching pattern found'
            return 0
    
    def add_abnormal_url_feature(self):
        self.df['abnormal_url'] = self.df[self.url_column_name].apply(lambda i: self.abnormal_url(i))
    
    def httpSecure(self, url):
        scheme = urlparse(url).scheme
        match = str(scheme)
        return 1 if match=='https' else 0
    
    def add_is_https_feature(self):
        self.df['https'] = self.df[self.url_column_name].apply(lambda i: self.httpSecure(i))
    
    def digit_count(self, url):
        digits = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
        return digits
    
    def add_digits_count(self):
        self.df['digits']= self.df[self.url_column_name].apply(lambda i: self.digit_count(i))
    
    def letter_count(self, url):
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
        return letters
    
    def add_letters_count(self):
        self.df['letters']= self.df[self.url_column_name].apply(lambda i: self.letter_count(i))
    
    def shortining_service(self,url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                        'tr\.im|link\.zip\.net',
                        url)
        return 1 if match else 0
    
    def add_shortening_service(self):
        self.df['Shortining_Service'] = self.df[self.url_column_name].apply(lambda x: self.shortining_service(x))

    def having_ip_address(self, url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
            '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
            '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
        return 1 if match else 0
    
    def add_having_ip_address(self):
        self.df['having_ip_address'] = self.df[self.url_column_name].apply(lambda i: self.having_ip_address(i))