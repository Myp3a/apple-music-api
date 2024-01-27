# Apple Music API
A library to interact with Apple Music API, both official and reverse-engineered. It allows you to use the catalog, control your library and download music.

[Features](#Features) •
[Installation](#installation) •
[Requirements](#Requirements) •
[Usage](#Usage) •
[TODO](#TODO)

# Features
 - Catalog search
 - Library search
 - Library edits
 - Playlists edits
 - Media downloads

# Installation
You can install the library by using:
```
pip install git+https://github.com/Myp3a/apple-music-api.git
```

# Requirements
You'll need three things to use all features of the library:
 - Apple Developer Token
 - Music User Token
 - Widevine Device File  

### Apple Developer Token
Allows interaction with all public API's. Required.  
You can get it with the instruction [here](https://developer.apple.com/documentation/applemusicapi/generating_developer_tokens).
### Music User Token
Allows interaction with your library. Required for library functions.  
You can get it by following the instruction [here](https://developer.apple.com/documentation/applemusicapi/user_authentication_for_musickit)
### Alternative way
You can get both tokens by intercepting requests to `https://music.apple.com/`.
### Widevine Device File
Required for decryption of songs.  
You'll need an Android device for it. Dump keys using [dumper](https://github.com/Diazole/dumper), and then use [pywidevine](https://github.com/devine-dl/pywidevine) to generate device file using this command:
```
pywidevine create-device -t ANDROID -l 3 -k private_key.pem -c client_id.bin -o .
```

# Usage
Example of searching catalog song information without user token:
```Python
import applemusic
from applemusic.api.catalog import CatalogTypes

DEV_TOKEN = "dev_token_goes_here"

cli = applemusic.ApiClient(DEV_TOKEN, storefront="us")

songs = cli.catalog.search("Ellie Goulding", CatalogTypes.Songs)
print(songs[0].attributes.name)           # Lights
print(songs[0].attributes.artist_name)    # Ellie Goulding
```
Adding library song to playlist
```Python
import applemusic
from applemusic.api.library import LibraryTypes

DEV_TOKEN = "dev_token_goes_here"
USER_TOKEN = "and_user_one_here"

cli = applemusic.ApiClient(DEV_TOKEN, USER_TOKEN)

songs = cli.library.search("Against The Current", LibraryTypes.Songs)
song = songs[0]
playlist = cli.playlist.create_playlist("My new playlist")
cli.playlist.add_to_playlist(playlist, songs)
```
Downloading a song
```Python
import applemusic
from applemusic.api.library import LibraryTypes

DEV_TOKEN = "dev_token_goes_here"
USER_TOKEN = "and_user_one_here"
WIDEVINE_DEVICE = "device.wvd"

cli = applemusic.ApiClient(DEV_TOKEN, USER_TOKEN, widevine_device_file=WIDEVINE_DEVICE)

songs = cli.library.search("TMNV", LibraryTypes.Songs)
song = songs[0]
catalog_song = cli.catalog.get_by_id(song.attributes.play_params.catalog_id)

with open("song.m4a","wb") as outfile:
    outfile.write(cli.playback.get_decrypted_audio(catalog_song))
```

# TODO
 - Make easier bindings for actions
 - Cover more API methods
 - Make docs

> Disclaimer: Apple Music API is an unofficial application and not affiliated with Apple.