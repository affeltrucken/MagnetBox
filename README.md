### Credits

Thanks to sidward35 for the code to get the watchlist from Letterboxd.

Taken from [this](https://github.com/sidward35/letterboxd-justwatch) project.

# MagnetBox
Automatically find and download torrents through a Letterboxd users watchlist using 1337x and qBittorrent, in Python.

The code is not great and it's not meant to be easily extendable. Just a quick hacky codebase to make it more convenient for me to download stuff to my media server.

### Requirements
* qBitTorrent
* Python 3.13.1

### Python Requirements
* py1337x
* qbittorrent-api
* colorama
* beautifulsoup4

### Install

1. Clone repository and enter folder:
```bash
git clone https://github.com/affeltrucken/MagnetBox; cd MagnetBox
```

3. Install requirements:
```bash
pip install -r requirements.txt
```
   
4. Make sure you enable Web-UI in qBitTorrent to allow automatic downloads:
* Open qBitTorrent
* Tools
* Options
* Web UI
* [X] Web User Interface (Remote control)
* Change Password (if needed)

5. Edit configuration in magnetbox.py:

   Change the default Letterboxd username, save location, and qBitTorrent credentials as needed.
```python
### CONFIGURATION ###
LETTERBOXD_USERNAME = "aldinsmajlovic"
MAX_TORRENT_SIZE_GB = 15.0

QBITTORRENT_HOST = "localhost"
QBITTORRENT_PORT = 8080
QBITTORRENT_USERNAME = "admin"
QBITTORRENT_PASSWORD = "password"
AUTHENTICATION_REQUIRED = False
TORRENT_CATEGORY_NAME = "MagnetBox"

TORRENT_SAVE_PATH = "D:/PLEX/MOVIES"
MAGNET_FILE = "saved_magnets.txt"
ALLOW_DUPLICATE_MAGNETS = False  # Set to True to add even if already saved
### END CONFIGURATION ###
```
4. Run script:
```bash
python magnetbox.py
```

Script should then get your watchlist, find the best torrent for each movie, and download them through qBitTorrent to the earlier specified save location.

