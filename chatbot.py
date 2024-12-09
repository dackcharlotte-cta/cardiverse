from openai import AzureOpenAI
import os
import requests
import json

client = AzureOpenAI(
	api_key = os.getenv("AZURE_KEY"),
	api_version = "2023-10-01-preview",
	azure_endpoint = os.getenv("AZURE_ENDPOINT")
)

messages = [
		{"role": "system", "content": f"Respone using the {user_message} as inspirations to create a poem about {recievers_name}"}
]

def get_music_for_r(user_message, recievers_name):
	url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={fiat_currency}"
	response = requests.get(url)
	print(url)
	data = response.json()
	current_price = [coin['current_price'] for coin in data if coin['id'] == crypto_name][0]
	#current_price = next((coin['current_price'] for coin in data if coin['id'] == crypto_name), None)

	return f"The current price of {crypto_name} is {current_price} {fiat_currency}"

functions = [
	{
		"type": "function",
		"function": {
			"name": "get_music_for_r",
			"description" : "Gets music that is inspired by users input", 
			"parameters": {
			#letting chat - gbt know that its getting 
			#key value pairs 
				"type": "object",
				"properties": {
					"crypto_name": {
						"type": "string",
						"description": "The name of crypto currency that i want to look up"
					},
					"fiat_currency": {
						"type": "string",
						"description": "The fiat currency for defining the price of crypto currency. use the offical abbrivation of the fiat currency"
					}
				},
				"required": ["crypto_name", "fiat_currency"]
				
			}
		}
	}
]




def ask_question(user_question):
	#building a memory/conversation 
	messages.append({"role": "user", "content": user_question})

	response = client.chat.completions.create(
		model = "GPT-4",
		messages = messages,
		tools = functions,
		tool_choice = "auto" 
	)

	response_message = response.choices[0].message

	#if vchat gbt does need help this will be none otherwuse there will be stiff 
	gbt_tools = response.choices[0].message.tool_calls

	#if gbts tool is not none
	#gbt_tools is a list  
	if gbt_tools:

		#need to give the Who wants to be a millionaire team the phone number 
		#set up a 'phonebook' , if we see a funcation name, we need to tell our code which function to call 
		available_functions = {
		"get_music_for_r" : music_for_r
		}

		messages.append(response_message)

		for gbt_tools in gbt_tools:
			#figure out which friend to call 
			function_name = gbt_tools.function.name
			function_to_call = available_functions[function_name]
			function_parameters = json.loads(gbt_tools.function.arguments)
			sam_response = function_to_call(function_parameters.get("crypto_name"), function_parameters.get("fiat_currency"))
			messages.append(
				{
					"tool_call_id": gbt_tools.id,
					"role": "tool", #new role type user is them and tool is what we need 
					"name": function_name,
					"content": sam_response
				}
			)
			second_response = client.chat.completions.create(
				model = "GPT-4",
				messages=messages
			)
			#this responses happens if you use the crypto funcation
			return second_response.choices[0].message.content
	else:
		# this is the chatbot reponse if no external funcaiton is used 	
		return response.choices[0].message.content
		