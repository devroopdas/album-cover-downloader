from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

#iTunes API URL
ITUNES_API_URL = "https://itunes.apple.com/search"

@app.route("/")
def home():
    return "Album Cover Downloader API is running!"

@app.route("/search", methods=["GET"])
def search_album():
    query = request.args.get("album")
    if not query:
        return jsonify({"error": "Please provide an album name"}), 400
    
    #Request iTunes API
    params = {"term": query, "media": "music", "entity": "album", "limit": 5}
    response = requests.get(ITUNES_API_URL, params=params)
    data = response.json()
    print(data)

    #Extracting the album cover
    if "results" in data and len(data["results"]) > 0:
        albums=[]
        for album_data in data["results"]:
            albums.append({
                "album": album_data["collectionName"], #Album Name
                "artist": album_data["artistName"],
                "cover_url": album_data["artworkUrl100"].replace("100x100", "1000x1000")
            })
        return jsonify({"results": albums})
    else:
        return jsonify({"error": "No albums found"}), 404



if __name__ == "__main__":
    app.run(debug=True)