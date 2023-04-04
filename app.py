from flask import Flask, render_template, jsonify, request
import requests
from urllib.parse import quote
import re
import os

## Remove for deploying
import config

proxy = 'http://web.prod.proxy.cargill.com:4300'
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
os.environ['REQUESTS_CA_BUNDLE'] = r'./static/cacert.pem'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-file')
def fetch_file():
    url = request.args.get('url')
    access_token = request.args.get('ghtoken')
    
    if access_token == '' or access_token == None:
        access_token = config.access_token
    
    if not url:
        return jsonify({"error": "URL not provided"}), 400
    
    new_url = url.split('?')[0]
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(new_url, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        return jsonify({"error": "Failed to fetch file"}), response.status_code

@app.route('/get-files')
def get_files():

    owner = request.args.get('owner')
    repo = request.args.get('repo')
    access_token = request.args.get('ghtoken')

    if owner == '':
        owner = 'NewFrontiers'
    if repo == '':
        repo = 'china_optical_pipelines'
    if access_token == '':
        access_token = config.access_token

    # Set up headers with access token
    headers = {'Authorization': f'token {access_token}','Accept':'application/vnd.github+json'}

    # Recursive call to get all files in repository
    def get_files_recursive(path):
        
        url = f'https://git.cglcloud.com/api/v3/repos/{owner}/{repo}/contents/{quote(path)}'
        response = requests.get(url, headers=headers)
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
