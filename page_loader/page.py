from os import path, mkdir, getcwd
from urllib.parse import urlparse, urljoin
import logging
import requests

from progress.bar import Bar
from bs4 import BeautifulSoup
from page_loader.utils import build_name


logging.basicConfig(level=logging.INFO)


def write_to_file(content, file_path, mode="w"):
    with open(file_path, mode) as file:
        file.write(content)


def create_folder(folder_path):
    if not path.exists(folder_path):
        mkdir(folder_path)


map_tag_to_attr = {
    "link": "href",
    "script": "src",
    "img": "src"
}


def prepare_resources(html, url, folder_path):
    soup = BeautifulSoup(html, 'html.parser')
    tags = []
    for tag in map_tag_to_attr.keys():
        tags.extend(soup.find_all(tag))

    links = []
    for tag in tags:
        attr = map_tag_to_attr[tag.name]
        link = tag.get(attr)

        if not link:
            continue

        full_url = urljoin(f"{url}/", link)

        if urlparse(full_url).netloc != urlparse(url).netloc:
            continue

        file_name = build_name(full_url)
        file_path = path.join(folder_path, file_name)
        tag[attr] = file_path
        links.append({
            "link": full_url,
            "file_path": file_path
        })
    return links, soup.prettify(formatter="html5")


def save_resource(resource, output):
    link, file_path = resource.values()

    with open(path.join(output, file_path), "wb") as file:
        response = requests.get(link, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        number_of_blocks = total_size_in_bytes / block_size + 1
        with Bar(f"Downloading {file_path}", max=number_of_blocks) as bar:
            for data in response.iter_content(block_size):
                file.write(data)
                bar.next()


def download(url, output=getcwd()):
    html_name = build_name(url)
    html_path = path.join(output, html_name)
    file_folder_name = build_name(url, is_folder=True)
    file_folder_path = path.join(output, file_folder_name)

    logging.info(f"Downloading html from {url}")
    response = requests.get(url)
    response.raise_for_status()

    logging.info(f"Creating {file_folder_path} folder for files")
    create_folder(file_folder_path)

    logging.info("Preparing resources")
    resources, html = prepare_resources(response.text, url, file_folder_name)

    for resource in resources:
        save_resource(resource, output)

    logging.info(f"Saving html to {html_path}")
    write_to_file(html, html_path)
    return html_path
