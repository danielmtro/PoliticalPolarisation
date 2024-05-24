from google.oauth2 import service_account
import google.generativeai as genai
import warnings
import os
warnings.filterwarnings("ignore")

import os
from google.oauth2 import service_account

service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if service_account_path is None:
    raise ValueError('The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.')

print("Using service account file at:", service_account_path)

# Load the service account key JSON file
credentials = service_account.Credentials.from_service_account_file(
    filename=service_account_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform'],
)
import os
print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

# Load the service account key JSON file
service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if service_account_path is None:
    raise ValueError('The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.')

credentials = service_account.Credentials.from_service_account_file(
    filename=service_account_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform'],
)

# Configure the genai client with your credentials
genai.configure(credentials=credentials)

from google.generativeai.types import HarmCategory, HarmBlockThreshold

def analyze_sentiment_gemini(text):
    model = genai.GenerativeModel('gemini-pro')
    message = ("Analyze the following text and determine the sentiment score of a given line "
               "in terms of positive or negative towards the relevant candidate "
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
        return 0
    except Exception as e:
        print(f"Exception: {e}")
        return -0
    
text_file = 'C:/Users/schma/Documents/GIT/PoliticalPolarisation/headline_txts_by_day_and_org/Headlines_2024-03-05.txt'

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
