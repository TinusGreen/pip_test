> captcha22: Exploiting the imbalance between human readable and computer complex CAPTCHAs

![](https://img.shields.io/github/license/FSecureLABS/captcha_cracking)
![](https://img.shields.io/github/contributors/FSecureLABS/captcha_cracking)

# Overview

**CAPTCHA22** is a [Tensorflow](https://github.com/tensorflow/tensorflow) powered tool for cracking and training CAPTCHA models. It provides the capability to deploy and interface with a **CAPTCHA22** server instance.

### Table of contents 

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

*For more information, refer to [CONTRIBUTING.MD](https://github.com/FSecureLABS/captcha_cracking/CONTRIBUTING.MD)*

# Getting Started

**CAPTCHA22** requires a working [Tensorflow](https://github.com/tensorflow/tensorflow) install. To verify your tensorflow installation, execute the following:

```
python -c 'import tensorflow as tf'
```

*CAPTCHA cracking is most efficient on a GPU-enabled Tensorflow build. Considering hosting such a server either locally or using a resource such as AWS for server hosting*

To host CAPTCHA models, the [Tensorflow Serving](https://github.com/tensorflow/serving) addon is also required.

## Installation 

To install the current release of **CAPTCHA22**:

```bash
$ pip install captcha22
```

To update **CAPTCHA22** to the latest version, add `--upgrade` flag to the above command.

## Usage 

**CAPTCHA22** consists of two main components: the [**server**](https://github.com/FSecureLABS/captcha_cracking/captcha22_server.py), *which will host the server and API*; and the [**client**](https://github.com/FSecureLABS/captcha_cracking/captcha22_client.py), *which allows you to interface with the server, run offline scripts, and automate CAPTCHA cracking attacks.*

1. Run the server:

    ```bash
    $ captcha22_server server & captcha22_server api
    ```
    _**OR** for only the cracking server, use:_
    ```bash
    $ captcha22_server server
    ```

    For a list of server commands and arguments, use:
    ```bash
    captcha22_server -h
    ```

2. Run the client:

    ```bash
    $ captcha22_client api
    ```
    _**OR** chose a cracking script and use:_
    ```bash
    $ captcha22_client cracker <script>
    ```

    For a list of client commands, scripts, and arguments, use:
    ```bash
    $ captcha_client -h
    ```

# Contributing

This project is in its early days and there's still plenty that can be done. Whether its submitting a fix, identifying bugs, suggesting enhancements, creating or updating documentation, refactoring smelly code, or even extending this list — all contributions help and are more than welcome. Please feel free to use your judgement and do whatever you think would benefit the community most.

*See [Contributing](https://github.com/FSecureLABS/captcha_cracking/CONTRIBUTING.md) for more information.*

# License 

**CAPTCHA22** is a graph-based tool for visualizing effective access and resource relationships within AWS. (C) 2018-2020 F-SECURE.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
