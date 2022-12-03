# ---------------------------------------------------------------------------#
# use "pip3 install openai" in a powershell to install the required library  #
# use "python3 .\generate.py" to run the program                             #
# ---------------------------------------------------------------------------#

import openai     # to generate images
import time       # to track time
import requests   # to download images
import hashlib    # to hash images for file names
import os         # to manage the filesystem

# key
openai.api_key = open('key.txt').read()   # create a file "key.txt" (same directory as this .py file) and paste nothing but your personal openAI key inside

# valid sizes
sizes = ['256x256', '512x512', '1024x1024']

# get message prompt
msg = input('Prompt\n>> ')

# get and validate image size
while True:
  sze = int(input('Size (1-3):\n\t1 - 256x256 (small, fastest download)\n\t2 - 512x512 (medium, balanced download)\n\t3 - 1024x1024 (large, slowest download)\n>> ')) - 1
  if sze > 2 or sze < 0:
    print('invalid entry')
    continue
  break
sze = sizes[sze]

# get and validate how many images to generate
count = 0
while True:
  count = int(input('How many (1-5)\n>> '))
  if count > 5 or count < 1:
    print('invalid entry')
    continue
  break

print('Generating...')

# start image generation timer
start = time.time()

# generate images
try:
  response = openai.Image.create(
    prompt=msg,
    n=count,
    size=sze
  )
except:
  print('Error with generation. Try again or try a different prompt')
  exit()

# stop timer
end = time.time()
# report time
print('Finished in ' + str(round(end-start, 3)) + 's\n')

# print image URLs
for i in range(count):
    print('Image ' + str(i + 1) + ":")
    print(str(response['data'][i]['url']) + '\n')

# get and validate image download querey
yn = ''
while True:
  yn = str(input('Download images? (y/n)\n>> '))
  if yn != "y" and yn != "n":
    print('invalid entry')
    continue
  break

# downlaod images if the user wanted to
if yn == 'y':
  for i in range(count):
    print('Downloading image ' + str(i + 1) + "...")
    start = time.time()
    img_data = requests.get(response['data'][i]['url']).content
    hsh = str(hashlib.md5(img_data).hexdigest())
    name = hsh + '.jpg'
    path = os.getcwd() + '\\' + msg + '\\'
    if not os.path.exists(path):
      os.makedirs(path)
    with open(path + name, 'wb') as handler:
      handler.write(img_data)
    end = time.time()
    print('(' + str(round(end-start, 3)) + 's)\t' + path + name)