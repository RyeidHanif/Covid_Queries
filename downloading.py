import requests
import os

# Define the API endpoint and the local directory to save files
api_url = 'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports'
local_directory = 'covid_files'


# Fetch the file list from the GitHub API
response = requests.get(api_url)
files = response.json()

# Loop through each file and download it
for file_info in files:
    # Check if the item is a file (not a directory)
    if file_info['type'] == 'file':
        file_name = file_info['name']
        download_url = file_info['download_url']
        
        # Fetch the file content
        file_response = requests.get(download_url)
        
        # Save the file content to the local directory
        file_path = os.path.join(local_directory, file_name)
        with open(file_path, 'wb') as file:
            file.write(file_response.content)
        
        print(f'Downloaded: {file_name}')

print('All files have been downloaded.')
