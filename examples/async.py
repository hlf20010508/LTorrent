import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import asyncio
from ltorrent_async.client import Client
from ltorrent_async.storage import StorageBase
from ltorrent_async.log import Logger

class MyLogger(Logger):
    def __init__(self):
        Logger.__init__(self)
    
    async def WARNING(self, *args):
        pass

class MyStorage(StorageBase):
    def __init__(self):
        StorageBase.__init__(self)

    async def write(self, file_piece_list, data):
        for file_piece in file_piece_list:
            path_file = os.path.join('downloads', file_piece["path"].split('/')[-1])
            file_offset = file_piece["fileOffset"]
            piece_offset = file_piece["pieceOffset"]
            length = file_piece["length"]

            try:
                f = open(path_file, 'r+b')
            except IOError:
                f = open(path_file, 'wb')
            except:
                print("Can't write to file")
                return

            f.seek(file_offset)
            f.write(data[piece_offset:piece_offset + length])
            f.close()

    async def read(self, files, block_offset, block_length):
        file_data_list = []
        for file in files:
            path_file = file["path"]
            file_offset = file["fileOffset"]
            piece_offset = file["pieceOffset"]
            length = file["length"]

            try:
                f = open(path_file, 'rb')
            except:
                print("Can't read file %s" % path_file)
                return
            f.seek(file_offset)
            data = f.read(length)
            file_data_list.append((piece_offset, data))
            f.close()
        file_data_list.sort(key=lambda x: x[0])
        piece = b''.join([data for _, data in file_data_list])
        return piece[block_offset : block_offset + block_length]

async def main():
    magnet_link = "magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c&dn=Big+Buck+Bunny&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fbig-buck-bunny.torrent"
    port = 8080
    logger = MyLogger()
    storage = MyStorage()

    client = Client(
        port=port,
        stdout=logger,
        storage=storage
    )

    await client.load(magnet_link=magnet_link)
    await client.list_file()
    selection = input("Select file: ")
    await client.select_file(selection=selection)
    await client.run()


if __name__ == '__main__':
    asyncio.run(main())
