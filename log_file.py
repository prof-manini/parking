# -*- coding:utf-8 -*-

def to_file(str):
    with open("log_saved.txt", "a+") as log_file:
        log_file.write(str + "\n")
