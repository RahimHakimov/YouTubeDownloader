import re
import requests
import os
from pytube import YouTube


def folder_name(url):
    try:
        requests.get(url)
    except:
        print("No internet connection... :(")
        return 0

    if 'list=' in url:
        cPL = url[url.rfind('=') + 1:]

    else:
        print("Incorrect Playlist...:(")
        return 0

    return cPL


def link_generator(url):
    try:
        res = requests.get(url)
    except:
        print("No internet connection... :(")
        return 0

    plain_text = res.text

    if "list=" in url:
        cPL = url[url.rfind('=') + 1:]
    else:
        print('Incorrect Playlist.')
        return 0

    tmp_material = re.compile(r"watch\?v=\S+?list=" + cPL)
    material = re.findall(tmp_material, plain_text)

    videos_links = []

    for cur in material:
        current_link = "https://youtube.com/" + cur.replace("&amp;", '&')
        if current_link not in videos_links:
            videos_links.append(current_link)

    return videos_links


inputted_url = input("WELCOME to YouTube - playlist DOWNLOADER\n author: @RahimHakimov\n" + "Enter playlist url: ")

os.chdir(os.getcwd())

new_folder = folder_name(inputted_url)

try:
    os.mkdir(new_folder[:8])
except:
    temp = 0

os.chdir(new_folder[:8])

downloaded_videos = []

for path_to_folder, s, files in os.walk('.', topdown=False):
    for name in files:
        if os.path.getsize(os.path.join(path_to_folder, name)) < 1:
            os.remove(os.path.join(path_to_folder, name))
        else:
            downloaded_videos.append(str(name))

videos_links = link_generator(inputted_url)

for current_link in videos_links:
    try:
        current_youtube_video = YouTube(current_link)
        main_title = current_youtube_video.title
        main_title = main_title + ".mp4"
        main_title = main_title.replace('|', '')
    except:
        print("Connection problem... :(")
        break

    if main_title not in downloaded_videos:
        vid = current_youtube_video.streams.filter(progressive=True, file_extension='mp4').first()

        if os.path.exists(str(os.getcwd()) + "/" + str(vid.default_filename)):
            print("Exists. . . " + vid.default_filename)

            s = input("Enter 1 to delete exists file and download new\nEnter 0 to keep this file and continue\n")

            if s == "0":
                continue

        print("Downloading. . . " + vid.default_filename)
        vid.download(os.getcwd())
        print("Video Downloaded!")

print(f"Downloading finished!\nSaved at: {os.getcwd()}")
