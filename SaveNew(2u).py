from telethon import TelegramClient, sync, events
import socks
import os
import configparser


# Reading Configs
config = configparser.ConfigParser()

# full path to config file location
config.read("/home/max/Documents/Telegram_proj/chat_mess/config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_id2 = config['Telegram']['api_id2']
api_hash2 = config['Telegram']['api_hash2']

api_hash = str(api_hash)
api_hash2 = str(api_hash2)

phone = config['Telegram']['phone']
session = config['Telegram']['session']
phone2 = config['Telegram']['phone2']
session2 = config['Telegram']['session2']
path_init = config['Telegram']['path']


client1 = TelegramClient(session, api_id, api_hash, proxy=(
    socks.SOCKS5, '96.96.33.133', 1080))  # vk messages (max account)

client2 = TelegramClient(session2, api_id2, api_hash2, proxy=(
    socks.SOCKS5, '96.96.33.133', 1080))  # tg messages


@client1.on(events.NewMessage(chats='Сообщение в VK'))
async def normal_handler(event):

    client = event.client

    user_mess = event.message.to_dict()['message']
    mess_attr = event.message

    print(name_client1 + ' got message')

    s_user_name = 'Сообщение в VK'

    file_path = 'Сообщение в VK(socialmsg_bot)'

    path = path_init + str(file_path)
    if os.path.isdir(path):
        print('folder already exists')
    else:
        os.mkdir(path)
        os.mkdir(path + '/media')

    if mess_attr.media:
        path_media = await event.message.download_media(path + '/media')
        print('File saved to ' + path_media)

    mess_date = event.message.to_dict()['date']
    mess_date = mess_date.strftime("%d-%m-%Y %H:%M")

    f = open(path + '/messages.txt', 'a+')
    f.write('from ' + s_user_name + '\n   ' + user_mess)
    if mess_attr.media:
        f.write(' (!media)')
    f.write('\n' + mess_date + '\n\n')
    print('message saved')
    f.close()


@client2.on(events.NewMessage())
async def normal_handler(event):

    client = event.client


    s_user_id = event.message.to_dict()['from_id']
    s_user_entity = await client.get_entity(s_user_id)

    # check if message came from private chat
    if s_user_entity.to_dict()['_'] == 'User' and s_user_entity.to_dict()['bot'] == False:

        print(name_client2 + ' got message')
        user_mess = event.message.to_dict()['message']
        g_user_id_dict = event.message.to_dict()['to_id']
        g_user_id = g_user_id_dict['user_id']
        mess_attr = event.message

        s_user_l_name = s_user_entity.last_name
        s_user_f_name = s_user_entity.first_name
        s_user_logname = s_user_entity.username

        g_user_entity = await client.get_entity(g_user_id)

        g_user_l_name = g_user_entity.last_name
        g_user_f_name = g_user_entity.first_name
        g_user_logname = g_user_entity.username

        if s_user_l_name:
            s_user_name = s_user_f_name + ' ' + s_user_l_name
        else:
            s_user_name = s_user_f_name

        if g_user_l_name:
            g_user_name = g_user_f_name + ' ' + g_user_l_name
        else:
            g_user_name = g_user_f_name

        if s_user_id == id_client2:
            file_path = str(g_user_name) + '(' + str(g_user_logname) + ')'
        elif g_user_id == id_client2:
            file_path = str(s_user_name) + '(' + str(s_user_logname) + ')'

        path = path_init + str(file_path)
        
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
            os.mkdir(path + '/media')

        if mess_attr.media:
            path_media = await event.message.download_media(path + '/media')
            print('File saved to ' + path_media)

        mess_date = event.message.to_dict()['date']
        mess_date = mess_date.strftime("%d-%m-%Y %H:%M")

        f = open(path + '/messages.txt', 'a+')
        f.write('from ' + s_user_name + '\n   ' + user_mess)
        if mess_attr.media:
            f.write(' (!media)')
        f.write('\n' +   mess_date + '\n\n')
        print('message saved')
        f.close()


client1.start()
client2.start()


id_client1 = client1.get_me().to_dict()['id']
id_client2 = client2.get_me().to_dict()['id']
name_client1 = client1.get_me().to_dict()['first_name']
name_client2 = client2.get_me().to_dict()['first_name']

print('Client started')

with client1:
    client1.run_until_disconnected()

with client2:
    client2.run_until_disconnected()
