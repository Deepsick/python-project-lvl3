### Hexlet tests and linter status:
[![Actions Status](https://github.com/Deepsick/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/Deepsick/python-project-lvl3/actions)
[![Node CI](https://github.com/Deepsick/backend-project-lvl3/workflows/Node%20CI/badge.svg)](https://github.com/Deepsick/backend-project-lvl3/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/9fb96d399ada0c5a68e9/maintainability)](https://codeclimate.com/github/Deepsick/python-project-lvl3/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9fb96d399ada0c5a68e9/test_coverage)](https://codeclimate.com/github/Deepsick/python-project-lvl3/test_coverage)

# Page-loader

Make request to url, download page and its resources


## Installation

Python packaging and dependency management tool ```poetry``` should be preinstalled.

```bash
make build
make package-install
```


## Usage

```bash
usage: page_loader [-h] [-o OUTPUT] url

Downloads html page with all its resources

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output folder path
```

### Downloading a page

[![asciicast](https://asciinema.org/a/1OgLWeQkK2nHrS9Im3bwbOAQV.svg)](https://asciinema.org/a/1OgLWeQkK2nHrS9Im3bwbOAQV)

### Logging

[![asciicast](https://asciinema.org/a/SqNkrcHPWUTteobZlascf0wgp.svg)](https://asciinema.org/a/SqNkrcHPWUTteobZlascf0wgp)

## Testing

```bash
make install
make lint
make test
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

[MIT](https://choosealicense.com/licenses/mit/)