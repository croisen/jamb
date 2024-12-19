# Just Anotha Music Bot

How far can I take my programming knowledge (me from 2020-2024)

Written in python and automatically downloads ffmpeg

## Usage

Use of a virtualenv is highly recommended, then install the dependencies

```bash
# Create the virtualenv
python3 -m venv env
source ./env/bin/activate

# Install the dependencies
pip install -r ./requirements.txt

# Add the bot token and other tokens to config.json and NOT config.default.json
cp config.default.json config.json

# Enjoy
python3 main.py
```
