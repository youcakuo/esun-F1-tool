# coding: utf-8

import os
import shutil
import zipfile
from PIL import Image

zip_path = 'zips'
source_path = 'unzips'
result_path = 'results'


def unzipFilesByFolder(src, dst):
    for f in os.listdir(src):
        print(f)
        with zipfile.ZipFile(os.path.join(src,f),'r') as zip_ref:
            zip_ref.extractall(os.path.join(dst,f[:-4]))

def processUnzip(src, dst):
    for f in os.listdir(src):
        txn = f[:5]
        print('processing txn:',txn)
        #os.rename(os.path.join(source_path,f,'images'),os.path.join(source_path,f,'images_txn'+txn))
        #os.rename(os.path.join(source_path, f, 'style.css'), os.path.join(source_path, f, 'style_txn' + txn + '.css'))
        if os.path.isdir(os.path.join(src,f,'images')):
            shutil.copytree(os.path.join(src,f,'images'), os.path.join(dst,'images_txn'+txn))
        else:
            print('No images folder found')
        shutil.copy(os.path.join(src, f, 'style.css'), os.path.join(dst, 'style_txn' + txn + '.css'))

        fin = open(os.path.join(src,f,'index.html'), 'rt',encoding="utf-8")
        fout = open(os.path.join(dst,'txn'+txn+'.html'),'wt',encoding="utf-8")
        for line in fin:
            fout.write(line.replace('src="images/', 'src="images_txn' + txn + '/').replace('style.css', 'style_txn'+txn+'.css'))
        fin.close()
        fout.close()

def rmTempFiles(folders):
    for folder in folders:
        print(folder, 'removed')
        shutil.rmtree(folder, ignore_errors=True)

#convert html which generated from docx via internet tool to F1 function format
def main():
    print('remove temp folders')
    tempFolders = ['unzips','results']
    rmTempFiles(tempFolders)
    print('unzip files to', source_path)
    unzipFilesByFolder(zip_path,source_path)
    print('modify output:', result_path)
    processUnzip(source_path,result_path)

def pngTojpeg(src):
    for f in os.listdir(src):
        print(f)
        if f.startswith('images_txn') and os.path.isdir(os.path.join(src,f)):
            for img in os.listdir(os.path.join(src,f)):
                print(img)
                if img.endswith('.png'):
                    im = Image.open(os.path.join(src,f,img))
                    rgb_im = im.convert('RGB')
                    print('save',img[:-4]+'.jpg')
                    rgb_im.save(os.path.join(src,f,img[:-4]+'.jpg'),optimize=True,quality=5)
                    os.remove(os.path.join(src,f,img))
        elif f.endswith('.html'):
            fin = open(os.path.join(src, f), 'rt', encoding="utf-8")
            fout = open(os.path.join(src, 'tmp'+f), 'wt', encoding="utf-8")
            for line in fin:
                fout.write(line.replace('.png', '.jpg'))
            fin.close()
            fout.close()
            os.remove(os.path.join(src,f))
            os.rename(os.path.join(src, 'tmp'+f),os.path.join(src, f))

def main2():
    pngTojpeg(result_path)


if __name__ == '__main__':
    main2()