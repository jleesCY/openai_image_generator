# ---------------------------------------------------------------------------#
# use "pip3 install openai" in a powershell to install the required library  #
# use "python3 .\generate.py" to run the program                             #
# ---------------------------------------------------------------------------#

import openai                     # to generate images
import time                       # to track time
import requests                   # to download images
import hashlib                    # to hash images for file names
import os                         # to manage the filesystem
from tkinter import filedialog    # to explore filesystem
from colorama import Fore, Style  # to change text color and style

# key
openai.api_key = open('key.txt').read()   # create a file "key.txt" (same directory as this .py file) and paste nothing but your personal openAI key inside

# valid sizes
sizes = ['256x256', '512x512', '1024x1024']

# get message prompt
msg = input(Fore.RESET + 'Prompt\n' + Fore.CYAN + '>> ' + Fore.YELLOW)

# get and validate image size
print(Fore.RESET + 'Size (1-3):\n\t1 - 256x256 (small, fastest download)\n\t2 - 512x512 (medium, balanced download)\n\t3 - 1024x1024 (large, slowest download)')
while True:
  sze = int(input(Fore.CYAN + '>> ' + Fore.YELLOW)) - 1
  if sze > 2 or sze < 0:
    print(Fore.RESET + Fore.RED + Style.BRIGHT + 'invalid entry' + Style.RESET_ALL)
    continue
  break
sze = sizes[sze]

# get and validate how many images to generate
print(Fore.RESET + 'How many (1-10)')
count = 0
while True:
  count = int(input(Fore.CYAN + '>> ' + Fore.YELLOW))
  if count > 10 or count < 1:
    print(Fore.RESET + Fore.RED + Style.BRIGHT + 'invalid entry' + Style.RESET_ALL)
    continue
  break

print(Fore.RESET + 'Generating...')

# start image generation timer
start = time.time()

# generate images
try:
  response = openai.Image.create(
    prompt=msg,
    n=count,
    size=sze
  )
except Exception as e:
  print(Fore.RED + str(e))
  print(Fore.RESET + Style.RESET_ALL)
  exit()

# stop timer
end = time.time()
# report time
print(Fore.RESET + 'Finished in ' + '[' + Fore.BLUE + str(round(end-start, 2)) + 's' + Fore.RESET + ']\n')

# print image URLs
for i in range(count):
    print(Fore.RESET + 'Image ' + str(i + 1) + ":")
    print(Fore.RESET + Fore.CYAN + str(response['data'][i]['url']))

# get and validate image download querey
print(Fore.RESET + 'Download images? (y/n)')
yn = ''
while True:
  yn = str(input(Fore.CYAN + '>> ' + Fore.YELLOW))
  if yn != "y" and yn != "n":
    print(Fore.RESET + Fore.RED + Style.BRIGHT + 'invalid entry' + Style.RESET_ALL)
    continue
  break

# downlaod images if the user wanted to
if yn == 'y':
  while True:
    path = filedialog.askdirectory(initialdir=os.getcwd() ,title='Choose a Download Folder').replace('/', '\\') + '\\' + msg + '\\'
    if path == '\\' + msg + '\\':
      print(Fore.RED + Style.BRIGHT + 'choose a directory' + Style.RESET_ALL)
      continue
    break
  for i in range(count):
    print(Fore.RESET + 'Downloading image ' + str(i + 1) + "...")
    start = time.time()
    img_data = requests.get(response['data'][i]['url']).content
    hsh = str(hashlib.md5(img_data).hexdigest())
    name = hsh + '.jpg'
    if not os.path.exists(path):
      os.makedirs(path)
    with open(path + name, 'wb') as handler:
      handler.write(img_data)
    end = time.time()
    print(Fore.RESET + '[' + Fore.BLUE + str(round(end-start, 2)) + 's' + Fore.RESET + ']\t' + Fore.YELLOW + path + name)
print(Fore.RESET + Style.RESET_ALL)