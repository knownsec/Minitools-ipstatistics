#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import ipdb
import mmap
import random
import argparse
from collections import defaultdict
from termcolor import colored


if(sys.platform == 'win32'):
    os.system('color')


db = ipdb.City(os.path.abspath('./mydata4vipday4.ipdb'))


FVEY = ['美国', '加拿大', '澳大利亚', '新西兰', '英国']


def get_file_lines(filepath):
    with open(filepath, "r+") as fp:
        buf = mmap.mmap(fp.fileno(), 0)
        lines = 0
        while buf.readline():
            lines += 1
        return lines


def export(filepath, country, province, quantity, idc):
    res = []
    with open(filepath) as f:
        for line in f:
            url = line.strip()
            ip = url.split('://')[-1].split('/')[0].split(':')[0]
            info = db.find_map(ip, 'CN')

            # exclude idc
            if not idc and info['idc'] == 'IDC':
                continue

            # export by country
            if not (country == '' or info['country_name'] == country):
                continue

            # export by region
            if not (province == '' or info['region_name'] == province):
                continue

            res.append(url)

    random.shuffle(res)
    for i in range(quantity if len(res) > quantity else len(res)):
        print(res[i])


def countryRank(filepath, quantity):
    res = defaultdict(int)
    with open(filepath) as f:
        for line in f:
            url = line.strip()
            ip = url.split('://')[-1].split('/')[0].split(':')[0]
            info = db.find_map(ip, 'CN')

            res[info['country_name']] += 1

    rank = sorted(res.items(), key=lambda item: item[1], reverse=True)
    count = len(rank) if len(rank) < quantity else quantity

    for i in range(0, count):
        if rank[i][0] in FVEY:
            print(colored(str(rank[i]), 'red'))
        else:
            print(str(rank[i]))


def provinceRank(filepath, country, quantity):
    res = defaultdict(int)
    with open(filepath) as f:
        for line in f:
            url = line.strip()
            ip = url.split('://')[-1].split('/')[0].split(':')[0]
            info = db.find_map(ip, 'CN')

            if info['country_name'] == country:
                res[info['region_name']] += 1

    rank = sorted(res.items(), key=lambda item: item[1], reverse=True)
    count = len(rank) if len(rank) < quantity else quantity
    for i in range(0, count):
        print(str(rank[i]))


def main():
    try:
        arg_parser = argparse.ArgumentParser(
            description=(
                '[*] ' + 'Data statistics use ipipdotnet database' + ' [*]'))
        arg_parser.add_argument(
            '-f',
            '--filepath',
            type=str,
            required=True,
            help='The filepath.')
        arg_parser.add_argument(
            '--idc',
            action='store_true',
            help='Include idc in result.')
        arg_parser.add_argument(
            '-m',
            '--mode',
            type=str,
            choices=['e', 'c', 'p'],
            default='c',
            help=(
                'Operating mode. e/export result that exclude five eyes, '
                'c/country rank, p/province rank.'
            )
        )
        arg_parser.add_argument(
            '-c',
            '--country',
            default='',
            help='The country name. eg. 中国')
        arg_parser.add_argument(
            '-p',
            '--province',
            default='',
            help='The province name. eg. 北京')
        arg_parser.add_argument(
            '-q',
            '--quantity',
            default=0,
            type=int,
            help='The quantity to display.')
        args = arg_parser.parse_args()

    except Exception as e:
        print('\nError: {}\n'.format(str(e)))
        sys.exit(1)

    if args.quantity == 0:
        args.quantity = get_file_lines(args.filepath)

    if args.mode.startswith('e'):
        export(args.filepath, args.country, args.province, args.quantity,
               args.idc)
    elif args.mode.startswith('c'):
        countryRank(args.filepath, args.quantity)
    elif args.mode.startswith('p'):
        provinceRank(args.filepath, args.country, args.quantity)


if __name__ == '__main__':
    main()
