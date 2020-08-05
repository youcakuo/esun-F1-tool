# coding: utf-8

import os
import shutil
import zipfile
from PIL import Image
import zipfile
import argparse

zip_path = 'zips'
source_path = 'unzips'
result_path = 'results'
html_path = 'html_backup'
backup_path = 'D:\\work\\esun\\F1\\results\\total'
jar_file = 'org.eclipse.helpcr_1.0.0.201410150948.jar'
jar_backup = 'backup'

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
                    rgb_im.save(os.path.join(src,f,img[:-4]+'.jpg'),optimize=True,quality=7)
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

def copy_html_without_docx(src, dst):
    tmp = []
    for f in os.listdir(dst):
        if f.startswith('txn') and f.endswith('.html'):
            tmp.append(f[:-5])
    for f in os.listdir(src):
        if os.path.isfile(os.path.join(src,f)) and not f[:8] in tmp:
            shutil.copyfile(os.path.join(src,f), os.path.join(dst,f))
            print('copy file without change: ', f)

def copy_backup_files(src, dst):
    if os.path.isfile(jar_file):
        print('remove jar file', jar_file)
        os.remove(jar_file)
    print('delete folder', dst)
    shutil.rmtree(dst, ignore_errors=True)
    print('copy folder from', src, 'to', dst)
    shutil.copytree(src,dst)

def main2():
    copy_backup_files(backup_path,result_path)
    pngTojpeg(result_path)
    copy_html_without_docx(html_path,result_path)

def getNewTxnList(src):
    result = []
    for f in os.listdir(src):
        if f.startswith('images_txn') and os.path.isdir(os.path.join(src,f)):
            result.append(f[7:])
    return result

def pngTojpeg2(src, qt):
    src = src + '//html'
    newTxn = getNewTxnList(src)
    print('newTxn:', newTxn)
    for f in os.listdir(src):
        # print(f)
        if f.startswith('images_txn') and os.path.isdir(os.path.join(src,f)):
            for img in os.listdir(os.path.join(src,f)):
                print('processing', f, img)
                if img.endswith('.png'):
                    im = Image.open(os.path.join(src,f,img))
                    rgb_im = im.convert('RGB')
                    # print('save',img[:-4]+'.jpg')
                    rgb_im.save(os.path.join(src,f,img[:-4]+'.jpg'),optimize=True,quality=qt)
                    os.remove(os.path.join(src,f,img))
        elif f.endswith('.html') and f[:-5] in newTxn:
            print('processing', f)
            fin = open(os.path.join(src, f), 'rt', encoding="utf-8")
            fout = open(os.path.join(src, 'tmp'+f), 'wt', encoding="utf-8")
            for line in fin:
                fout.write(line.replace('.png', '.jpg'))
            fin.close()
            fout.close()
            os.remove(os.path.join(src,f))
            os.rename(os.path.join(src, 'tmp'+f),os.path.join(src, f))
        elif (f.endswith('.jpg') or f.endswith('png') or f.endswith('gif')) and f[:8] in newTxn:
            os.remove(os.path.join(src,f))

def jar_folder(src):
    os.chdir(src)
    os.system('jar -cvfM ' + jar_file + ' ./')
    shutil.move(jar_file, os.path.join('../',jar_file))

def extract_jar_files(src, dst):
    print('copy jar file from', os.path.join(src, jar_file))
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    shutil.copyfile(os.path.join(src, jar_file), os.path.join(dst, jar_file))
    print('extract jar file to', dst)
    with zipfile.ZipFile(os.path.join(dst, jar_file)) as z:
        z.extractall(dst)
    print('remove jar file', os.path.join(dst, jar_file))
    os.remove(os.path.join(dst, jar_file))

def main3(quality):
    extract_jar_files(jar_backup, result_path)
    pngTojpeg2(result_path, quality)
    jar_folder(result_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quality', help='轉出圖檔品質')
    args = parser.parse_args()
    quality = int(args.quality) if args.quality else 30

    main3(quality)