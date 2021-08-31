# Call the mathpix API to convert image to LaTex
import sys
import base64
import requests
import json
import os
import re
import time

count = 0

# Call the mathpix API to convert image to LaTex, return the LaTex code found
# in the image, or 'no math' if the API doesn't find any code
def get_latex(file_name):
    try:
        count = 0
        file_path = os.path.join('Imágenes recuperadas',file_name)
        image_uri = "data:image/jpg;base64," + base64.b64encode(open(file_path, "rb").read()).decode('ascii')
        r = requests.post("https://api.mathpix.com/v3/latex",
            data=json.dumps({'url': image_uri}),
            headers={"app_id": "mjbar", "app_key": "0a1fb3289b285f9351e3fb0911d06ec7",
                    "Content-type": "application/json"})
#        print(json.dumps(json.loads(r.text), indent=4, sort_keys=True))
# r is response type, so it seems that it can't be parsed
# r.text is str type
        err = re.findall('"error":"(.*?)"', r.text)[0]
        if len(err) > 0:
            return 'F'
        else:
            confidence = float(re.findall('"latex_confidence":(.*?),', r.text)[0])
            if confidence <= 0.8:
                return re.findall('"latex":"(.*?)"', r.text)[0] + '   <--REVISAR'
            else:
                return re.findall('"latex":"(.*?)"', r.text)[0]
    except:
        print('\n No way to handle the image:', file_name)


# Replace '\\' for '\' in the LaTex code (escaped characters)
def clean_latex(cod):
    try:
        return cod.replace('\\\\', '\\')
    except:
        return 'F'


# Get the clean LaTex code from every .jpg image found in the
# 'Imágenes recuperadas' folder, and write it on a .txt file called
# 'Fórmulas.txt'. If the image belongs to a new .docx file (this is known
# because of its name), first it writes the name of the .docx file as a header.
docs = []
form_path = os.path.join('Imágenes recuperadas', 'Fórmulas.txt')
fhand = open(form_path,'w')
fhand.write('Fórmulas de exámenes: \n')
for nombrefichero in os.listdir('Imágenes recuperadas'):
    if not (nombrefichero.endswith('.jpg') or nombrefichero.endswith('.jpeg')): continue
    nombredoc = re.findall('(.+)_[0-9]*\.', nombrefichero)[0]
    if nombredoc not in docs:
        docs.append(nombredoc)
        fhand.write('\n' + nombredoc + '\n\n')
        print('\n .docx file:', nombredoc)
    print('\n Getting LaTex from:', nombrefichero)
    latex = clean_latex( get_latex(nombrefichero) )
    if len(latex) < 2: continue
    fhand.write(latex + '\n')
    print('LaTex:', latex)
    count = count + 1
    if count % 10 == 0 :
        print('\n Pausing for a bit...')
        time.sleep(1)
fhand.close()
