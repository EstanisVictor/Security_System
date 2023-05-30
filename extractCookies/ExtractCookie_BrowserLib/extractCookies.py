import datetime
import browsercookie

def get_chrome_datetime(chromedate):
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""

def get_cookies_browser():
    cj = browsercookie.chrome()
    
    with open("cookies.txt", "w", encoding="utf-8") as f:
        for cookie in cj:
            f.write(f"""
            Host: {cookie.domain}
            Cookie name (session): {cookie.name}
            Cookie value: {cookie.value}
            Expires datetime (UTC): {get_chrome_datetime(cookie.expires)}
            ===============================================================
            """)
def main():
    get_cookies_browser()
    
if __name__ == "__main__":
    main()