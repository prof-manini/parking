# -*- coding:utf-8 -*-

import argparse
parser = argparse.ArgumentParser()

from datetime import date, timedelta
yesterday = date.today() - timedelta(1)


# Opzioni programma (--car, --sensor, --date)
parser.add_argument("-c", "--car", help="Specify the car you want to see the timing in the parking", type=int, default=None, required=False)
parser.add_argument("-s", "--sensor", help="Specify the sensor you want to see cars parked", type=int, default=None, required=False)
parser.add_argument("-d", "--date", help="Specify the date when you want to see all parked cars in that day", type=str, required=False)


def main(args):

    nris = 0

    car = str(args.car) if args.car != None else ""
    sensor = str(args.sensor) if args.sensor != None else ""
    date = args.date if args.date != None else yesterday.strftime("%Y/%m/%d")

    with open("log_saved.txt", "r") as log_file:
        for line in log_file.readlines():
            lcar, lsensor, levent, ldate, ltime = line.replace("\n", "").split(" ")
            print line.replace("\n", "").split(" ")
            if car in lcar and sensor in lsensor and date in ldate:
                print (line.strip())
                nris += 1

    log_file.close

    if not nris > 0:
        print ("Nessun risultato per la ricerca effettuata!")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
