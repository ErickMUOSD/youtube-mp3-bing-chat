import asyncio, json
import os
import re
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from pytube import YouTube
from alive_progress.styles import showtime


def read_txt():
    try:
        file1 = open('/home/erick/Documents/PersonalProject/youtube-downloable-music/urls_file.txt', 'r')
        return file1.readlines()
    except Exception as e:
        print('someth went wrong' + str(e))
        return None

def download_music_from_list(list_music):
    if list_music is None:
        return
    for url_song in list_music:
        print('Downloading song: ' + url_song)
        dowload_yt_video(url_song, destination='/home/erick/Documents/PersonalProject/Music_from_list')
def dowload_yt_video(url, destination):
    try:
        yt = YouTube(str(url))
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        print(yt.title + " has been successfully downloaded.")
    except Exception as e:
        print('song '+ str(url))
        print('something went wrong.' + str(e))


def extract_youtube_url(text):
    text_without_special_characters = text.replace('(', ' ').replace(')', ' ').replace('[', ' ').replace(']', ' ')

    search = re.search("(?P<url>https?://[^\s]+)", text_without_special_characters)
    if not search:
        return None

    return search.group("url")


async def main():
    cookies = json.loads(open("bing_cookies*.json", encoding="utf-8").read())  # might omit cookies option
    bot = await Chatbot.create(cookies=cookies)  # Passing cookies is "optional", as explained above

    end_system = 'N'
    while end_system == 'N' or end_system == 'n':
        print('Enter text song:')
        text = input()
        print('Enter author:')
        author = input()
        print('Skip Y/N')
        choice = input()
        if choice == 'N' or choice == 'n':
            prompt = f"Busca un video de  youtube llamado: {text} de {author} y devuelve la url "
        else:
            print('Give me a prompt:')
            prompt = input()

        try:
            print(prompt)
            response = await bot.ask(prompt,
                                     conversation_style=ConversationStyle.precise, simplify_response=True)
        except Exception as e:
            print(str(e))
            continue
        print(response['text'])
        url = extract_youtube_url(response['text'] or '')
        if not url:
            print("No se encontro la url")
        else:
            dowload_yt_video(url, destination= '/home/erick/Documents/PersonalProject/Music')
        print('Leave system ? Y/N')
        end_system = input()


if __name__ == "__main__":
    asyncio.run(main())
    # list_music = read_txt()
    # download_music_from_list(list_music)
