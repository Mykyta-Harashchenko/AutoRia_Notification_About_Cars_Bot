import requests
from bs4 import BeautifulSoup

def scrape_auto_ria() -> list[dict]:
    url = "https://auto.ria.com/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.id=840&damage.not=0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Не вдалося підключитися до сайту, код статусу: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    cars = []
    ads = soup.find_all("section", class_="ticket-item")

    for ad in ads:
        try:
            title = ad.find("div", class_="head-ticket").get_text(strip=True)
            price = ad.find("div", class_="price-ticket").get_text(strip=True)
            mileage = ad.find("li", class_="item-char").get_text(strip=True) if ad.find("li", class_="item-char") else "Не вказано"
            photos = ad.find_all("img", class_="outline", limit=3)
            photo_urls = [photo["src"] for photo in photos if "src" in photo.attrs]
            auction_link = ad.find("a", class_="address")["href"]
            details_button = None
            car_page_response = requests.get(auction_link, headers=headers)
            if car_page_response.status_code == 200:
                car_page_soup = BeautifulSoup(car_page_response.text, "html.parser")
                details_button = next(
                    (a["href"] for a in car_page_soup.find_all("a", class_="action-wrapper-link") if "href" in a.attrs),
                    None
                )
            cars.append({
                "title": title,
                "price": price,
                "mileage": mileage,
                "photos": photo_urls,
                "auction_link": auction_link,
                "auction_details_link": details_button,
            })
        except Exception as e:
            print(f"Помилка при парсингу оголошення: {e}")
    return cars

