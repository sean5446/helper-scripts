# requirements.txt: pysmb

# Drive the type inside Drive.compare_to_drive 
from __future__ import annotations

import sys
import time
import os
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor

from typing import Callable, Optional
from abc import ABC, abstractmethod

from smb.smb_structs import OperationFailure
from smb.SMBConnection import SMBConnection
# https://pysmb.readthedocs.io/en/latest/api/smb_SMBConnection.html


class Drive(ABC):
    contents: set[str]
    base_path: str
    conn: SMBConnection

    @abstractmethod
    def scan(self, path: str) -> set[str]:
        pass

    @abstractmethod
    def clean(self, path: str, filter: set[str], dry_run=True) -> None:
        pass

    def end_with_slash(self, path: str) -> str:
        return path if path.endswith("/") else path + "/"

    def user_confirm_delete(self, path: str, filter: set[str]) -> bool:
        prompt = f"Anything that's not: '{filter}'\nwill be deleted from '{path}'\nYou sure bro? (Y/[N]): "
        user_input = input(prompt)
        return user_input == "Y"

    def _separate_share_and_path(self, full_path: str) -> tuple[str, str]:
        share = full_path.split("/")[0]
        rest_of_path = "/" + "/".join(full_path.split("/")[1:])
        return share, rest_of_path
    
    def compare_to_drive(self, other: Drive, path: str = '') -> tuple[set[str], set[str]]:
        if len(self.contents) == 0:
            self.scan(path)
        if len(other.contents) == 0:
            other.scan(path)
        if len(self.contents) == 0 or len(other.contents) == 0:
            raise ValueError("Both drives must have contents scanned before comparison")
        if self.base_path is None or other.base_path is None or self.base_path != other.base_path:
            raise ValueError(f"Both drives must have same the same base path {self.base_path} {other.base_path}")

        unique_to_other = other.contents - self.contents
        unique_to_self = self.contents - other.contents
        return unique_to_self, unique_to_other
    
    def copy(self, src_drive: Drive, src_path: str, dest_drive: Drive, dest_path: str) -> None:
        # LOCAL to SMB
        if isinstance(src_drive, Local) and isinstance(dest_drive, SMB):
            local_path = os.path.join(src_drive.root, src_path)
            share, share_path = self._separate_share_and_path(dest_path)
            if share_path.endswith("/"):
                self.conn.createDirectory(share, share_path)
            else:
                with open(local_path, 'rb') as f:
                    self.conn.storeFile(share, share_path, f)
        # SMB to LOCAL
        elif isinstance(src_drive, SMB) and isinstance(dest_drive, Local):
            local_path = os.path.join(dest_drive.root, dest_path)
            share, share_path = self._separate_share_and_path(src_path)
            if share_path.endswith("/"):
                os.makedirs(local_path, exist_ok=True)
            else:
                try:
                    with open(local_path, 'wb') as f:
                        self.conn.retrieveFile(share, os.path.join(share, share_path), f)
                except OperationFailure:
                    os.remove(local_path)
        # LOCAL to LOCAL
        elif isinstance(src_drive, Local) and isinstance(dest_drive, Local):
            shutil.copy(os.path.join(src_drive.root, src_path), os.path.join(dest_drive.root, dest_path))


class Local(Drive):

    def __init__(self, root: str, friendly_name: str = "Local") -> None:
        self.root = root
        self.friendly_name = friendly_name
        self.contents = set()

    def _fmt_path(self, path: str) -> str:
        path = path.replace("\\", "/").replace(self.root, "") # convert windows slashes and remote root
        return path if not path.startswith("/") else path[1:] # trim os.path.join leading slash on unix
    
    def _separate_share_and_path(self):
        pass

    def scan(self, path: str) -> set[str]:
        self.contents = set()
        self.base_path = path
        path = self.end_with_slash(self.root) + path
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                logging.debug(self._fmt_path(os.path.join(root, name)))
                self.contents.add(self._fmt_path(os.path.join(root, name)))
            for name in dirs:
                # match SMB style - now all directories will end in "/"
                logging.debug(self._fmt_path(os.path.join(root, name)) + "/")
                self.contents.add(self._fmt_path(os.path.join(root, name)) + "/")
        return self.contents
    
    def clean(self, path: str, filter: set[str], dry_run=True) -> None:
        if not dry_run and not self.user_confirm_delete(path, filter):
            return
        path = self.root + path
        for root, _, files in os.walk(path, topdown=False):
            for name in files:
                if not name.lower().endswith(tuple(filter)):
                    if dry_run:
                        print(os.path.join(root, name))
                    else:
                        os.remove(os.path.join(root, name))
    
    def __str__(self) -> str:
        return f"{self.friendly_name} {self.root}"


class SMB(Drive):

    def __init__(self, username: str, password: str, remote_host: str, friendly_name: str = 'SMB') -> None:
        self.conn = SMBConnection(username, password, 'my_name', 'remote_name')
        assert self.conn.connect(remote_host, timeout=3)
        self.remote_host = remote_host
        self.friendly_name = friendly_name if friendly_name else f"SMB {remote_host}"
        self.contents = set()

    def _recursive_list(self, share: str, path: str, contents: set[str], func: Callable[[str], None] | None) -> set[str]:
        for x in self.conn.listPath(share, path):
            if x.isDirectory:
                next = path + x.filename + "/"
                if x.filename not in (".", ".."):
                    logging.debug(share + next)
                    self.contents.add(share + next)
                    self._recursive_list(share, next, contents, func)
            else:
                logging.debug(share + path + x.filename)
                if func is not None:
                    func(share + path + x.filename)
                else:
                    self.contents.add(share + path + x.filename)
        return self.contents

    def scan(self, path: str = "/", func: Callable[[str], None] | None = None) -> set[str]:
        self.contents = set()
        self.base_path = path
        if path == "/":
            for x in self.conn.listShares():
                if x.name != "IPC$":
                    self._recursive_list(x.name, "/", self.contents, func)
        else:
            share, rest_of_path = self._separate_share_and_path(path)
            self._recursive_list(share, self.end_with_slash(rest_of_path), self.contents, func)
        return self.contents
    
    # TODO clean calls scan which makes a set, which isn't needed for clean
    def clean(self, path: str, filter: set[str], dry_run=True) -> None:
        if not dry_run and not self.user_confirm_delete(path, filter):
            return
        def delete_func(path: str) -> None:
            if not path.lower().endswith(tuple(filter)):
                share, rest_of_path = self._separate_share_and_path(path)
                if dry_run:
                    print(f"{share}{rest_of_path}")
                if not dry_run:
                    self.conn.deleteFiles(share, rest_of_path)
        self.scan(path, delete_func)

    def __str__(self) -> str:
        return f"SMB {self.remote_host}"


if __name__ == "__main__":
    start_time = time.time()

    username = os.getenv("SMB_USER", "username")
    password = os.getenv("SMB_PASS", "password")
    remote_smb_ip = os.getenv("SMB_IP", "192.168.50.1")
    debug = os.getenv("SMB_DEBUG", False)
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    compare_path = None

    if len(sys.argv) > 1:
        compare_path = sys.argv[1]

    if len(sys.argv) > 4:
        username = sys.argv[2]
        password = sys.argv[3]
        remote_smb_ip = sys.argv[4]

    if not compare_path or not username or not password or not remote_smb_ip:
        print("Usage: smb_sync.py <path> (with SMB_USER, SMB_PASS, SMB_IP environment variables set)")
        sys.exit(1)

    remote = SMB(username, password, remote_smb_ip)
    local = Local("/mnt/m")
    usb = Local("/mnt/d", "USB")

    # remove junk (txt, jpg, Thumbs.db, html etc.) - super dangerous on the wrong folder
    #usb.clean(compare_path, {".srt", ".mp4", ".avi", ".mkv", ".m4v", ".divx", ".mpg"})

    # find differences drives 1:1 
    with ThreadPoolExecutor(max_workers=2) as executor:
        usb_future = executor.submit(local.compare_to_drive, usb, compare_path)
        remote_future = executor.submit(local.compare_to_drive, remote, compare_path)
        local_not_usb, usb_not_local = usb_future.result()
        local_not_remote, remote_not_local = remote_future.result()

    print(f"{local.friendly_name} contents size {len(local.contents)}")
    print(f"{usb.friendly_name} contents size {len(usb.contents)}")
    print(f"{remote.friendly_name} contents size {len(remote.contents)}")

    for x in local_not_usb:
        print(f"Local not usb: {x}")

    for x in usb_not_local:
        print(f"USB not local: {x}")

    for x in local_not_remote:
        print(f"Local not remote: {x}")
    
    for x in remote_not_local:
        print(f"Remote not local: {x}")

    # TODO automatically try to align drives
    # should probably add md5 and last modified time for comparisons too
    # ideally try to find if a file was moved rather than delete/copy

    # remote.copy(remote, "Video/remote.txt", local, "Video/remote.txt")
    # remote.copy(local, "Video/local.txt", remote, "Video/local.txt")

    stop_time = time.time()
    print(f"Time taken: {(stop_time - start_time):.2f} seconds")
