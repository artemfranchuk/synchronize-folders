import argparse
import logging
import os
import shutil
import time

def sync_folders(src, replica):
    for folder, subfolders, filenames in os.walk(src):
        replica_folder = folder.replace(src, replica)
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)
            logging.info(f"Created folder: {replica_folder}")

        for filename in filenames:
            src_file = os.path.join(folder, filename)
            replica_file = os.path.join(replica_folder, filename)

            if not os.path.exists(replica_file) or os.path.getmtime(src_file) > os.path.getmtime(replica_file):
                shutil.copy2(src_file, replica_file)
                logging.info(f"Copied file: {src_file} to {replica_file}")

    for folder, subfolders, filenames in os.walk(replica):
        src_folder = folder.replace(replica, src)
        if not os.path.exists(src_folder):
            shutil.rmtree(folder)
            logging.info(f"Removed folder: {folder}")

        for filename in filenames:
            src_file = os.path.join(src_folder, filename)
            replica_file = os.path.join(folder, filename)

            if not os.path.exists(src_file):
                os.remove(replica_file)
                logging.info(f"Removed file: {replica_file}")

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("src", help="Source folder")
    parser.add_argument("replica", help="Replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("--log", default="sync.log", help="Log file path")

    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(console)

    while True:
        sync_folders(args.src, args.replica)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
