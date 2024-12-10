from openai import AzureOpenAI 
import os
import requests
import json
from PIL import Image
import datetime


def get_image(bot_prompt): 
	client = AzureOpenAI(
	api_key = os.getenv("AZURE_KEY"),
	api_version = "2023-12-01-preview",
	azure_endpoint = os.getenv("AZURE_ENDPOINT")
	)


	dalle_result = client.images.generate(
	model = "dalle3",
	prompt = bot_prompt,
	n=1,
	style = "vivid"
	)


	json_repsonse = json.loads(dalle_result.model_dump_json())

	#making/setting up file path/ a new folder 
	image_dir = os.path.join(os.curdir, 'images')

	#if doesnt exist 
	#go ahead and make it 
	if not os.path.isdir(image_dir):
		os.mkdir(image_dir)

	#my image path, name of the foldere +, plus file name
	date_now = str(datetime.datetime.now())
	date_now = date_now.replace('.', '_').replace(':', '_')

	image_path = os.path.join(image_dir, 'cover' + date_now +'.png') 
	#if you want to have to save image over the time, you can add a counter, maybe by getting date
	image_url = json_repsonse['data'][0]['url']

	#generate the image, gives you a URL for image not the actual image
	generate_image = requests.get(image_url).content 

	#save image in folder
	#wb = write to binary 
	with open(image_path, 'wb') as file: 
		file.write(generate_image) 

	#have python open hte image file
	#bonus step nice debugger
	image = Image.open(image_path)
	image.show() 
	return 'cover' + date_now +'.png'