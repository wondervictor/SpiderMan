# -*- coding: utf-8 -*-

"""
Download
"""

import urllib2


def download(url, filepath):
    """
    Download with urllib2
    :param url: file destination
    :param filepath: file path to save
    :return: 
    """
    print("Downloading ....from:\n %s" % url)
    f = urllib2.urlopen(url)
    data = f.read()
    with open(filepath, 'wb') as open_file:
        open_file.write(data)

    print("Download finished saved to: %s" % filepath)


