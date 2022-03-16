image_path = 'D:/Image/%s/%s' % ('xiaohan', '11.txt')
content = "edqweqwe"
with open(image_path, 'w') as f:
    # photo.chunks()为图片的一系列数据，它是一一段段的，所以要用for逐个读取
        f.write(content)

# D:\Image\xioahan