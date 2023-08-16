import json
import os
import base64
from urllib.parse import urlparse

def extract_resources_from_har(har_path, output_folder):
    with open(har_path, 'r') as f:
        data = json.load(f)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for entry in data['log']['entries']:
        url = entry['request']['url']
        parsed_url = urlparse(url)
        path = parsed_url.path.lstrip('/')

        if not path:
            path = 'index.html'
        elif path.endswith('/'):
            path = path[:-1]

        # Debug: Check for index.html in the path
        if 'index.html' in path:
            print(f"Found index.html with URL: {url}")
            if 'encoding' in entry['response']['content'] and entry['response']['content']['encoding'] == 'base64':
                print(f"Content encoding: base64")
            else:
                print(f"Content encoding: plain text")
            content_preview = entry['response']['content']['text'][:100] if 'text' in entry['response']['content'] else "No Content"
            print(f"Content starts with: {content_preview}")
    

        # Ensure directory exists
        directory = os.path.join(output_folder, os.path.dirname(path))
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Check if the resource has content
        if 'content' in entry['response'] and 'text' in entry['response']['content']:
            content = entry['response']['content']['text']

            # Debug: Check if content is empty
            if not content:
                print(f"No content found for URL: {url}")

            mime_type = entry['response']['content']['mimeType']
            if content: 
                if 'encoding' in entry['response']['content'] and entry['response']['content']['encoding'] == 'base64':
                    content = base64.b64decode(content)
                    with open(os.path.join(output_folder, path), 'wb') as f:
                        f.write(content)
                else:
                    with open(os.path.join(output_folder, path), 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == "__main__":
    # har_file_path = input("Enter the path to your .HAR file: ")
    # output_directory = input("Enter the directory where you want to save the extracted resources: ")
    output_directory = 'extracted_har'
    extract_resources_from_har('beta.character.ai.har', output_directory)
    print(f"Resources extracted to {output_directory}!")
