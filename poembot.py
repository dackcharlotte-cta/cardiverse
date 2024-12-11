#chatbot that writes poem for cover 

from openai import AzureOpenAI
import os

#for debugging 
#occasion = "birthday"
#user_message = "Gonzalo loves tennis, playing the guitar and seeing historical places "
#recievers_name = "Gonzalo"

client = AzureOpenAI(
	api_key = os.getenv("AZURE_KEY"),
	azure_endpoint = os.getenv("AZURE_ENDPOINT"),
	api_version = "2023-10-01-preview"
)


def get_poem(user_message, recievers_name, occasions):
	messages = [
		{"role": "system", "content": f"Can you create a rhyming peom, word limit: 15, about {recievers_name} using {user_message} and {occasions} that is the formate 'for the person who, .... ' I will write happy birthday at the end, then after a hyphen, then use {user_message} and {occasions} to create a image prompt for an image generations platfrom, no human/people should be in the image."},
		{"role": "user", "content": user_message}
	]
	response = client.chat.completions.create(
		model = "GPT-4",
		messages = messages
	)
	return response.choices[0].message.content

#for debugging 
#get_poem(user_message, recievers_name, occasion)