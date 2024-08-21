News Cast with NewsAPI
======================

A web application to fetch and display news articles using websockets.

Installation
============

Clone the repository and install the required libraries::

    $ git clone https://github.com/iamoliverden/aiohttp_news_app.git

Install the app (from the project folder)::

    $ pip install -e .

Run the application::

    $ cd chat
    $ python main.py

Open your browser and navigate to::

    http://127.0.0.1:8080

Requirements
============
* aiohttp_
* aiohttp_jinja2_
* Faker_
* asyncio_

.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _aiohttp_jinja2: https://github.com/aio-libs/aiohttp_jinja2
.. _Faker: https://github.com/joke2k/faker
.. _asyncio: https://docs.python.org/3/library/asyncio.html

Project Files
=============
* `index.html` - The HTML template for the web interface.
* `main.py` - The main application file to run the server.
* `views.py` - Contains the logic for fetching news and handling websockets.

Usage
=====
1. **Connect**: Click the "Connect" button to establish a websocket connection.
2. **Status**: The connection status will be displayed.
3. **Log**: The log will display messages and news articles fetched periodically.

Acknowledgment
==============
This project was inspired by and includes some code from the aiohttp demos repository: `https://github.com/aio-libs/aiohttp-demos.git`
