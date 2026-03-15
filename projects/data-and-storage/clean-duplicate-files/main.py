"""
Traverse through root_folder and detect duplicated files by content hash. 

Ideas:
    - Find out duplicate of specific file. (Special user case)
    - If all files and folders in a folder are duplicated, the folder is duplicated (Important feature)
"""

import hashlib
import os
import time
from argparse import ArgumentParser
from collections import defaultdict
from dataclasses import dataclass
from functools import w***s


def timer(func):
    """
    Decoratro to debug time consumed in function call
    """

    @w***s(func)
    def w***per(*args):
        start_time = time.time()
        retval = func(*args)
        print(
            f"DEBUG: The {func.__name__} took {time.time() - start_time} Seconds, retval ={str(retval)[:10]}"
        )
        return retval

    return w***per


def get_arguments():
    """
    Reading command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        dest="path",
        help="Root path for traversing",
        required=True,
    )
    # parser.add_argument(
    #     "--age",
    #     type=int,
    #     dest="age",
    #     help="The Age for the user",
    #     required=False,
    # )

    arguments = parser.parse_args()

    return arguments.path


def get_file_size(file_path) -> int | None:
    try:
        stats = os.stat(file_path)
    except Exception:
        return None
    else:
        return stats.st_size


@dataclass
class FileInfo:
    file_name: str
    file_hash: str
    file_path: str
    file_size: int


@timer
def main():
    """
    Main function to show stats for duplicated files
    """
    # Get arguments
    root_folder = get_arguments()

    # Configuration to control behavior
    DEBUG_PARTIALLY_EMPTY = False
    DEBUG_PARTIALLY_DUPLICATED = False
    DEBUG = False
    FAST_MODE_ENABLED = True
    hashes_dict = {}
    empty_files = []
    is_empty_dict = {}
    is_dupli_dict = {}
    skipped_folders = [
        ".npm",
        ".venv",
        ".msf4",
        ".mozilla",
        ".config",
        ".gradle",
        ".docker",
        ".cert",
        ".gphoto",
        ".dotnet",
        ".dbus",
        ".yarn",
        ".rustup",
        ".arbtt",
        ".cache",
        ".dartServer",
        ".zoom",
        ".var",
        ".android",
        ".local",
        ".vscode",
        ".pub-cache",
        ".kivy",
        ".ipython",
        ".openshot_qt",
        ".java",
        ".thunderbird",
        ".audacity-data",
        ".dart",
        ".dart-tool",
        ".gnupg",
        ".anydesk",
        ".cargo",
    ]
    removed_files = []
    stats_dict = defaultdict(int)
    review_those = []

    def all_dirs_are_duplicated(root, dirs):
        for dir in dirs:
            dir_full_path = os.path.join(root, dir)
            if (
                dir_full_path not in is_dupli_dict
                and dir_full_path not in is_empty_dict
            ):
                return False
        return True

    def get_dirs_status(root, dirs):
        res = []
        for dir in dirs:
            dir_full_path = os.path.join(root, dir)
            res.append(
                (
                    dir_full_path,
                    dir_full_path not in is_dupli_dict
                    and dir_full_path not in is_empty_dict,
                )
            )
        return res

    def append_to_dupli_dict(a_path):
        # Delete all paths inside this path.
        keys_to_delete = []
        key: str
        for key, _ in is_dupli_dict.items():
            if key.startswith(a_path):
                keys_to_delete.append(key)
        for k in keys_to_delete:
            del is_dupli_dict[k]
            if k in review_those:
                review_those.remove(k)
            else:
                print(
                    f"something went wrong, {k} should be in review_those, but it is not found"
                )

        is_dupli_dict[a_path] = True

    for root, dirs, files in os.walk(root_folder, topdown=False):
        root_split = root.split("/")

        if len(root_split) > 3 and root_split[3] in skipped_folders:
            if DEBUG:
                print("Skipping folder")
            stats_dict["skipped_folders"] += 1
            continue

        if ".git" in root_split:
            stats_dict["skipped .git"] += 1
            if DEBUG:
                print("Skipping .git")
            continue

        all_files = len(files)
        duplicated_files_counter = 0
        empty_files_counter = 0

        if len(files) == 0 and len(dirs) == 0:
            stats_dict["skipped_empty_folders"] += 1
            if DEBUG:
                print(f"Skipping Empty folder: {root}")
            is_empty_dict[root] = True
            continue

        if len(files) == 0 and len(dirs) != 0:
            stats_dict["skipped_no_files_in_folder"] += 1
            if DEBUG:
                print("skipped_no_files_in_folder")
            if all_dirs_are_duplicated(root, dirs):
                stats_dict["duplicated_folders_due_to_duplicted_folders"] += 1
                review_those.append(root)
                append_to_dupli_dict(root)

            elif DEBUG:
                print("get_dirs_status:", *get_dirs_status(root, dirs), sep="\n")
            continue

        for file_name in files:

            stats_dict["total_files_loop"] += 1
            file_path = os.path.join(root, file_name)
            file_size = get_file_size(file_path)

            try:
                if FAST_MODE_ENABLED:
                    file_hash: str = bytes(str(file_size), encoding="utf-8") + open(
                        file_path, "rb"
                    ).read(15)
                else:
                    file_hash: str = hashlib.md5(
                        open(file_path, "rb").read()
                    ).hexdigest()
            except FileNotFoundError:
                # deleted for some reason
                file_info = FileInfo(
                    file_name, "0000000000000000000000000", file_path, file_size
                )
                removed_files.append(file_info)
                stats_dict["FileNotFoundError"] += 1
                continue
            file_info = FileInfo(file_name, file_hash, file_path, file_size)

            if file_size == 0:
                empty_files.append(file_info)
                empty_files_counter += 1
                stats_dict["empty_files_counter"] += 1
                continue

            if file_hash in hashes_dict:
                stats_dict["duplicated_files_counter"] += 1
                # other_file = hashes_dict[file_hash]
                duplicated_files_counter += 1
                # print(f"Detect duplicate: {file_info} with {other_file}")
                print(".", end="")
            else:
                stats_dict["normal_files"] += 1
                hashes_dict[file_hash] = file_info

        if all_files == duplicated_files_counter:
            print(f"Probably folder {root} is duplicated, files_count = {all_files}.")
            # No directories, and all files are duplciated
            if len(dirs) == 0 or all_dirs_are_duplicated(root, dirs):
                stats_dict["duplicated_folders_due_to_duplicted_files_and_folders"] += 1
                review_those.append(root)
                is_dupli_dict[root] = True
        elif duplicated_files_counter > 0 and DEBUG_PARTIALLY_DUPLICATED:
            print(f"{duplicated_files_counter}/{all_files} Duplicated files in {root}")

        if empty_files_counter > 0:
            if all_files == empty_files_counter and len(dirs) == 0:
                print(
                    f"Folder containing all EMPTY files {root}, {all_files} are empty."
                )
            elif DEBUG_PARTIALLY_EMPTY:
                print(f"{empty_files_counter}/{all_files} empty files in {root}")

    print(f"Done, stats_dict={stats_dict}")
    return review_those


if __name__ == "__main__":
    review_those = main()
    input("Press Enter to show folders to review")
    print(*review_those, sep="\n")
