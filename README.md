# Review Recommender

A tool that helps find reviewer for a pull request.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install review-recommender
```
## Usage

```bash
usage: review_recommender [-h] owner repo num token

Given pull request, rank revisors

positional arguments:
  owner       the owner of the repository
  repo        the name of the repository
  num         the number of the pull request
  token       the github access token

optional arguments:
  -h, --help  show this help message and exit
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)