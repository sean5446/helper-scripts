
import glob
import os
import re
import sys
import zipfile


def get_version(manifest_contents: str, file: str) -> str:
    if 'Implementation-Version' in manifest_contents:
        return manifest_contents.split('Implementation-Version: ')[1].split('\n')[0].replace('\r', '')
    elif re.search("\d+\.\d+\.\d+", file):
        return re.findall("\d+\.\d+\.\d+", file)[0]
    elif re.search("\d+\.\d+", file):
        return re.findall("\d+\.\d+", file)[0]
    else:
        return 'Unknown'


def get_license(input: str, license_type_list) -> str:
    # find first occurance of license
    indexes = [input.find(word) for word in license_type_list]
    idx = min([index for index in indexes if index != -1])
    license = license_type_list[indexes.index(idx)] if idx != -1 else 'Unknown'
    return license


def main():
    dep_home = sys.argv[1]
    dep_info = []

    license_type_list = ['Apache', 'EPL', 'EDL', 'BSD', 'GNU', 'CDDL', ' MIT ']

    for file in glob.glob(f"{dep_home}/*.jar"):
        archive = zipfile.ZipFile(file, 'r')
        version = 'N/A'
        license = 'N/A'

        try:
            manifest_contents = archive.read('META-INF/MANIFEST.MF').decode("utf-8")
            version = get_version(manifest_contents, file)
        except Exception as e:
            pass

        for zipped_file in archive.namelist():
            if 'license' in zipped_file.lower():
                try:
                    license_contents = archive.read(zipped_file).decode("utf-8")
                    license = get_license(license_contents, license_type_list)
                except Exception as e:
                    pass

        archive.close()
        dep_info.append([os.path.basename(file), version, license])

    # print("file name, version, license")
    for row in dep_info:
        print(f"{row[0]}, {row[1]}, {row[2]}")


if __name__ == '__main__':
    main()
