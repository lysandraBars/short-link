URL Shortener Code(Tinyurl) - @T7C
=========================

Overview
---------
This code is a simple URL shortener tool that allows users to shorten URLs, manage a history of shortened links, and handle expired links. It provides a command-line interface (CLI) with a rich, professional, and cyberpunk-style user interface using the `rich` library. The code can also shorten URLs (using tinyurl) directly from the clipboard.

Features
--------
- Shorten URLs: Convert long URLs into short, manageable links.
- View History: Display a history of shortened URLs with timestamps, custom names, and expiry information.
- Update Links: Update an existing shortened link's long URL and expiry time.
- Delete Expired Links: Remove links that have expired from the history.
- Shorten URL from Clipboard: Automatically shorten the URL copied to the clipboard.
- Remind About Expiring Links: Notify users of links that are about to expire.
- Rich Interface: Professional and cyberpunk-style interface with the `rich` library.

Requirements
-------------
- Python 3.x
- `requests` library
- `rich` library
- `pyfiglet` library
- `pyperclip` library

You can install the required libraries using pip:

Setup
------
1. Clone the repository or download the script.

2. Make sure you have Python 3.x installed on your system.

3. Install the required libraries by running:

    ```
    pip install requests rich pyfiglet pyperclip
    ```

4. Run the application with the following command:

    ```
    python shorturl.py
    ```


Usage
------
### Main Menu Options

1. Shorten URL: Enter a long URL to get a shortened version. Optionally, add a custom name and expiry time.
2. View History: See the history of shortened URLs, including their custom names, timestamps, and expiry details.
3. Update Link: Modify an existing link's long URL or expiry time using its custom name.
4. Delete Expired Links: Remove links that have passed their expiry time.
5. Shorten URL from Clipboard: Shorten a URL that is currently in the clipboard.
6. Remind About Expiring Links: Get reminders for links that are close to expiring.
7. Other:
    - View About: Information about the coder.
    - Get File Path: Display the path to the history file.
    - Usega: Placeholder for future functionality.
8. Exit: Close the application.

Notes
------
- The history of shortened URLs is saved in `url_history.json`.
- Expiry times are handled in seconds.

### Contact me
- Gmail: tranminhtan4953@gmail.com
- Telegram: https://tinyurl.com/2xnj2uo2
- Facebook: https://tinyurl.com/2byx7s6f

