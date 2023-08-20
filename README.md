# SQL Error

SQL Error is a tool to scan web pages for potential SQL injection vulnerabilities. It sends HTTP requests to URLs and checks if the response contains SQL syntax error messages, indicating a potential vulnerability.

## Requirements

1. To run the SQL Error, you need to have Python installed on your system. You also need to install the following libraries using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.

## Usage

1. You can run the SQL Error using the following command:
    ```bash
    python SqlError.py [base_url]
    
If you provide the base_url argument, the scanner will start scanning from that URL.

If you don't provide the base_url argument, the scanner will prompt you to enter the start URL.

Press Ctrl+C at any time to interrupt the scanning process. The scanner will display the URLs with potential SQL injection vulnerabilities found during the scan.

## Examples

Start scanning from a specific URL:
  ```bash
  python SqlError.py [base_url]
  ```

Start scanning with user input for the start URL:
  ```bash
  python SqlError.py
  ```
## Disclaimer

This tool is for educational and informational purposes only. Use it responsibly and only on websites that you have permission to scan. The authors are not responsible for any misuse or damage caused by this tool.

## License

This project is licensed under the MIT License.

## Support me

<a href="https://www.buymeacoffee.com/SmakeMeMo" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/black_img.png" alt="Buy Me A Coffee">
