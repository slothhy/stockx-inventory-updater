# stockx-inventory-updater

![Screenshot](https://i.imgur.com/FsZhTF3.png)

## Installation
```
pip3 install -r requirements.txt
```
## Features
* Get product name
* Get last sale
* Get average of last 3 sales
* Set desired currency

## Configuration
Currency and row to start with can be edited in the **`config.json`** file.

## How to use
1. Fill in style code and size in the workbook provided.
2. Open terminal or command prompt and cd to the directory.
3. python3 **`stockx-inventory-updater.py`**
4. Results will be output to **`stockx_book_output.xlsx`**

## Bugs
403 errors are caused by too many requests from the same IP in a short time. \
Once encountered, click [here](https://stockx.com/api/browse?) on an incognito browser and solve the captcha. \
The workaround now would be to change the starting row if the script encounters a 403 to continue from there. \
Feel free to report any bugs running the script.

## To-do
* Autorun script daily or weekly (tough with dem captchas)
* Notify user if desired price is far off the average sale or last sale