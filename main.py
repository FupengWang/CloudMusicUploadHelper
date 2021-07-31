from login import login
from upload import uploadfile
from decrypt import decrypt
import sys, os, time

def addToList(file:str, uplist:list):
    ext = file.split('.')[-1]
    if ext == 'ncm':
        uplist.append(decrypt(file))
    elif ext in ['MP3', 'mp3', 'flac', 'FLAC', 'WAV', 'wav', 'M4A', 'm4a', 'acc', 'ACC']:
        uplist.append(file)

if __name__ == '__main__':
    login(debug=True)

    uploadList = []

    try:
        arg = sys.argv[1]
        args = sys.argv[1:]
    except IndexError:
        print("请输入欲上传的文件或目录")
        args = [input(">>>")]

    for item in args:
        if os.path.isdir(item):
            lst = os.listdir(item)
            for kids in lst:
                addToList(os.path.join(item, kids), uploadList)
        else:
            addToList(item, uploadList)

    uploadList = list(set(uploadList))
    count = 0

    for item in uploadList:
        fileName = item.split("\\")[-1]
        while True:
            try:
                uploadfile(item)
                count = count + 1
                print(f"{fileName}上传完成!")
            except Exception:
                print(f"{fileName}上传出错, 正在重试...")
                time.sleep(5)

    input(f"完成!共上传{count}首歌曲!\n按回车键退出...")
