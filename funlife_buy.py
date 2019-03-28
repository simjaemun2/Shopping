#!/Users/a1/anaconda3/bin/python

import sys
import configparser

from funlife import Funlife


if len(sys.argv) < 2:
    print("There is no path of config!!")
    exit(1)

config = configparser.ConfigParser()
config.read(sys.argv[1])

fun = Funlife(config)
fun.buy_happy()