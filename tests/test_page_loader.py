import tempfile
from os import path, listdir
from urllib.parse import urljoin
import pytest
import requests
import pathlib

from page_loader import download

FIXTURES_DIR = 'fixtures'

URL = 'https://example.com'
ERROR_URL = 'https://error-example.com'
RESOURCES = [
    {
        "file_name": "example-com-resources-img.jpg",
        "url": "/resources/img.jpg"
    },
    {
        "file_name": "example-com-resources-index.css",
        "url": "/resources/index.css"
    },
    {
        "file_name": "example-com-resources-index.js",
        "url": "/resources/index.js"
    }
]

html_name = "example-com.html"
file_folder_name = "example-com_files"

map_status_to_route = {
    "500": 'server-error',
    "404": 'not-found',
    "401": 'unauthorized',
    "400": 'bad',
    "403": 'forbidden'
}


def get_path(file_name):
    dir_path = pathlib.Path(__file__).absolute().parent
    return path.join(dir_path, FIXTURES_DIR, file_name)


def read_file(path, mode="r"):
    with open(path, mode) as f:
        result = f.read()
    return result


def read_fixture(file_name, mode="r"):
    return read_file(get_path(file_name), mode)


def test_page_loader(requests_mock):
    """Check that page loader is working correctly."""
    html = read_fixture("initial.html")
    requests_mock.get(URL, text=html)

    for resource in RESOURCES:
        file_name, url = resource.values()
        resource_content = read_fixture(
            path.join('resources', file_name), "rb"
        )
        requests_mock.get(urljoin(URL, url), content=resource_content)

    with tempfile.TemporaryDirectory() as output:
        html_path = path.join(output, html_name)
        file_folder_path = path.join(output, file_folder_name)
        output_path = download(URL, output)
        html_content = read_file(html_path)
        expected_html_content = read_fixture('expected_initial.html')

        assert output_path == html_path
        assert html_content == expected_html_content
        assert len(listdir(file_folder_path)) == len(RESOURCES)

        for resource in RESOURCES:
            file_name = resource["file_name"]
            resource_path = path.join(file_folder_path, file_name)
            fixture_resource_path = path.join('resources', file_name)
            resource_content = read_file(resource_path, "rb")
            expected_resource_content = read_fixture(
                fixture_resource_path, "rb"
            )
            assert resource_content == expected_resource_content


def test_file_system_error(requests_mock):
    """Check that page loader throws correct file system errors."""
    requests_mock.get(URL)

    with pytest.raises(PermissionError):
        assert download(URL, '/sys')

    with pytest.raises(FileNotFoundError):
        assert download(URL, get_path('notExitingFolder'))

    with pytest.raises(NotADirectoryError):
        assert download(URL, get_path('initial.html'))


@pytest.mark.parametrize('status', map_status_to_route.keys())
def test_http_errors(requests_mock, status):
    """Check that page loader returns correct http statuses."""
    route = map_status_to_route[status]
    url = urljoin(URL, route)
    requests_mock.get(url, status_code=int(status))

    with tempfile.TemporaryDirectory() as output:
        with pytest.raises(requests.exceptions.HTTPError):
            download(url, output)
