import logging

DEFAULT_BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'
}

def setup_logging(log_level: int = logging.INFO):
    logging.basicConfig(
        handlers=[
            logging.FileHandler("logs/ai_bot.log"),
            logging.StreamHandler()
        ],
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=log_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

def is_url(url: str):
    return url.startswith('http://') or url.startswith('https://')

def get_browser_headers():
    return DEFAULT_BROWSER_HEADERS