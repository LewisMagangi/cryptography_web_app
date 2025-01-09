# Cryptography Web App

This project is a comprehensive web application that focuses on cryptographic analysis and includes a blog for sharing insights and updates. The application aims to optimize system performance by dynamically selecting cryptographic algorithms based on end-user needs. The system is divided into subsystems according to the functionality of the algorithms. Hashing algorithms, used for verifying message integrity, have a dedicated subsystem. A comparative analysis is conducted to determine the most suitable algorithm, taking all relevant factors into account.

## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Visualization](#visualization)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Introduction

In the world of IT, there's always a dilemma about the best algorithm to use. Many developers, whose expertise may not be deeply intertwined with security, often face challenges when it comes to cryptography. While developing websites, systems, or applications, developers tend to use algorithms with a reputable reputation, ones they have used before, or those recommended by more experienced engineers. Regardless of the method used to select the algorithm, there's always a question of which is the most efficient and robust cryptographic algorithm to use.

Developers may be tempted to tweak the implementation of an algorithm to make it faster or consume less power, especially in large-scale production projects where the team aims to reduce maintenance costs. However, cryptographers and cryptoanalysts understand the negative implications of such endeavors. Engineers might be aware of the potential consequences and choose to get all hands on deck to ensure the security and efficiency of their cryptographic implementations.

## Features

List the key features of your project.

## Getting Started

Guide users through getting your project up and running on their local machine.

### Prerequisites

List any software, libraries, or dependencies that users need to have before they can use your project.

- Python 3.8 or higher
- Git

### Installation

Provide step-by-step instructions on how to install and set up your project.

1. **Clone the repository:**

    ```sh
    git clone https://github.com/LewisMagangi/cryptography_web_app.git
    cd cryptography_web_app
    ```

2. **Set up a virtual environment:**

    On Windows:
    ```sh
    python -m venv venv_cryptography
    venv_cryptography\Scripts\activate
    ```

    On macOS and Linux:
    ```sh
    python3 -m venv venv_cryptography
    source venv_cryptography/bin/activate
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Running the Django Blog

1. **Navigate to the Django project directory:**

    ```sh
    cd blog
    ```

2. **Apply the migrations:**

    ```sh
    python manage.py migrate
    ```

3. **Run the Django development server:**

    ```sh
    python manage.py runserver
    ```

    The blog will be accessible at `http://127.0.0.1:8000/`.

## Usage

Include examples and explanations of how to use your project. Provide code snippets if necessary.

1. **Run the symmetric encryption analysis:**

    ```sh
    python src/symmetric.py
    ```

    This will perform encryption and decryption analysis using various symmetric algorithms and save the results to `data/results/symmetric_analysis_results.csv`.

2. **Run the asymmetric encryption analysis:**

    ```sh
    python src/asymmetric.py
    ```

    This will perform encryption and decryption analysis using various asymmetric algorithms and save the results to `data/results/asymmetric_analysis_results.csv`.

3. **Run the hashing analysis:**

    ```sh
    python src/hashing.py
    ```

    This will perform hashing analysis using various hashing algorithms and save the results to `data/results/hashing_analysis_results.csv`.

4. **View the results:**

    The results of the encryption, decryption, and hashing analysis will be saved in the `data/results` directory:
    - Symmetric analysis results: `data/results/symmetric_analysis_results.csv`
    - Asymmetric analysis results: `data/results/asymmetric_analysis_results.csv`
    - Hashing analysis results: `data/results/hashing_analysis_results.csv`

## Visualization

1. **Run the visualization scripts:**

    ```sh
    python src/symmetric_analysis_visualization.py
    python src/asymmetric_analysis_visualization.py
    python src/hashing_analysis_visualization.py
    ```

    These scripts will take the data from the respective CSV files and generate graphs for analysis.

2. **View the analysis graphs:**

    The generated graphs will be saved in the `data/graphs` directory:
    - Symmetric analysis graphs: `data/graphs/symmetric`
    - Asymmetric analysis graphs: `data/graphs/asymmetric`
    - Hashing analysis graphs: `data/graphs/hashing`

### Additional Information

Provide any additional information or resources that might be helpful for users.

- [Python Documentation](https://docs.python.org/3/)
- [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/en/latest/)
- [Django Documentation](https://docs.djangoproject.com/en/stable/)

## Contributing

Explain how people can contribute to your project. Include guidelines for submitting issues or pull requests.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Give credit to any third-party resources, libraries, or tools that you used or were inspired by during the development of your project.