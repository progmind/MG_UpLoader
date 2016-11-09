#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import dropbox
import qrcode

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

BASEDIR = os.path.abspath(os.path.dirname(__file__))
dbx = dropbox.Dropbox("アクセストークン")
QRsavedir = 'QRコードを保存したいフォルダのパス'

def getext(filename):
    return os.path.splitext(filename)[-1].lower()

class ChangeHandler(FileSystemEventHandler):
    print('★監視しているフォルダ')
    print('　'+ os.path.abspath(os.path.dirname(__file__)))
    print('★QRコードを保存するフォルダ')
    print('　'+ QRsavedir)
    
    def on_created(self, event):
        if event.is_directory:
            return
        if getext(event.src_path) in ('.jpg','.png','.txt'):	
            print('\n◆マンガが生成されました')
            #print('　ファイルパスは %s です\n' % event.src_path)
            path = event.src_path
            print('　Dropboxにアップロードします')
            file = os.path.basename(path)
            print('　ファイル名は' + file + 'です\n')

            with open(file, 'rb') as f:
                dbx.files_upload(f.read(), '/'+ file)
            data = dbx.sharing_create_shared_link_with_settings('/' + file)
            print('　アップロード完了しました。ファイルのURLは')

            print('　' + data.url)
            print('　です\n')
            print('　QRコードの画像を生成します')

            encode_text = data.url
            img = qrcode.make(encode_text)
            type(img)
            img.save(QRsavedir +'/QR_'+ file)
            print('　QRコードを表示＆保存しました\n')
            img.show()




if __name__ in '__main__':
    while 1:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler,BASEDIR,recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
