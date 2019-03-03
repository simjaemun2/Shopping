# Auto shopping using selinium

## List of web-site
Shopping mall site will be added.
- funlife

## Prerequisit
- Chrome web driver
- Python 3.X
- List of item url

## Usage

``` bash
funlife.py <config file path> <num of happy> &
```
- config file path : config file for funlife
- (optinal) num of happy : num to buy (default 5) 
- Current version buy item just once. 

## TODO-List
- Use multiprocess to buy multiple item at the same time
- Get automatically url of item when item is opened. Current program needs to get a list of url that opened in the past.
- Docker container to get web driver and set config file automatically.
- Automatically terminate program when item is closed.