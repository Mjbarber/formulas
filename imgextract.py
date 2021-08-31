import zipfile
import re
import os

count = 0

# Extract .docx file, get a a list of its files and a sublist of its images,
# then read them and rewrite them in the 'Imágenes recuperadas' folder
# with a proper name (name of the .docx file + number of image + extension)
def ext_im(docnam, cont):
    try:
        document = zipfile.ZipFile(docnam)
        filelist = document.namelist()

        imagelist = [filename for filename in filelist if re.search('.*image.*', filename)]
        imagelist.sort()

        print('\n List of images in', docnam, ':', '\n', imagelist, '\n')

        if not os.path.isdir('Imágenes recuperadas'): os.mkdir('Imágenes recuperadas')

        for image in imagelist:
            imgdata = document.read(image)
# This line would just get the name of the .docx file, with no full path
#            image_pre = re.findall('([^\\\]+)\.', docnam)[0] + '_'
            image_pre = docnam.replace('\\', '-')
            image_pre = re.findall('.-(.+)\.', image_pre)[0] + '_'
            image_ext = re.findall('([0-9]+\..{2,4}$)', image)[0]
            imagename = image_pre + image_ext
            imagepath = os.path.join('Imágenes recuperadas', imagename)
            if os.path.exists(imagepath): continue
            print('Extrating image:', imagename)
            fhand = open(imagepath, 'wb')
            fhand.write(imgdata)
            fhand.close()
            cont = cont + 1
        document.close()
    except:
        print('\n No way to extract images from:', docnam)
    return cont

# Walk the whole tree of folders and extract images from the .docx files found
for (nombredir, dirs, ficheros) in os.walk('.'):
    for nombrefichero in ficheros:
        if not (nombrefichero.endswith('.doc') or nombrefichero.endswith('.docx')): continue
# The following lines make the loop to extract images only from files which
# name contains some key-words related to controls, exams...
        key_words = ['control', 'examen', 'exámenes', 'evaluación', 'evaluacion',
                    'recuperación', 'recuperacion', 'rec']
        flag = 0
        for key_word in key_words:
            if re.search(key_word, nombrefichero.lower()):
                flag = 1
        if flag == 0: continue
###
        elfichero = os.path.join(nombredir, nombrefichero)
        count = ext_im(elfichero, count)

print('\n', 'Number of images extracted:', count)
