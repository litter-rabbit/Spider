api_key='7b3304d0de88957'
api_key2='177db10f6588957'


from PIL import Image
import requests
import io
import pytesseract
from parsel import Selector
from urllib.parse import urljoin

url='http://www.porters.vip/confusion/recruit.html'

def get(url):
    resp=requests.request('GET',url)
    sel=Selector(resp.text)
    image_name=sel.css('.pn::attr("src")').extract_first()
    image_url=urljoin(url,image_name)
    image_body=requests.get(image_url).content
    image_stream=Image.open(io.BytesIO(image_body))
    print(pytesseract.image_to_string(image_stream))


if __name__ == '__main__':
    get(url)




