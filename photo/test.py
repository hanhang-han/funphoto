from PIL import Image


def thumb_made(image_url):
    im = Image.open(image_url)
    im.thumbnail((200,100))
    thumb_url ='_thumb.'.join(image_url.rsplit('.'))
    im.save(thumb_url)
    return 'finsihed'
image_url = 'D:/Image/hh/亚马逊.png'
thumb_made(image_url)
