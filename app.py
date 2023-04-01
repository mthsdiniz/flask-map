import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/geojson-files')
def geojson_files():
    owner = 'mthsdiniz'  # Replace with the owner of the GitHub repository
    repo = 'geojsons'  # Replace with the name of the GitHub repository
    # Use local
    #github_api_url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    #response = requests.get(github_api_url)

    # Use Enterprise
    github_enterprise_base_url = 'https://your_github_enterprise_instance.com'  # Replace with your GitHub Enterprise base URL
    github_api_url = f'{github_enterprise_base_url}/api/v3/repos/{owner}/{repo}/contents'

    headers = {'Authorization': 'token your_access_token'}
    response = requests.get(github_api_url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        geojson_files = [
            {'name': file['name'], 'url': file['download_url']}
            for file in files
            if file['name'].endswith('.geojson')
        ]
        return jsonify(geojson_files)
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)