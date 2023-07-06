import asyncio, json
import os
import re
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from pytube import YouTube


def dowload_yt_video(url):
    try:
        yt = YouTube(str(url))
        video = yt.streams.filter(only_audio=True).first()
        destination = '/home/erick/Documents/PersonalProject/Music'
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        print(yt.title + " has been successfully downloaded.")
    except Exception as e:
        print('something went wrong.' + str(e))


def extract_youtube_url(text):
    text_without_special_characters = text.replace('(', ' ').replace(')', ' ').replace('[', ' ').replace(']', ' ')
    return re.search("(?P<url>https?://[^\s]+)", text_without_special_characters).group("url")


async def main(text, author):
    cookies = json.loads(open("bing_cookies*.json", encoding="utf-8").read())  # might omit cookies option
    bot = await Chatbot.create(cookies=cookies )  # Passing cookies is "optional", as explained above
    response = await bot.ask(prompt=f"Busca un video de youtube llamado: {text} de  {author} y retorna  la url ",
                             conversation_style=ConversationStyle.precise, simplify_response=True)
    # response = json.dumps(response, indent=2)
    print(response['text'])
    await bot.close()
    return response['text']


if __name__ == "__main__":
    text = asyncio.run(main(text="Lagrimas de escarcha", author="Gatos negros del tiberio"))
    url = extract_youtube_url(text)
    dowload_yt_video(url)
