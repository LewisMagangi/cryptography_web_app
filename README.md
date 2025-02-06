# Cryptography Web App

This project is a comprehensive web application that focuses on cryptographic analysis and includes a blog for sharing insights and updates. The application aims to optimize system performance by dynamically selecting cryptographic algorithms based on end-user needs. The system is divided into subsystems according to the functionality of the algorithms. Hashing algorithms, used for verifying message integrity, have a dedicated subsystem. A comparative analysis is conducted to determine the most suitable algorithm, taking all relevant factors into account.

## Introduction

In the world of IT, there's always a dilemma about the best algorithm to use. Many developers, whose expertise may not be deeply intertwined with security, often face challenges when it comes to cryptography. While developing websites, systems, or applications, developers tend to use algorithms with a reputable reputation, ones they have used before, or those recommended by more experienced engineers. Regardless of the method used to select the algorithm, there's always a question of which is the most efficient and robust cryptographic algorithm to use.

Developers may be tempted to tweak the implementation of an algorithm to make it faster or consume less power, especially in large-scale production projects where the team aims to reduce maintenance costs. However, cryptographers and cryptoanalysts understand the negative implications of such endeavors. Engineers might be aware of the potential consequences and choose to get all hands on deck to ensure the security and efficiency of their cryptographic implementations.

## Branch Information

- `development`: For local development only
- `deployment`: For production server deployment only (requires web server setup)

## Getting Started

Here's how you can get the project up and running on your local machine.

### Prerequisites

Make sure you have the following software installed:

- Python 3.8 or higher
- Git

### Installation

Follow these steps to set up the project:

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

### Data Generation

1. **Generate sample text data:**
   ```sh
   # For small sample sizes (0-250 bytes)
   cd analysis/data/smaller_sample_text/
   python fak-range-data-gen.py

   # For larger sample sizes (1-50 MB)
   cd analysis/data/sample_text/
   python fak-range-data-gen.py
   ```

### Database Setup

1. **Create and apply migrations:**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create superuser (if needed):**
   ```sh
   python manage.py createsuperuser
   ```

## Running the Django Blog

To get the blog up and running:

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

    You can now access the blog at `http://127.0.0.1:8000/`.

## Usage

Here's how you can use the project:

1. **Run the symmetric encryption analysis:**

    ```sh
    python analysis/src/symmetric.py
    ```

    This script performs encryption and decryption analysis using various symmetric algorithms and saves the results to `data/results/symmetric_analysis_results.csv`.

2. **Run the asymmetric encryption analysis:**

    ```sh
    python analysis/src/asymmetric.py
    ```

    This script performs encryption and decryption analysis using various asymmetric algorithms and saves the results to `analysis/data/results/asymmetric_analysis_results.csv`.

3. **Run the hashing analysis:**

    ```sh
    python analysis/src/hashing.py
    ```

    This script performs hashing analysis using various hashing algorithms and saves the results to `analysis/data/results/hashing_analysis_results.csv`.

4. **View the results:**

    The results of the encryption, decryption, and hashing analysis will be saved in the `analysis/data/results` directory:
    - Symmetric analysis results: `analysis/data/results/symmetric_analysis_results.csv`
    - Asymmetric analysis results: `analysis/data/results/asymmetric_analysis_results.csv`
    - Hashing analysis results: `analysis/data/results/hashing_analysis_results.csv`

## Visualization

To visualize the analysis results:

1. **Run the visualization scripts:**

    ```sh
    python analysis/src/data_visualization.py
    python analysis/src/asymmetric_analysis_visualization.py
    ```

    These scripts will generate graphs from the data in the respective CSV files.

2. **View the analysis graphs:**

    The generated graphs will be saved in the `data/graphs` directory:
    - Symmetric analysis graphs: `data/graphs/symmetric`
    - Asymmetric analysis graphs: `data/graphs/asymmetric`
    - Hashing analysis graphs: `data/graphs/hashing`

### Additional Information

Here are some additional resources that might be helpful:

- [Python Documentation](https://docs.python.org/3/)
- [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/en/latest/)
- [Django Documentation](https://docs.djangoproject.com/en/stable/)

## Contributing

Want to contribute to this project? Great! Feel free to submit issues or pull requests. Make sure to follow the guidelines for contributing.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

A big thank you to all the third-party resources, libraries, and tools that made this project possible. Your contributions and inspirations are greatly appreciated.