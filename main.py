import os
import re
import requests as requests
import urllib.parse

status_skipped_show_flag: bool = True
status_success_show_flag: bool = True

url: str = "https://sample.com/"
output_dir: str = "sample.com"


def main():
    download_dir(url, output_dir)


def download_dir(url, output_dir):
    # 1. Get the contents of the target file.
    os.makedirs(output_dir, exist_ok=True)
    save_file(url, output_dir + "/curl.txt", type="text/html")

    with open(output_dir + "/curl.txt") as f:
        lines = f.readlines()
        f.close()

    # 2. Get the link in the a tag from the target file.
    file_path = []
    for line in lines:
        if re.search(r'href="(.*?)"', line):
            file_path.append(trance_path(resub_href(line), url))

    for file in file_path:
        # To avoid going back to the hierarchy above the parent directory,
        # compare by the number of characters.
        if file.count('/') < url.count('/'):
            continue
        # Extract file names from paths.
        file_name = re.sub('(.*?)/', '', file)
        # Extracts the directory name when the path ends in /.
        if file[-1] == '/':
            file_name = re.split('/', file)[-2]
        # If the file name has not been extracted by this point, continue.
        if file_name == "":
            continue
        # If the path is a directory, recursion.
        if is_dir(file):
            download_dir(file, output_dir + "/" + file_name)
            continue

        # ========================================================== #
        # Processing not necessary                                   #
        # if you don't care about 'load', 'capacity', and 'time'.    #
        # ========================================================== #

        # If the file name already exists.
        # (URL encoding already supported)
        if os.path.exists(output_dir + "/" + urllib.parse.unquote(file_name)):
            if status_skipped_show_flag:
                download_status(path=output_dir + "/" + file_name, message="file exist")
        else:
            # Resized wordpress image files are not included.
            if re.search('(.*?)x([0-9].*?)\.(.*?)', file_name) is None:
                # The extension 'webp' is not applicable.
                if re.search('webp', file_name) is None:
                    # output flags.
                    if status_success_show_flag:
                        download_status(status="success", path=output_dir + "/" + file_name, message="success to get")
                    save_file(file, output_dir + "/" + file_name)
                else:  # webp
                    if status_skipped_show_flag:
                        download_status(path=output_dir + "/" + file_name, message="webp is skipped")
            else:  # resize file
                if status_skipped_show_flag:
                    download_status(path=output_dir + "/" + file_name,
                                    message="resize file of (.*?)x([0-9].*?)\.(.*?) is skipped")


def is_dir(file_path: str):
    """
    :param file_path: str
    :return :bool
    """
    if file_path[-1] == '/':
        return True
    else:
        return False


def resub_href(txt: str):
    """
    e.g.
        input:  <a href="https://example.jp/pic.jpg">xxx</a>
        output: https://example.jp/pic.jpg
    :param txt:
    :return: str
    """
    ret = re.sub('(.*?)href="', '', txt)
    ret = re.sub('">(.*?)\n', "", ret)
    return ret


def trance_path(path: str, url: str):
    """
    e.g.
        input 1: ./pic.jpg
        input 2: /pic.jpg
        input 3: pic.jpg
        input 4: https://example.jp/pic.jpg
        output : https://example.jp/pic.jpg
    :param path:
    :param url:
    :return: str
    """
    naked_url = get_naked_url(url)
    # ./ relative path
    if './' in path:
        ret = url + re.sub('./', '', path)
    # / absolute path (protocol omitted)
    elif path[0:1] == "/":
        ret = naked_url[:-1] + path
    # http* Absolute path (with protocol)
    elif path[0:4] == "http":
        ret = path
    # When ./ is a relative path without
    else:
        ret = url + path
    return ret


def get_naked_url(url: str):
    """
    e.g.
        input  : https://example.jp
        output : https://example.jp/
    :param url:
    :return: str
    """
    ret = re.search('https://(.*?)/', url)
    if ret == None:
        ret = re.search('https://(.*?)/', url + "/")
    return ret.group(0)


def download_image(url, timeout=10, type='image'):
    """
    :param url: str
    :param timeout: str
    :param type: str
    :return: str response.content
    """
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    if response.status_code != 200:
        e = Exception("HTTP status: " + str(response.status_code))
        print("Download and listing " + url + " ...")
        print(e)
        # raise e

    content_type = response.headers["content-type"]
    if type not in content_type:
        e = Exception("Content-Type: " + content_type)
        print(e)

    return response.content


def save_file(download_link: str, file_name: str, type: str = 'image'):
    """
    :param download_link: str
    :param file_name: str
    :param type: str
    :return: bool
    """
    url_decoded_file_name = urllib.parse.unquote(file_name)
    with open(url_decoded_file_name, 'wb') as saveFile:
        image = download_image(download_link, type=type)
        saveFile.write(image)
    return True


def download_status(status: str = 'skipped', message: str = 'no log', path: str = ''):
    """
    print format download status
    :param status: str
    :param message: str
    :param path: str
    :return: bool
    """
    print('[' + status + '] ' + message + "\t" + path)
    return True


if __name__ == '__main__':
    main()
