import shelve

# @todo: use config.json instead?
class Configuration:
    default_port = 8080
    log_conf_path = "project/configuration/logging.conf"
    log_file_path = "logging.log"

    log_view_n_lines = 100

    template_folder_path = "project/templates/"

    # trap settings
    trap_depth_max_depth = -1  # -1 (infinite), 2 (trap/depth/), 3 (trap/depth/3), etc.

    modes = [
        {
            'name': 'Blog',
            'route': 'blog',
            'add': 'admin/blog/add',
            'enabled': True
        },
        {
            'name': 'Forum',
            'route': 'forum',
            'add': 'admin/forum/add',
            'enabled': True
        },
        {
            'name': 'Newsfeed',
            'route': 'newsfeed',
            'add': 'admin/newsfeed/add',
            'enabled': True
        },
        {
            'name': 'Forms',
            'route': 'forms',
            'add': 'admin/forms/add',
            'enabled': True
        },
        {
            'name': 'Catalog',
            'route': 'catalog',
            'add': 'admin/catalog/add',
            'enabled': True
        }
    ]

    entry_single_page = True
    pagination_entry_per_page = 25

    ajax_enabled = True
    infinite_scroll_enabled = True


    # external links to use with the trap
    links = {
        "external": [
            {
                "name": "Google",
                "url": "http://www.google.ca/",
                "target": "_blank"
            },
            {
                "name": "Facebook",
                "url": "http://www.facebook.com/"
            },
            {
                "name": "twitter",
                "url": "http://www.twitter.com/"
            },
            {
                "name": "Facebook",
                "url": "http://www.facebook.com/"
            },
            {
                "name": "Grooveshark",
                "url": "http://www.grooveshark.com/"
            },
            {
                "name": "Python",
                "url": "http://www.python.org/"
            },
            {
                "name": "Perdu?",
                "url": "http://www.perdu.com/"
            },
            {
                "name": "thisdomaindoesnetexist",
                "url": "http://www.thisdomaindoesnetexist.com/"
            },
        ]
    }

    error_codes = {
        "1xx": [
            [100, "Continue"],
            [101, "Switching Protocols"],
            [102, "Processing (WebDAV; RFC 2518)"]
        ],
        "2xx": [
            [200, "OK"],
            [201, "Created"],
            [202, "Accepted"],
            [203, "Non-Authoritative Information (since HTTP/1.1)"],
            [204, "No Content"],
            [205, "Reset Content"],
            [206, "Partial Content"],
            [207, "Multi-Status (WebDAV; RFC 4918)"],
            [208, "Already Reported (WebDAV; RFC 5842)"],
            [226, "IM Used (RFC 3229)"]
        ],
        "3xx": [
            [300, "Multiple Choices"],
            [301, "Moved Permanently"],
            [302, "Found"],
            [303, "See Other (since HTTP/1.1)"],
            [304, "Not Modified"],
            [305, "Use Proxy (since HTTP/1.1)"],
            [306, "Switch Proxy"],
            [307, "Temporary Redirect (since HTTP/1.1)"],
            [308, "Permanent Redirect (Experimental RFC; RFC 7238)"]
        ],
        "4xx": [
            [400, "Bad Request"],
            [401, "Unauthorized"],
            [402, "Payment Required"],
            [403, "Forbidden"],
            [404, "Not Found"],
            [405, "Method Not Allowed"],
            [406, "Not Acceptable"],
            [407, "Proxy Authentication Required"],
            [408, "Request Timeout"],
            [409, "Conflict"],
            [410, "Gone"],
            [411, "Length Required"],
            [412, "Precondition Failed"],
            [413, "Request Entity Too Large"],
            [414, "Request-URI Too Long"],
            [415, "Unsupported Media Type"],
            [416, "Requested Range Not Satisfiable"],
            [417, "Expectation Failed"],
            [418, "I'm a teapot (RFC 2324)"],
            [419, "Authentication Timeout (not in RFC 2616)"],
            [420, "Method Failure (Spring Framework)"],
            [420, "Enhance Your Calm (Twitter)"],
            [422, "Unprocessable Entity (WebDAV; RFC 4918)"],
            [423, "Locked (WebDAV; RFC 4918)"],
            [424, "Failed Dependency (WebDAV; RFC 4918)"],
            [426, "Upgrade Required"],
            [428, "Precondition Required (RFC 6585)"],
            [429, "Too Many Requests (RFC 6585)"],
            [431, "Request Header Fields Too Large (RFC 6585)"],
            [440, "Login Timeout (Microsoft)"],
            [444, "No Response (Nginx)"],
            [449, "Retry With (Microsoft)"],
            [450, "Blocked by Windows Parental Controls (Microsoft)"],
            [451, "Unavailable For Legal Reasons (Internet draft)"],
            [451, "Redirect (Microsoft)"],
            [494, "Request Header Too Large (Nginx)"],
            [495, "Cert Error (Nginx)"],
            [496, "No Cert (Nginx)"],
            [497, "HTTP to HTTPS (Nginx)"],
            [498, "Token expired/invalid (Esri)"],
            [499, "Client Closed Request (Nginx)"],
            [499, "Token required (Esri)"]
        ],

        "5xx": [
            [500, "Internal Server Error"],
            [501, "Not Implemented"],
            [502, "Bad Gateway"],
            [503, "Service Unavailable"],
            [504, "Gateway Timeout"],
            [505, "HTTP Version Not Supported"],
            [506, "Variant Also Negotiates (RFC 2295)"],
            [507, "Insufficient Storage (WebDAV; RFC 4918)"],
            [508, "Loop Detected (WebDAV; RFC 5842)"],
            [509, "Bandwidth Limit Exceeded (Apache bw/limited extension)[25]"],
            [510, "Not Extended (RFC 2774)"],
            [511, "Network Authentication Required (RFC 6585)"],
            [520, "Origin Error (Cloudflare)"],
            [521, "Web server is down (Cloudflare)"],
            [522, "Connection timed out (Cloudflare)"],
            [523, "Proxy Declined Request (Cloudflare)"],
            [524, "A timeout occurred (Cloudflare)"],
            [598, "Network read timeout error (Unknown)"],
            [599, "Network connect timeout error (Unknown)"]
        ]
    }


    # Shelve database for configuration, unused yet
    def __init__(self):
        self.config_path = "db/shelve.db"
        shelve_db = shelve.open(self.config_path)

        if not shelve_db.has_key("modes"):
            shelve_db["modes"] = self.modes

        if not shelve_db.has_key('entry_single_page'):
            shelve_db["entry_single_page"] = self.entry_single_page

        if not shelve_db.has_key('pagination_entry_per_page'):
            shelve_db[
                'pagination_entry_per_page'] = self.pagination_entry_per_page

        shelve_db.close()
        self.load()


    def save(self):
        shelve_db = shelve.open(self.config_path)
        shelve_db['modes'] = self.modes

        shelve_db['pagination_entry_per_page'] = self.entry_single_page
        shelve_db['entry_single_page'] = self.entry_single_page

        shelve_db.close()


    def load(self):
        shelve_db = shelve.open(self.config_path)
        if shelve_db.has_key('modes'):
            self.modes = shelve_db['modes']

        if shelve_db.has_key('pagination_entry_per_page'):
            self.pagination_entry_per_page = shelve_db[
                'pagination_entry_per_page']

        if shelve_db.has_key('entry_single_page'):
            self.pagination_entry_per_page = shelve_db.has_key(
                'entry_single_page')

        shelve_db.close()