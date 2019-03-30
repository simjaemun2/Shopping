# Auto shopping using selinium

## List of web-site
Shopping mall site will be added.
- funlife

## Prerequisit
- Chrome web driver
- Python 3.X
- config file

## Usage

``` bash
python funlife_buy.py <config file path> &
python funlife_coupon.py <config file path> &
```
- config file path : config file for funlife

## TODO-List
- Use multiprocess to buy multiple item at the same time
- Docker container to get web driver and set config file automatically.
- Automatically terminate program when item is closed.
- Error handling accurately
- Handle bad network traffic