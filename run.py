import os

from podcastbuzz import app

if __name__ == '__main__':
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)