from rubika.shad import Bot
from threading import Thread
import requests
import os

bot = Bot("AppName", auth="yqusnlhcmgfhetywdvbocgumwtmkidvy")
list_message_seened , retries = [] , {}

def download(link, name):
    file = requests.get(link)
    if file.status_code != 200:
        return False
    f = open(name,"wb")
    f.write(file.content)
    f.close
    return True

def send(bot,chat):
    access = chat['access']
    if chat['abs_object']['type'] == 'User' :
        text:str = chat['last_message']['text']
        if 'SendMessages' in access and chat['last_message']['type'] == 'Text' and text.strip() != '':
            text = text.strip()
            if text.startswith("!dl ["):
                link = text[5:-1]
                name = "file." + link.split(".")[-1]
                try:
                    bot.sendMessage(chat['object_guid'],"در حال یافتن لطفا صبر کنید",message_id=chat['last_message']['message_id'])
                    res = download(link,name)
                    if res:
                        bot.sendMessage(chat['object_guid'],"نصف کار انجام شده درحال آپلود فایل روی سرورای شاد",message_id=chat['last_message']['message_id'])
                        bot.sendDocument(chat['object_guid'],name,message_id=chat['last_message']['message_id'])
                    else:
                        bot.sendMessage(chat['object_guid'],"چیزی یافت نشد ❌",message_id=chat['last_message']['message_id'])
                    try:
                        os.remove(name)
                    except:
                        pass
                        
                except:
                    bot.sendMessage(chat['object_guid'],"چیزی یافت نشد ❌",message_id=chat['last_message']['message_id'])


while True:
    try:
        chats_list:list = bot.getChatsUpdate()
        if chats_list != []:
            for chat in chats_list:
                m_id = chat['object_guid'] + chat['last_message']['message_id']
                if not m_id in list_message_seened:
                    tr1 = Thread(target=send ,args=(bot, chat,))
                    tr1.start()
                    list_message_seened.append(m_id)
    except KeyboardInterrupt:
        exit()

    except Exception as e:
        if type(e) in list(retries.keys()):
            if retries[type(e)] < 3:
                retries[type(e)] += 1
                continue
            else:
                retries.pop(type(e))
        else:
            retries[type(e)] = 1
            continue                        