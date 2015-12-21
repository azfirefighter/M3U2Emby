import os

__author__ = "Tilman Griesel"
__copyright__ = "Copyright 2015, rocketengine.io"
__license__ = "MIT"
__maintainer__ = "Tilman Griesel"
__email__ = "griesel@rocketengine.io"

##############################
# CONFIG
##############################
SOURCE_DIR = "C:\\dev\\ws\\private\\M3U2Emby\\testdata"
TARGET_DIR = "C:\\dev\\ws\\private\\M3U2Emby\\out"
CAN_EDIT = False
USERS = ['f102fb850ada4661a6c5698c6c3c8f09',
         '95c10e6117da4429a728f35b81ace850']
##############################

def locate_m3u():
    result = []
    for subdir, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if os.path.splitext(file)[1] == ".m3u":
                result.append(os.path.join(subdir, file))
    return result

def read_m3u_playlist(path):
    ret = {}
    result = []
    head, tail = os.path.split(path)
    print path
    data = open(path).readlines()
    for entry in data:
        # Ignore EXTM3U
        if entry[0] != "#":
            # Create Path
            entry_path = os.path.join(head, entry.rstrip())
            result.append(entry_path)

    ret['title'] = tail.replace('.m3u', '')
    ret['data'] = result

    return ret

def write_emby_playlist(playlist):
    '''
    Don't use XML libs
    to keep the deps low.
    :return:
    '''
    title = playlist['title']
    data = playlist['data']

    xml = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n'
    xml += '\t<Item>\n'
    xml += '\t\t<PlaylistMediaType>Audio</PlaylistMediaType>\n'
    xml += '\t\t<Added>00/00/00 0:00:00 AM</Added>\n' # TODO: Set time
    xml += '\t\t<LockData>false</LockData>\n'
    xml += '\t\t<LocalTitle>' + title + '</LocalTitle>\n'

    xml += '\t\t<PlaylistItems>\n'
    for entry in data:
        xml += '\t\t\t<PlaylistItem>'
        xml += '<Path>' + entry + '</Path>'
        xml += '</PlaylistItem>\n'
    xml += '\t\t</PlaylistItems>\n'

    xml += '\t\t<Shares>\n'
    for user in USERS:
        xml += '\t\t\t<Share>\n'
        xml += '\t\t\t\t<UserId>' + user + '</UserId>\n'
        xml += '\t\t\t\t<CanEdit>' + str(CAN_EDIT).lower() + '</CanEdit>\n'
        xml += '\t\t\t</Share>\n'
    xml += '\t\t</Shares>\n'
    xml += '\t</Item>\n'

    file_name = title + ' [playlist]'
    out = open(os.path.join(TARGET_DIR, file_name), "w")
    out.write(xml)
    out.close()

def main():
    '''
    Read M3U playlists and convert them to
    a emby xml playlist.
    :return:
    '''
    for pl_path in locate_m3u():
        write_emby_playlist(read_m3u_playlist(pl_path))

main()
exit(0)