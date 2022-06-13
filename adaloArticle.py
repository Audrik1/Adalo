from PIL import Image, ImageFont, ImageDraw
import pandas as pd
import textwrap
from string import ascii_letters
import string
import cloudinary
import cloudinary.uploader
import cloudinary.api
import requests
import json


# Create image locally
def main():
    print("Initializing Script!")
    # Questions and image sources
    # Insert csv file name
    csvFile = #File
    # Insert Image
    imageSource = 'source.png'

    # Define font, size and color of the text
    font = ImageFont.truetype(r"DejaVuSans.ttf", 35)
    text_color = '#000000'

    # % of space taken by the text on the image
    textCoverage = .99

    # Open csv file
    datas = pd.read_csv(csvFile, encoding='utf-8')

    # Iterate on each line of the csv
    for i,row in datas.iterrows():
        question = str(row['Questions'])

        # Open source image
        empty_img = Image.open(imageSource) 

        # Create a new image
        draw = ImageDraw.Draw(im=empty_img)

        # Calculate the average length of a single character of our font
        # This takes into account the specific font and font size.
        avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
        max_char_count = int(empty_img.size[0] * textCoverage / avg_char_width)

        # Create line break
        text = textwrap.fill(text=question, width=max_char_count)

        # Add text to image
        draw.text(xy=(empty_img.size[0]/2, empty_img.size[1] / 2), text=text, font=font, fill=text_color, anchor='mm', align="center")

        # Save image locally
        empty_img.save(f'question_{i}.png')
        localImage = f'question_{i}.png'

        questionNum = i

        SendTocloudinary(localImage, questionNum)


# Upload local image to Cloudinary
def SendTocloudinary(localImage, questionNum):

    # Insert Cloudinary credentials
    cloudinary.config( 
    cloud_name = #Key, 
    api_key = #Key, 
    api_secret = #Key 
                    )
    
    # Image naming
    imageName = f'question_{questionNum}'

    # Cloudinary folder
    # Insert Cloudinary Folder name
    folder = #Folder

    cloudinary.uploader.upload(localImage, public_id = imageName, folder = folder)

    # Get uploaded url
    urlCloudinary = cloudinary.api.resources_by_ids(f'English/{imageName}')
    imageUrl = (urlCloudinary['resources'][0]['url'])

    adalo(localImage,imageUrl, questionNum)

# Send images url to Adalo
def adalo(localImage, imageUrl, questionNum):

        # Adalo credentials
        # Insert adalo token bearer
        headers = {'Content-Type': 'application/json',
            "Authorization": #Key
                    }

        # Adalo collection API
        # Insert Adalo collection URL
        url = #AdaloCollectionURL

        # Datas to be sent
        body = {
                "Name": localImage,
                "Image": imageUrl,
                "Num": questionNum
                }

        requests.post(url, data=json.dumps(body), headers=headers)


if __name__ == "__main__":
    main()

print("Process Complete!")