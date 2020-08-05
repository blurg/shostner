from ..main import urls

def log_access_info(shortened_url: str, user_agent: str, referer: str, ip: str, language: str):
    print("Just Redirected a request with the following data")
    print(f"Shortened URL: {shortened_url}")
    print(f"Targer URL: {urls.get(shortened_url, 'http://www.facebook.com')}")
    print(f"User Agent: {user_agent}")
    print(f"Referer: {referer}")
    print(f"Ip: {ip}")
    print(f"Language Preferences: {language}")
    print("====================")
