import base64

import requests
from bs4 import BeautifulSoup

song_directory = "songs"
artist_name = "Beatles"

song_counter = 1

def download_all():

    url_list = []

    page = requests.get("http://lyrics.wikia.com/api.php?artist="+artist_name)
    soup = BeautifulSoup(page.text)
    ulTag = soup.find_all("ul", {"class":"songs"})

    for tag in ulTag:
        liTags = tag.find_all("li")

        for tag in liTags:
            aTag = tag.find_all("a")

            for tag in aTag:
                url_list.append(tag['href'])

    return url_list

def download_song(song_url):

    global song_counter

    page = requests.get(song_url)
    soup = BeautifulSoup(page.text)
    tag = soup.find_all("meta", {"property":"og:title"})
    for meta_title_tag in tag:
        meta_title = meta_title_tag["content"]
        title = meta_title.split(":",1)[1]
        #title_formatted = base64.b64encode(title)
    title_formatted = song_directory+"/"+str(song_counter).zfill(3)
    output_file = open(title_formatted.encode("utf-8"),"w")
    song_counter += 1
#    output_file = open(song_directory+"/"+title,"w")
    output_file.write(title+"\n")

    for script in soup(["script","style"]):
        script.extract()

    divTag = soup.find_all("div", {"class":"lyricbox"})

    for tag in divTag:
        output_file.write(tag.get_text("\n").encode("utf-8"))

    output_file.close()

song_url_list = []
song_url_list = download_all()

for song_url in song_url_list:
    download_song(song_url)

#download_song(song_url_list[0])
