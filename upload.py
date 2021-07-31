import hashlib
import os
from time import sleep

import pyncm
import tinytag


def getmd5(file):
    md5 = hashlib.md5()
    with open(file, 'rb') as f:
        while chunk := f.read():
            md5.update(chunk)
    return md5


def uploadfile(file):
    fsize = os.stat(file).st_size
    md5 = getmd5(file).hexdigest()
    fname = os.path.basename(file)
    fext = file.split('.')[-1]

    try:
        info = tinytag.TinyTag.get(file)
    except:
        print("文件有误! 无法读取信息!")
        return

    cresult = pyncm.cloud.GetCheckCloudUpload(md5)
    songId = cresult['songId']
    token = pyncm.cloud.GetNosToken(fname, md5, str(fsize), fext)['result']

    if cresult['needUpload']:
        pyncm.cloud.SetUploadObject(open(file, 'rb'), md5, fsize, token['objectKey'], token['token'])

    while True:
        try:
            submit_result = pyncm.cloud.SetUploadCloudInfo(token['resourceId'], songId, md5, fname, info.title,
                                                           info.artist,
                                                           info.album, info.bitrate)
            publish_result = pyncm.cloud.SetPublishCloudResource(submit_result['songId'])
            break
        except KeyError:
            submit_result = pyncm.cloud.SetUploadCloudInfo(token['resourceId'], songId, md5, fname)
            publish_result = pyncm.cloud.SetPublishCloudResource(submit_result['songId'])
            break
        except Exception:
            sleep(5)

    if publish_result['code'] == 200:
        return True
    else:
        return False



