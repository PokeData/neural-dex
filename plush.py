#
#
#  this script will get all images of toys from pokemoncenter.com
#  and save each on a folder with the pokemon species name
#
#
#


from bs4 import BeautifulSoup
import requests
import pickle
import re
import shutil
import os



page = requests.get("https://www.pokemoncenter.com/plush#facet:&productBeginIndex:90&facetLimit:&orderBy:5&pageView:list&minPrice:&maxPrice:&pageSize:300&")

soup = BeautifulSoup(page.content, 'html.parser')

results = {}

for tag in soup.findAll("div",class_="product"):
    temp = tag

    try:
        # download image
        img_obj = temp.find(class_='product_image')
        img_link = img_obj.find(class_='alt-image')['data-src']
        img_link = 'https://www.pokemoncenter.com' + img_link
        # get name of plush
        name_obj = temp.find(class_='product_name')
        name = name_obj.find('a')['data-name'].split(' ', 1)[0]
        results[name] = img_link
    except:
        # name tag not found!
        pass


# one folder will be created for each pokemon species
for name,url in results.items():
    response = requests.get(url, stream=True)
    #create dir with pokemon name if it doesnt exists
    if not os.path.exists('poke_imgs'):
        os.makedirs('poke_imgs')

    if not os.path.exists('poke_imgs/' + name):
        os.makedirs('poke_imgs/'+ name)


    with open('poke_imgs/' +  name + '/' + name + '.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
