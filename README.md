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
* Get highest bid
* Get lowest ask
* Set desired currency

## Configuration
**`config.json`**
1. Set currency and starting row.
2. Set the user agent of the browser you will be using to solve any captcha.

## How to use
1. Fill in style code and size in the workbook provided.
2. Open terminal or command prompt and cd to the directory.
3. python3 **`stockx-inventory-updater.py`**
4. Results will be output to **`stock_book_output.xlsx`**
5. 403 errors are caused by too many requests from the same IP in a short time.\
Once encountered, click [here](https://stockx.com) on the incognito browser that you have set the user agent of and solve the captcha.
The workaround now would be to change the starting row if the script encounters a 403 to continue from there.

## Bugs
Feel free to report any bugs running the script.

## To-do
* Autorun script daily or weekly (tough with dem captchas)
* Notify user if desired price is far off the average sale or last sale