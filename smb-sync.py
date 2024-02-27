# Drive the type inside Drive.compare_to_drive 
from __future__ import annotations

import time
import os
import shutil

from typing import Callable
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

    def user_confirm_delete(self) -> bool:
        user_input = input("About to delete stuff. You sure bro? (y/n): ")
        return user_input.lower() == "y"

    def _separate_share_and_path(self, full_path: str) -> tuple[str, str]:
        share = full_path.split("/")[0]
        rest_of_path = "/" + "/".join(full_path.split("/")[1:])
        return share, rest_of_path
    
    def compare_to_drive(self, other: Drive) -> tuple[set[str], set[str]]:
        if self.contents is None or other.contents is None:
            raise ValueError("Both drives must be scanned before comparing")
        if self.base_path is None or other.base_path is None or self.base_path != other.base_path:
            raise ValueError(f"Both drives must have same the same base path {self.base_path} {other.base_path}")
        unique_to_self = self.contents - other.contents
        unique_to_other = other.contents - self.contents
        return unique_to_self, unique_to_other
    
    def copy(self, src_drive: Drive, src_path: str, dest_drive: Drive, dest_path: str) -> None:
        # TODO what if it's a directory?
        # LOCAL to SMB
        if isinstance(src_drive, Local) and isinstance(dest_drive, SMB):
            local_path = os.path.join(src_drive.root, src_path)
            share, share_path = self._separate_share_and_path(dest_path)
            with open(local_path, 'rb') as f:
               self.conn.storeFile(share, share_path, f)
        # SMB to LOCAL
        elif isinstance(src_drive, SMB) and isinstance(dest_drive, Local):
            local_path = os.path.join(dest_drive.root, dest_path)
            share, share_path = self._separate_share_and_path(src_path)
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

    def _fmt_path(self, path: str) -> str:
        path = path.replace("\\", "/").replace(self.root, "") # trim windows slash and root
        return path if not path.startswith("/") else path[1:] # trim os.path.join leading slash on unix
    
    def _separate_share_and_path(self):
        pass

    def scan(self, path: str) -> set[str]:
        self.contents = set()
        self.base_path = path
        path = self.end_with_slash(self.root) + path
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                # print(self._fmt_path(os.path.join(root, name)))
                self.contents.add(self._fmt_path(os.path.join(root, name)))
            for name in dirs:
                # match SMB style - now all directories will end in "/"
                # print(self._fmt_path(os.path.join(root, name)) + "/")
                self.contents.add(self._fmt_path(os.path.join(root, name)) + "/")
        return self.contents
    
    def clean(self, path: str, filter: set[str], dry_run=True) -> None:
        if not dry_run and not self.user_confirm_delete():
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

    def __init__(self, username: str, password: str, remote_host: str) -> None:
        self.conn = SMBConnection(username, password, 'my_name', 'remote_name')
        assert self.conn.connect(remote_host, timeout=3)
        self.remote_host = remote_host

    def _recursive_list(self, share: str, path: str, contents: set[str], func: Callable[[str], None] | None) -> set[str]:
        for x in self.conn.listPath(share, path):
            if x.isDirectory:
                next = path + x.filename + "/"
                if x.filename not in (".", ".."):
                    # print(share + next)
                    self.contents.add(share + next)
                    self._recursive_list(share, next, contents, func)
            else:
                # print(share + path + x.filename)
                if func is not None:
                    func(share + path + x.filename)
                else:
                    self.contents.add(share + path + x.filename)
        return self.contents

    def scan(self, path: str = "/", func: Callable[[str], None] = None) -> set[str]:
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
        if not dry_run and not self.user_confirm_delete():
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
    compare_path = "Video"
    remote = SMB(os.getenv("username", ""), "", "192.168.50.1")
    local = Local("M:/")
    usb = Local("H:/", "USB")

    # remove junk (txt, jpg, Thumbs.db, html etc.) - super dangerous on the wrong folder
    video_safe_list = {".srt", ".mp4", ".avi", ".mkv", ".m4v", ".divx", ".mpg"}
    for drive in (remote, local, usb):
        drive.clean(compare_path, video_safe_list, dry_run=True)
    print()

    # scan drives
    for drive in (remote, local, usb):
        drive.scan(compare_path)
        print(drive)
        print(len(drive.contents))
    print()

    # find differences in drives - can only compare 1:1 currently
    unqiue_to_remote, _ = remote.compare_to_drive(local)
    _, unique_to_usb = local.compare_to_drive(usb)

    for x in unqiue_to_remote:
        print(f"Remote: {x}")

    for x in unique_to_usb:
        print(f"USB: {x}")

    # TODO align drives
    # maybe the file was moved? maybe check if os.path.basename(x) exist in both unique sets
    # remote.copy(remote, "Video/remote.txt", local, "Video/remote.txt")
    # remote.copy(local, "Video/local.txt", remote, "Video/local.txt")

    stop_time = time.time()
    print(f"Time taken: {(stop_time - start_time):.2f} seconds")

