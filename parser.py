# coding: utf-8

import os
import shutil
import zipfile

zip_path = 'zips'
source_path = 'unzips'
result_path = 'results'


for f in os.listdir(zip_path):
    print(f)
    with zipfile.ZipFile(os.path.join(zip_path,f),'r') as zip_ref:
        zip_ref.extractall(os.path.join(source_path,f[:-4]))

for f in os.listdir(source_path):
    txn = f[:5]
    print('processing txn:',txn)
    #os.rename(os.path.join(source_path,f,'images'),os.path.join(source_path,f,'images_txn'+txn))
    #os.rename(os.path.join(source_path, f, 'style.css'), os.path.join(source_path, f, 'style_txn' + txn + '.css'))
    if os.path.isdir(os.path.join(source_path,f,'images')):
        shutil.copytree(os.path.join(source_path,f,'images'), os.path.join(result_path,'images_txn'+txn))
    else:
        print('No images folder found')
    shutil.copy(os.path.join(source_path, f, 'style.css'), os.path.join(result_path, 'style_txn' + txn + '.css'))

    fin = open(os.path.join(source_path,f,'index.html'), 'rt',encoding="utf-8")
    fout = open(os.path.join(result_path,'txn'+txn+'.html'),'wt',encoding="utf-8")
    for line in fin:
        fout.write(line.replace('src="images/', 'src="images_txn' + txn + '/').replace('style.css', 'style_txn'+txn+'.css'))
    fin.close()
    fout.close()

