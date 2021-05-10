from PIL import Image, ImageDraw, ImageFont
from flask import Flask, request, json
import requests
import vk
from settings import confirmation_token, token, user_token, admin_list
from urllib.request import urlopen
import wordMaking
import coverMaking

app = Flask(__name__)
GROUP_ID = 146177467


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v=5.68)
        user_id = data['object']['user_id']
        if api.groups.isMember(group_id=GROUP_ID, user_id=user_id, access_token=token) == 0 and user_id != 75614210:
            api.messages.send(access_token=token, user_id=user_id,
                              message="Сервис доступен только подписчикам сообщества")
            return 'ok'

        elif data['object']['body'] == '&&&' and (user_id in admin_list):
            url = api.photos.getWallUploadServer(access_token=user_token, group_id=GROUP_ID)
            url = url['upload_url']
            files = {'photo': open("Adm_great.jpg", 'rb')}
            res = requests.post(url, files=files).json();

            server = res['server']
            photo = res['photo']
            res_hash = res['hash']
            save_wall_photo_result = api.photos.saveWallPhoto(access_token=user_token, group_id=GROUP_ID, server=server,
                                                              photo=photo, hash=res_hash)
            attach = "photo" + str(save_wall_photo_result[0]['owner_id']) + "_" + str(save_wall_photo_result[0]['id'])
            api.wall.post(access_token=user_token, owner_id=-GROUP_ID, from_group=1, attachment=attach)
            api.messages.send(access_token=token, user_id=user_id, message='Very nice!')
            return 'ok'

        elif ('attachments' in data['object'].keys() and 'photo' in data['object']['attachments'][0].keys() and
              data['object']['body'] != ""):
            word = data['object']['body']

            if 'photo_2560' in data['object']['attachments'][0]['photo'].keys():
                url = data['object']['attachments'][0]['photo']['photo_2560']
            elif 'photo_1280' in data['object']['attachments'][0]['photo'].keys():
                url = data['object']['attachments'][0]['photo']['photo_1280']
            elif 'photo_807' in data['object']['attachments'][0]['photo'].keys():
                url = data['object']['attachments'][0]['photo']['photo_807']
            elif 'photo_604' in data['object']['attachments'][0]['photo'].keys():
                url = data['object']['attachments'][0]['photo']['photo_604']
            else:
                url = data['object']['attachments'][0]['photo']['photo_130']

            url = url.replace("\/", '/')

            image = Image.open(urlopen(url))
            image = wordMaking.makeGreateImage(image, word)

            url = api.photos.getMessagesUploadServer(access_token=token, peer_id=user_id)
            url = url['upload_url']

            if user_id in admin_list:
                image.save("Adm_great.jpg")
                files = {'photo': open("Adm_great.jpg", 'rb')}
            else:
                image.save("great.jpg")
                files = {'photo': open("great.jpg", 'rb')}

            res = requests.post(url, files=files).json()

            server = res['server']
            photo = res['photo']
            res_hash = res['hash']
            save_wall_photo_result = api.photos.saveMessagesPhoto(access_token=token, server=server, photo=photo,
                                                                  hash=res_hash)
            attach = "photo" + str(save_wall_photo_result[0]['owner_id']) + "_" + str(save_wall_photo_result[0]['id'])
            api.messages.send(access_token=token, user_id=user_id, message="Вот, держи", attachment=attach)
            api.messages.send(access_token=token, user_id=user_id,
                              message='Можешь поделиться с друзьями или предложить новостью в паблик! ;-)')
            return 'ok'

        else:
            user_name = api.users.get(access_token=token, user_ids=user_id)
            name = user_name[0]['first_name']
            api.messages.send(access_token=token, user_id=user_id,
                              message='Привет - хуивет, ' + name + '!\nКак насчёт картинки?')
            api.messages.send(access_token=token, user_id=user_id, message='Отправь мне любое фото и слово!')
            return 'ok'
    elif data['type'] == 'group_join':
        session = vk.Session()
        api = vk.API(session, v=5.68)
        user_id = data['object']['user_id']
        user_name = api.users.get(access_token=token, user_ids=user_id)
        name = user_name[0]['first_name'] + ' ' + user_name[0]['last_name']
        word = name + ', Добро пожаловать'
        image = Image.open('coverTemplate.jpg')
        image = coverMaking.makeGreatCover(image, word)
        image.save("cover.jpg")

        url = api.photos.getOwnerCoverPhotoUploadServer(access_token=token, group_id=GROUP_ID, crop_x2=1590,
                                                        crop_y2=400)
        url = url['upload_url']
        files = {'photo': open("cover.jpg", 'rb')}
        res = requests.post(url, files=files).json()
        photo = res['photo']
        res_hash = res['hash']

        api.photos.saveOwnerCoverPhoto(access_token=token, hash=res_hash, photo=photo)

        return 'ok'
