from tld import get_tld
from urllib.parse import urlparse
import re

class URLFeatureExtractor:

    def remove_www(self, url):
        """
        Removes the "www." prefix from a URL string if it exists.

        Args:
            url: The URL string.

        Returns:
            The URL string with the "www." prefix removed (if present), otherwise the original URL.
        """
        protocols = ["http://", "https://"]
        for protocol in protocols:
            if url.startswith(protocol + "www."):
                return protocol + url[len(protocol)+4:]  # Remove "www." after protocol (length 11)
        if url.startswith("www."):
            return url[4:]  # Remove the first 4 characters ("www.")
        return url

    def extract_length(self, url):
        """
        Extracts the length of the URL string.

        Args:
            url: The URL string.

        Returns:
            The length of the URL string.
        """
        return len(url)

    def extract_domain(self, url):
        """
        Extracts the domain name from the URL.

        Args:
            url: The URL string.

        Returns:
            The domain name extracted using regular expressions.
        """
        match = re.findall(r"^https?://([^/]+)", url)
        return match[0] if match else ""
    
    def process_tld(self, url):
        """
        Extracts the tld from the URL.

        Args:
            url: The URL string.

        Returns:
            The tld or None.
        """
        try:
            res = get_tld(url, as_object = True, fail_silently=False,fix_protocol=True)
            pri_domain= res.parsed_url.netloc
        except :
            pri_domain= None
        return pri_domain
    
    def special_character_count(self, url, special_character):
        """
        Counts the occurences of a certain special character in the URL.

        Args:
            url: The URL string and the special character.

        Returns:
            The count of character occurence.
        """
        return url.count(special_character)
    
    def abnormal_url(self, url):
        """
        Parses the URL hostname and tries to validate it against the URL itself.

        Args:
            url: The URL string.

        Returns:
            The 1 if it matches 0 otherwise.
        """
        hostname = urlparse(url).hostname
        hostname = str(hostname)
        match = re.search(hostname, url)
        return 1 if match else 0
    
    def httpSecure(self, url):
        """
        Checks if the URL's scheme is https.

        Args:
            url: The URL string.

        Returns:
            The 1 if it is, 0 otherwise.
        """
        scheme = urlparse(url).scheme
        match = str(scheme)
        return 1 if match=='https' else 0
    
    def digits_count(self, url):
        """
        Counts the number of digits in a URL.

        Args:
            url: The URL string.

        Returns:
            The digits count.
        """
        digits = 0
        for i in url:
            if i.isnumeric():
                digits = digits + 1
        return digits
    
    def letters_count(self, url):
        """
        Counts the number of letters in a URL.

        Args:
            url: The URL string.

        Returns:
            The letters count.
        """
        letters = 0
        for i in url:
            if i.isalpha():
                letters = letters + 1
        return letters
    
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
    
    def extract_features(self, url):
        """
        Extracts all features from a URL and returns them as a dictionary.

        Args:
            url: The URL string.

        Returns:
            A dictionary containing all extracted URL features.
        """
        url = self.remove_www(url)
        features = {}
        features["url_len"] = self.extract_length(url)
        # features["domain"] = self.extract_domain(url)
        # features["tld"] = self.process_tld(url)
        features["@"] = self.special_character_count(url, "@")
        features["?"] = self.special_character_count(url, "?")
        features["-"] = self.special_character_count(url, "-")
        features["="] = self.special_character_count(url, "=")
        features["."] = self.special_character_count(url, ".")
        features["#"] = self.special_character_count(url, "#")
        features["%"] = self.special_character_count(url, "%")
        features["+"] = self.special_character_count(url, "+")
        features["$"] = self.special_character_count(url, "$")
        features["!"] = self.special_character_count(url, "!")
        features["*"] = self.special_character_count(url, "*")
        features[","] = self.special_character_count(url, ",")
        features["//"] = self.special_character_count(url, "//")
        features["abnormal_url"] = self.abnormal_url(url)
        features["https"] = self.httpSecure(url)
        features["digits"] = self.digits_count(url)
        features["letters"] = self.letters_count(url)
        features["Shortining_Service"] = self.shortining_service(url)
        features["having_ip_address"] = self.having_ip_address(url)

        return features