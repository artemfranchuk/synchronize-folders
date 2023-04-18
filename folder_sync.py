import argparse
import logging
import os
import shutil
import time

def sync_folders(src, replica):
    # Walk through each folder, subfolder, and file in the source folder
    for folder, subfolders, filenames in os.walk(src):
        # Replace the source folder path with the replica folder path
        replica_folder = folder.replace(src, replica)

        # If the replica folder doesn't exist, create it
        if not os.path.exists(replica_folder):
            os.makedirs(replica_folder)
            logging.info(f"Created folder: {replica_folder}")

        # Go through each file in the source folder
        for filename in filenames:
            # Create the full path for the source and replica files
            src_file = os.path.join(folder, filename)
            replica_file = os.path.join(replica_folder, filename)

            # If the replica file doesn't exist or is older than the source file, copy the source file to the replica folder
            if not os.path.exists(replica_file) or os.path.getmtime(src_file) > os.path.getmtime(replica_file):
                shutil.copy2(src_file, replica_file)
                logging.info(f"Copied file: {src_file} to {replica_file}")

    # Walk through each folder, subfolder, and file in the replica folder
    for folder, subfolders, filenames in os.walk(replica):
        # Replace the replica folder path with the source folder path
        src_folder = folder.replace(replica, src)

        # If the source folder doesn't exist, remove the replica folder
        if not os.path.exists(src_folder):
            shutil.rmtree(folder)
            logging.info(f"Removed folder: {folder}")

        # Go through each file in the replica folder
        for filename in filenames:
            # Create the full path for the source and replica files
            src_file = os.path.join(src_folder, filename)
            replica_file = os.path.join(folder, filename)

            # If the source file doesn't exist, remove the replica file
            if not os.path.exists(src_file):
                os.remove(replica_file)
                logging.info(f"Removed file: {replica_file}")

def main():
    # Create an argument parser to get command-line arguments
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("src", help="Source folder")
    parser.add_argument("replica", help="Replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("--log", default="sync.log", help="Log file path")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Configure the logging
    logging.basicConfig(filename=args.log, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(console)

    # Loop forever
    while True:
        # Synchronize the source and replica folders
        sync_folders(args.src, args.replica)

        # Sleep for the specified interval in seconds
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
