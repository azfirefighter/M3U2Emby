import os
import ConfigParser

__author__ = "Tilman Griesel"
__copyright__ = "Copyright 2015, rocketengine.io"
__license__ = "MIT"
__maintainer__ = "Tilman Griesel"
__email__ = "griesel@rocketengine.io"

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

##############################
# CONFIG
##############################
SOURCE_DIR = config.get("dir", "source")
TARGET_DIR = config.get("dir", "target")
CAN_EDIT = config.getboolean("users", "edit")
USERS = str(config.get("users", "users")).split(";")

print "Source: " + SOURCE_DIR
print "Target: " + TARGET_DIR
print "Can Edit: " + str(CAN_EDIT)
print "Users: " + str(USERS)

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
            if os.path.isfile(entry_path):
                result.append(entry_path)
            else:
                print "Invalid playlist item found. File does not exists. Path: " + entry_path

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

    dir_name = os.path.join(TARGET_DIR, title + ' [playlist]')

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    out = open(os.path.join(dir_name, 'playlist.xml'), "w")
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