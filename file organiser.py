# simple Downloads File content organiser
from pathlib import Path
import os, shutil

# recognize the Paths
downloads_path = str(Path.home() / 'Downloads')
pictures_path = str(Path.home() / 'Pictures')
music_path = str(Path.home() / 'Music')
videos_path = str(Path.home() / 'Videos')
documents_path = str(Path.home() / 'Documents')

# declare file extensions
music_ext = ('.mp3', '.wma', '.mid', '.m4a', '.ogg', '.flac', '.wav', '.amr')
videos_ext = ('.avi', '.mp4', '.m4v', '.mkv', '.mov', '.wmv', '.mpg', '.flv')
documents_ext = ('.pdf', '.doc', '.docx', '.docm', '.dot', '.dotm', '.dotx', '.html', '.txt', '.xps', 
'.csv', '.xls', '.xlsb', '.xlsm', '.xltx', '.xps', '.xml')
pictures_ext = ('.jpg', '.jpg', '.gif', '.png','.jpx', '.bmp', '.ico')


# files to move
music = []
videos = []
documents = []
pictures = []

files = os.listdir(downloads_path)
# check for extensions
for file in files:
    ext = os.path.splitext(file)[-1]
    if ext in music_ext:
        music.append(file)
    elif ext in videos_ext:
        videos.append(file)
    elif ext in documents_ext:
        documents.append(file)
    elif ext in pictures_ext:
        pictures.append(file)

# move files to the new directory
for item in files:
    if item in music:
        dir = downloads_path + '\\' + item
        shutil.move(dir, music_path)
    elif item in videos:
        dir = downloads_path + '\\' + item
        shutil.move(dir, videos_path)
    elif item in documents:
        dir = downloads_path + '\\' + item
        shutil.move(dir, documents_path)
    elif item in pictures:
        dir = downloads_path + '\\' + item
        shutil.move(dir, pictures_path)
