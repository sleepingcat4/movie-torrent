import os
import subprocess
import glob

def download_torrent(magnet_link, download_dir='/torrent/download', proxy="http://172.17.0.2:8888"):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    command = [
        'aria2c',
        '--seed-time=0',
        '--file-allocation=none',
        '--dir=' + download_dir,
        '--all-proxy=' + proxy,
        magnet_link
    ]
    
    subprocess.run(command)

    downloaded_files = glob.glob(os.path.join(download_dir, '*'))
    downloaded_files.sort(key=os.path.getctime, reverse=True)
    
    if downloaded_files:
        base_name = "00000"
        index = 0

        while os.path.exists(os.path.join(download_dir, f"{str(index).zfill(5)}")):
            index += 1

        os.rename(downloaded_files[0], os.path.join(download_dir, f"{str(index).zfill(5)}"))
