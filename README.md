# StressPoint

Load test your personal website or server.

## Installation

Open a terminal and run:

```sh
git clone https://github.com/itwaisi/stresspoint.git
cd stresspoint
```

Start a virtual environment:

```sh
python -m venv .venv

# LINUX / MACOS
source .venv/bin/activate

# WINDOWS
.venv\Scripts\activate
```

Install the required packages:

```sh
pip install -r requirements.txt
```

## Command-Line Options

| Option       | Description                          | Default |
|--------------|--------------------------------------|---------|
| `url`    | URL to test              | `None`  |
| `requests`  | Number of requests to call              | `None` |
| `workers`  | Number of workers to use              | `None` |
| `ip`  | IP of server running test              | `None` |
| `vpn`  | Must have `ip` set if you want to use a VPN              | `False` |

## Run StressPoint

Open a terminal and run:

```sh
python main.py url=https://example.com requests=1 workers=1 vpn=False
```
