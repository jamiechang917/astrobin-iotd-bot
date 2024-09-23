import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}

def get_iotd_url() -> str:
    url = "https://www.astrobin.com/iotd/archive/"
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        latest_image_link = soup.find('div', class_='iotd-archive-image').find('a', href=True)
        latest_image_href = latest_image_link['href']
        image_url = f"https://astrobin.com{latest_image_href}"
        return image_url
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WARNING     Failed to get IOTD URL: {e}")
        return None

def get_image_info(url:str):
    try:
        response = requests.get(url, headers=headers)
        soup   = BeautifulSoup(response.content, "html.parser")
        title  = soup.find('h3', class_='image-title').get_text(strip=True)
        date   = soup.find('span', class_='date').get_text(strip=True)
        author = soup.find('div', class_='username').get_text(strip=True)
        try:
            description = soup.find('div', class_='image-description').get_text(strip=True, separator=" ")[len("Description "):]
        except:
            description = "" # No description
        img    = soup.find('div', class_='astrobin-image-container').find('a', href=True).find('img')['src']
        return {
            'title': title,
            'date': date,
            'author': author,
            'description': description,
            'img': img
        }
    except Exception as e:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WARNING     Failed to get image info: {e}")
        return None

def truncate_text(text, word_limit=100):
    words = text.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return text

# if __name__ == "__main__":
#     print(get_image_info(get_iotd_url()))