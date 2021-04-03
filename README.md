# Code Challenge
This is an reverse proxy used to intercept requests and validate wether they are malicious or duplicated.

## Installation

Clone the repository

```bash
git clone https://github.com/carlos2606/code_challenge.git
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the requirements.

```bash
pip install -r requirements.txt
```

## Usage

Create a .env file in the root of the project with the variables in .env-template file. These environment variables will be loaded with the library dotenv.

Run the API server with the following command:

```bash
python main.py
```

## Docs
FastAPI has OpenAPI integrated to all its projecs. Then all you need is go to the url "localhost:<port>/docs" to see more information about the endpoints

## License
[MIT](https://choosealicense.com/licenses/mit/)