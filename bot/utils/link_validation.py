import re


def check_pikabu_link(link: str) -> str | bool:
    try:
        # Formatted string used for regex with whitespace. Without this regex can be failed if link in end of string
        link = re.search('https:\/\/pikabu.ru(.*) ', f'{link} ').group().strip()
        return link
    except Exception as e:
        return False
