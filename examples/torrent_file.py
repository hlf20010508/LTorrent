import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ltorrent.client import Client

if __name__ == '__main__':
    torrent_path = "examples/example.torrent"
    port = 8080
    timeout = 1

    client = Client(
        port=port,
        torrent_path=torrent_path,
        timeout=timeout,
    )
    client.start()
