#!/usr/bin/env python2
#-*- coding: utf-8 -*-
"""
arrr is using archiveready.org's api
"""

__version__ = "0.1"
__status__ = "quick hack"
__author__ = 'steffen fritz'
__contact__ = 'fritz@dla-marbach.de'
__license__ = 'The MIT License (c) 2014 DLA Marbach'

import sys
import simplejson
import urllib

base_url = "http://archiveready.com/api?url="


def get_url_from_warc(warc_file):
    """
    :param: warc_file as input
    """
    url_list = []
    with open(warc_file, "r") as fd:
        for line in fd:
            if line.lower().startswith("warc-target-uri"):
                url_ = line.split(":", 1)[1].strip()
                if url_.startswith("http") or url_.startswith("https"):
                    if url_ not in url_list:
                        url_list.append(url_)

    with open("url_list.txt", "w") as fe:
        for url in url_list:
            fe.write(url + "\n")


def read_source(batch_file):
    """
    :param: batch_file
    :return: url_list
    :rtype: list
    """
    fd = open(batch_file, "r")
    url_list = fd.readlines()
    fd.close()

    return url_list


def ask_arc(url_list):
    """
    :param: url_list
    """
    counter = 0
    for url in url_list:
        counter += 1
        url_ = base_url + url
        print("\nCalling: " + url_)
        file_name_lst = url_.split(':', 2)
        file_name_ = file_name_lst[2].replace("/", "_")[:-1] + "_result.txt"
        ud = urllib.urlopen(base_url + url)
        raw_response = ud.read()
        get_n_print_info(raw_response, file_name_)
        print("URLs tested: " + str(counter))


def get_n_print_info(raw_response, file_name_):
    """
    :param: raw_response
    :param: file_name_
    """
    fd = open("results_last_final/" + file_name_, "w")
    jstr = simplejson.loads(raw_response)
    
    print("Finished: " + jstr['url'] + "\n")

    fd.write("URL: " + jstr['url'] + "\n")
    fd.write("Testdatum: " + str(jstr['created']) + "\n")
    fd.write("Standard Compliance: " + str(jstr['test']['Standards_Compliance']) + "\n")
    fd.write("Archivierbarkeit: " + str(jstr['test']['website_archivability']) + "\n")
    fd.write("Accessibility: " + str(jstr['test']['Accessibility']) + "\n")
    fd.write("Kohäsion: " + str(jstr['test']['Cohesion']) + "\n")
    fd.write("\n+++ Meldungen +++\n")

    for message in jstr['messages']:
        fd.write("-" * 40)
        fd.write("\nTitel: " + message['title'] + "\n")
        fd.write("Level: " + str(message['level']) + "\n")
        fd.write("Gewichtung: " + message['significance'] + "\n")
        fd.write("Beschreibung:\n" + message['message'] + "\n")
        fd.write("\n")

    fd.close()


def main():
    """
    :return:
    """
    if len(sys.argv) != 2:
        print("\nUsage: arrr.py [URL_SOURCE_FILE.txt |  WARC_FILE.warc]\n")
        sys.exit(0)
    if sys.argv[1].endswith(".txt"):
        url_list = read_source(sys.argv[1])
        ask_arc(url_list)
    elif sys.argv[1].endswith(".warc"):
        get_url_from_warc(sys.argv[1])
    else:
        print("\nUsage: arrr.py [URL_SOURCE_FILE.txt | WARC_FILE.warc]\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
