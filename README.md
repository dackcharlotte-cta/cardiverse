# Cardiverse

## Overview of Project

Cardiverse is a platform for personalised greeting cards that utilises AI to create:

- Custom 3D avatars
- Custom poem about the reciever 
- Semi Customisable theme

The platform enables users to celebrate special occasions by sending personalised virtual greeting cards.

------

## Setup

### Clone the Repo

To set up the project locally, you first need to clone the repository. Follow these steps:

1. **Ensure Prerequisites Are Installed**
    Make sure you have Git installed on your machine. You can download it from [git-scm.com](https://git-scm.com/).

2. **Get the Repository URL**
    Navigate to the repository page on GitHub. Click the green **Code** button and copy the URL of the repository. For example:

   - HTTPS: `https://github.com/dackcharlotte-cta/cardiverse.git`
   - SSH: `git@github.com:dackcharlotte-cta/cardiverse.git`

3. **Clone the Repository from your command-line** (example for SSH)
    Open your terminal and navigate to the directory where you want the project to reside. Use the `git clone` command followed by the repository URL:

   ```bash
   git clone git@github.com:dackcharlotte-cta/cardiverse.git
   ```

4. **Navigate to the Project Folder**

   ```bash
   cd repository
   ```

### Install Dependencies

1. Create a virtual environment in your command-line:

   ```bash
   virtualenv venv
   ```

2. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

   If the requirements file does not work, manually install the following:

   - Flask
   - requests

------

### Setting up API Keys

#### Meshy API

1. Obtain your API key from [Meshy Documentation](https://docs.meshy.ai/).

2. Create a JSON file named `meshy_keys.json` in your project directory with the following content:

   ```json
   {
     "Authorization": "{your_key}"
   }
   ```

#### OpenAI API

1. Obtain your API key from [OpenAI](https://openai.com/index/openai-api/).

#### Azure Environment Keys

1. Obtain your Azure key and endpoint.

2. Set them via the command line:

   ```bash
   set AZURE_KEY={your_key}
   set AZURE_ENDPOINT={your_link}
   ```

3. Alternatively, create a JSON file named `azure_keys.json` with the following content:

   ```json
   {
     "AZURE_KEY": "{your_key}",
     "AZURE_ENDPOINT": "{your_link}"
   }
   ```

Demo: 

