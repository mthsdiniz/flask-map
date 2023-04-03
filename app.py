from flask import Flask, render_template, jsonify, request
import requests
from urllib.parse import quote
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-file')
def fetch_file():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL not provided"}), 400

    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return jsonify({"error": "Failed to fetch file"}), response.status_code

@app.route('/get-files')
def get_files():
    # Replace with your own repository owner, repository name, and GitHub access token
    owner = 'NewFrontiers'
    repo = 'china_optical_pipelines'
    access_token = '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'

    # Set up headers with access token
    headers = {'Authorization': f'token {access_token}'}

    # Recursive call to get all files in repository
    def get_files_recursive(path):
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{quote(path)}'
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            files = []
            for item in response.json():
                if item['type'] == 'file':
                    if re.match(r'.*\.geojson$|.*\.kml$', item['name']):
                        files.append({
                            'name': item['name'],
                            'url': item['download_url']
                        })
                elif item['type'] == 'dir':
                    files += get_files_recursive(item['path'])
            return files
        else:
            return []

    files = get_files_recursive('')
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True)
