import requests
import json
from urllib.parse import quote,unquote,urlparse
import time
import re
from tqdm import tqdm
import os
from pytubefix import Playlist, YouTube
from pytubefix.cli import on_progress
from termcolor import colored
from blacklisted import *
from megaDownloader import *
from config import *

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


def supported():
    siteslist = []
    url = 'https://api.alldebrid.com/v4/hosts/domains?agent=test'
    r = requests.get(url)
    data = json.loads(r.text)

    for hosts in data['data']['hosts']:
        siteslist.append(hosts)
    
    for streams in data['data']['streams']:
        siteslist.append(streams)
        
    for redirectors in data['data']['redirectors']:
        siteslist.append(redirectors)
    
    #Removes blacklisted sites from the retrieved list.
    for site in blacklist:
        if site in blacklist:
            siteslist = remove_values_from_list(siteslist, site)

    #Removes duplicated items
    siteslist = list(dict.fromkeys(siteslist))

    whitelist = ["ddownload.com", "send.cm", "bfmtv.com", "twitter.com", "x.com", "mitele.es", "tudou.com", "youku.com"]
    siteslist = siteslist + whitelist
    return siteslist

def checksupport():
        userurl = input(colored("Enter the url: \t","light_yellow"))
        siteslist = supported()
        for site in siteslist:
                if userurl == site:
                        print(colored(str(userurl) + " is supported","light_green"))
                        return True
        print(colored(str(userurl) + " is not supported","light_red"))


#gets link from json that retrieved from alldebrid API
def getlink(data):
    return data['data']['link']


#getFileNameFromLink gets the file name from link 
#the filename comes after the last slash

def getFileNameFromLink(name):
    if name.find('/'):
        name = unquote(name.rsplit('/', 1)[1])
    name = re.sub(r'[\\/*?:"<>|]',"",name)
    return name


#downloader function comes after unlocking the url to start downloading the file in the current working directory.
# the filename comes from executing getFileNameFromLink() function to retrieve it from URL
# the rest of the code downloads the file with progress bar by using tqdm library
# the os.getcwd() prints the current working directory.

def downloader(unlockedlink):
    if os.path.isdir('output') is False:
        os.mkdir('output')

    print(colored("Start Downloading.....","light_green"))
    fileName = 'output/'+getFileNameFromLink(unlockedlink)
    print(colored("FileName: " + getFileNameFromLink(unlockedlink), "light_yellow"))
    response = requests.get(unlockedlink, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    with tqdm(total=total_size, unit="B", unit_scale=True, colour="red") as progress_bar:
        with open(fileName, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

    if total_size != 0 and progress_bar.n != total_size:
        raise RuntimeError(colored("Could not download file", "light_red"))
    print(colored("DONE!!","light_green"))
    print(colored("Your file is saved in: ", "light_green") + colored(os.getcwd()+"\\output\n\n", "light_yellow"))
    


def unlocker(link):    
    try:
        url = "https://api.alldebrid.com/v4/link/unlock?agent=test&apikey="+ key + "&link=" + quote(link)
        r = requests.get(url)
        data = json.loads(r.text)
        if 'delayed' in data['data']:
            containsDelay(data)
        elif data['data']['host'] == "stream" and data['data']['link'] == "":
            id = data['data']['id']
            stream = data['data']['streams']
            index = 0
            print(colored("Name:\t "+ str(data['data']['filename']),"light_yellow"))
            for stream in range(len(stream)):
                print(colored(str(index) + ") " + str(data['data']['streams'][index]['quality']),"light_blue"))
                index+=1
            option = int(input(colored(">>> ","light_yellow")))


            stream = data['data']['streams'][option]['id']

            mediaunlocker(id, stream)
        else:
            downloader(getlink(data))
    except TypeError:
        print(colored("Invalid Input!", "light_red"))
    except KeyboardInterrupt:
        print(colored("the download process has been interrupted!", "light_red"))
    except:
        parsed_url = urlparse(link)
        domain = parsed_url.netloc
        print(colored("something went wrong. is " + domain +" website supported?", "light_red"))
        print(colored("Try Again.", "light_red"))





def mediaunlocker(id, stream):
    url = "https://api.alldebrid.com/v4/link/streaming?agent=test&apikey="+ key + "&id=" + quote(id) + "&stream=" + quote(stream)
    r = requests.get(url)
    data = json.loads(r.text)
    containsDelay(data)




def containsDelay(data):
    if 'delayed' in data['data']:
        url = "https://api.alldebrid.com/v4/link/delayed?agent=test&apikey="+ key + "&id=" + str(data['data']['delayed'])
        r = requests.get(url)
        data = json.loads(r.text)
        while True:
            status = data['data']['status']
            if status == 1 or status == 0:
                print(colored("Still processing", "light_yellow"))
                time.sleep(5)
            elif status == 2:
                downloader(getlink(data))
                return True
            elif status == 3:
                print(colored("Error, could not generate download link.", "light_red"))
                return False
            r = requests.get(url)
            data = json.loads(r.text)
    else:
        downloader(getlink(data))





def multiunlocker(links):
    for link in links:
        link = link.strip()
        domain = urlparse(link).netloc
        if domain in blacklist:
            print(colored(domain+" is not supported!!","red"))
        elif "youtube" in link or "youtu.be" in link:
            if "playlist" in link:
                option = int(input(colored("Download Playlist as:\n1)Video\n2)Audio\n3)Both\n>>> ", "light_blue")))
                print(colored("NOTE: THE ENTIRE YOUTUBE PLAYLIST WILL BE DOWNLOADED AS AUDIO OR VIDEO OR BOTH", "light_yellow"))
                time.sleep(5)
                YoutubePlaylist(link,option)
            else:
                option = int(input(colored("1)Video\n2)Audio\n3)Both\n>>> ","light_blue")))
                YoutubeOptions(link,option)
        elif "mega" and "folder" in link:
            folderExtractor(link)
            file = open('mega.txt', 'r')
            links = file.readlines()
            multiunlocker(links)
        else:
            unlocker(link)



def multilink():
    try:
        file = open('links.txt', 'r')
        links = file.readlines()
        multiunlocker(links)
    except FileNotFoundError:
         print(colored("links.txt file doesn't exist or empty", "light_red"))
         print(colored("create this file beside the program in the same directory and fill it with links, link in each line", "light_red"))
    except: 
        print(colored("Something went wrong.\n Try Again.", "light_red"))

    
def singlelink():
    link = input("Enter your link: \t")
    link = link.strip()
    domain = urlparse(link).netloc
    if domain in blacklist:
        print(colored(domain+" is not supported!!","red"))
    
    elif "youtube" in link or "youtu.be" in link:
        if "playlist" in link:
            option = int(input(colored("Download Playlist as:\n1)Video\n2)Audio\n3)Both\n>>> ", "light_blue")))
            YoutubePlaylist(link,option)
            return True
        option = int(input(colored("1)Video\n2)Audio\n3)Both\n>>> ", "light_blue")))
        YoutubeOptions(link,option)
    elif "mega" and "folder" in link:
        folderExtractor(link)
        file = open('mega.txt', 'r')
        links = file.readlines()
        multiunlocker(links)
    
    else:
        unlocker(link)


def YoutubeOptions(link, option):
    if option == 1:
        YoutubeVideoDownloader(link)
    elif option == 2:
        YoutubeAudioDownloader(link)
    elif option == 3:
        YoutubeVideoDownloader(link)
        YoutubeAudioDownloader(link)
    else:
        print(colored("Invalid option", "light_red"))


def YoutubePlaylist(link,option):
    playlist = Playlist(link)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    for url in playlist: 
        YoutubeOptions(url,option)
    



def YoutubeVideoDownloader(link):
    try:
        video = YouTube(link, on_progress_callback=on_progress)
        video = video.streams.get_highest_resolution()
        print(colored("Video Name: "+video.title, "light_yellow"))
        video.download(filename=removeSpecialChars(video.title)+'.mp4', output_path='output')
        print(colored("Download is completed successfully", "light_green"))
        print(colored("Your file is saved in: ", "light_green") + colored(os.getcwd()+"\\output\n\n", "light_yellow"))
    except:
        YoutubeAnotherMethod(link)


def YoutubeAudioDownloader(link):
    try:
        audio = YouTube(link, on_progress_callback=on_progress)
        audio = audio.streams.filter(only_audio=True).first()
        print(colored("Audio Name: "+audio.title,"light_yellow"))
        audio.download(filename=removeSpecialChars(audio.title)+'.mp3', output_path='output')
        print(colored("Download is completed successfully", "light_green"))
        print(colored("Your file is saved in: ", "light_green") + colored(os.getcwd()+"\\output\n\n", "light_yellow"))
    except:
        YoutubeAnotherMethod(link)
    

def YoutubeAnotherMethod(link):
    print(colored("An error has occurred", "light_red"))
    print(colored("Trying another method.....", "light_yellow"))
    time.sleep(5)
    unlocker(link)



# removeSpecialChars function removes any invalid/special character that forbidden in naming files in windows 

def removeSpecialChars(filename):
    invalid = '<>:"/\\|?*'
    for char in invalid:
        filename = filename.replace(char, ' ')
    return filename