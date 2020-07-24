# coding: utf-8

import os
import shutil
import zipfile

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

def main():
    print('remove temp folders')
    tempFolders = ['unzips','results']
    rmTempFiles(tempFolders)
    print('unzip files to', source_path)
    unzipFilesByFolder(zip_path,source_path)
    print('modify output:', result_path)
    processUnzip(source_path,result_path)

if __name__ == '__main__':
    main()