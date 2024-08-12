import requests
from bs4 import BeautifulSoup

url = "https://mta.ua/igrovi-pristavki/manufacturers_nintendo_sony"
user_agent = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
}


def get_page(url, page_number="/page=1"):
    get_page = requests.get(url + page_number, headers=user_agent)
    get_content = get_page.text
    soup_obj = BeautifulSoup(get_content, "html.parser")
    return soup_obj


soup_obj = get_page(url)
find_tag_of_page = soup_obj.find_all("a", class_="pagination__list_url")
list_of_pages_number = []
for element in find_tag_of_page:
    number_page = element.contents[0]
    try:
        list_of_pages_number.append(int(number_page))
    except:
        break
if list_of_pages_number:
    get_count_pages = max(list_of_pages_number)
else:
    get_count_pages = 1

number_page = 1
while number_page <= int(get_count_pages):
    soup_obj2 = get_page(url, f"/page={number_page}")
    find_content = soup_obj2.find_all("div", class_="products__item_caption")

    for product in find_content:
        get_product_name = product.contents[1].string
        find_product_price = product.contents[3]
        try:
            get_price_new = find_product_price.find(
                "div", class_="products__item_price products__item_price_special"
            ).string
            get_price_old = find_product_price.find(
                "div", class_="products__item_price products__item_price_old"
            ).string
            print(
                f"Name: {get_product_name} ; New price: {get_price_new} ; Old price: {get_price_old}"
            )
        except:
            try:
                get_price = find_product_price.find(
                    "div", class_="products__item_price"
                ).string
                print(f"Name: {get_product_name} ; Price: {get_price}")
            except:
                break
    number_page += 1
