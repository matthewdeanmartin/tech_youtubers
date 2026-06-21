from datetime import datetime

AUTHOR = 'YouTubers on Mastodon'
SITENAME = 'YouTubers on Mastodon'
SITESUBTITLE = 'Find YouTube creators, channel feeds, and real people to follow on Mastodon.'
SITEURL = ''
CURRENTYEAR = datetime.now().year
GENERATED_DATE = datetime.now().strftime('%Y-%m-%d')

PATH = 'content'

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'

# Feed generation is usually not needed for static listings
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = ()
SOCIAL = ()

DEFAULT_PAGINATION = 20

def _sort_by_sortorder(pages):
    return sorted(pages, key=lambda p: int(getattr(p, 'sortorder', 99)))

JINJA_FILTERS = {'sort_by_sortorder': _sort_by_sortorder}

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

THEME = 'themes/simple-pages'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = 'reviews/{slug}/'
ARTICLE_SAVE_AS = 'reviews/{slug}/index.html'

DIRECT_TEMPLATES = ['index', 'tags']
ARCHIVES_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_SAVE_AS = 'tags/index.html'
