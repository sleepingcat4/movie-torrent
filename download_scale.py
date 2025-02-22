import os
import subprocess
import glob
import time
import signal

def download_torrents_from_file(txt_file, download_dir='/torrent/download', proxy="http://172.17.0.2:8888", timeout=900):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    with open(txt_file, 'r') as f:
        magnet_links = [line.strip() for line in f if line.strip()]

    for magnet_link in magnet_links:
        command = [
            'aria2c',
            '--seed-time=0',
            '--file-allocation=none',
            '--dir=' + download_dir,
            '--all-proxy=' + proxy,
            magnet_link
        ]

        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)

        start_time = time.time()
        while time.time() - start_time < timeout:
            if process.poll() is not None:
                break
            time.sleep(5)

        if process.poll() is None:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

        downloaded_files = glob.glob(os.path.join(download_dir, '*'))
        downloaded_files.sort(key=os.path.getctime, reverse=True)

        if downloaded_files:
            index = 0
            while os.path.exists(os.path.join(download_dir, f"{str(index).zfill(5)}")):
                index += 1

            os.rename(downloaded_files[0], os.path.join(download_dir, f"{str(index).zfill(5)}"))

download_torrents_from_file('movie.txt')
