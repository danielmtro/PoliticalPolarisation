import os

import google.generativeai as genai
import warnings
warnings.filterwarnings("ignore")

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

from google.oauth2 import service_account
import google.auth

# Load the service account key JSON file
credentials = service_account.Credentials.from_service_account_file(
    filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/cloud-platform'],
)

# Explicitly use the credentials to authenticate
# This is an example for the Storage Client, but it would be similar for other clients
from google.cloud import storage
client = storage.Client(credentials=credentials)

import os

# ... other code ...

service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if service_account_path is None:
    raise ValueError('The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.')

genai.configure(api_key=GOOGLE_API_KEY)

from google.generativeai.types import HarmCategory, HarmBlockThreshold

def analyze_sentiment_gemini(text):
    model = genai.GenerativeModel('gemini-pro')
    message = ("Analyze the following text file and determine the sentiment score of a given line in terms of positive or negative towards the relevant candidate "
               "(i.e., Biden or Trump). Return answer in a single integer value. The sentiment score range should be -1 if negative, 1 if positive sentiment towards the candidate, and 0 for else: " + text)
    try:
        response = model.generate_content(message, safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        })
        print("API Response:", response)  # Print the full API response
        return float(response.text)
    except AttributeError as e:
        print(f"Attribute Error: {e}")
        model = genai.GenerativeModel('gemini-pro')
        return 0
    except Exception as e:
        print(f"Exception: {e}")
        model = genai.GenerativeModel('gemini-pro')
        return -0
    
# Specify the path to your text file
text_file = 'C:/Users/schma/Documents/GIT/PoliticalPolarisation/headline_txts_by_day_and_org/Headlines_2024-03-05_Output.txt'

# Determine the path for the output file
output_file_path = text_file.replace('.txt', '_SentimentScores.txt')

# Open the input file to read and the output file to write
with open(text_file, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        line = line.strip()  # Remove whitespace
        if line:  # Check if line is not empty
            score = analyze_sentiment_gemini(line)
            # Write the original line and its sentiment score to the output file
            outfile.write(f"{line}\t{score}\n")
            print(f"{line}\t{score}")
            
# Close the input and output files
infile.close()
outfile.close()
