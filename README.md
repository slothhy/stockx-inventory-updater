# stockx-inventory-updater

![Screenshot](https://i.imgur.com/RIFEo54.png)

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
2. python3 **`stockx-inventory-updater.py`**

## Bugs
If you encounter captcha or 403 errors, try solving captcha by browsing the StockX website manually and see if it disappears.
Feel free to report any bugs running the script.

## To-do
* Autorun script daily or weekly
* Notify user if desired price is far off the average sale or last sale
