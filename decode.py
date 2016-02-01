import base64
file=open('D:/wp/PycharmProjects/ltxszw/都市言情/蓝领情缘/3p.txt','rb')
data=file.read()
data=base64.b64decode(data)
data=data.decode('utf-8')
print(data)
file.close()