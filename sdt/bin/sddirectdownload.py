#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script run download test on each url and display download status.

Note
    Return code is always 0
"""

import argparse
import os
import sys
import json
import sdapp
import sdconfig
import sdget
import sdget_urllib
from sdtypes import File
from sdtools import print_stderr

def run(files):
    for file_ in files:

        # check

        assert 'url' in file_
        assert 'data_node' in file_
        assert 'local_path' in file_


        # cast

        f=File(**file_)


        # prepare attributes

        #local_path='/tmp/test.nc'
        #local_path='%s/test.nc'%sdconfig.tmp_folder
        local_path=f.get_full_local_path()


        # check

        if os.path.isfile(local_path):
            #os.remove(local_path)
            print_stderr('WARNING: download cancelled as local file already exists (%s)'%local_path)
            continue


        # transfer

        #(status,local_checksum,killed,script_stderr)=sdget.download(f.url,local_path,af.checksum_type,False)
        (status,local_checksum)=sdget_urllib.download_file(f.url,local_path,f.checksum_type)


        # post-transfer

        attribute_to_show_in_msg=local_path # local_path | f.data_node | ..

        if status!=0:
            print_stderr('Download failed (%s)'%attribute_to_show_in_msg)
        else:
            print_stderr('File successfully downloaded (%s)'%attribute_to_show_in_msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )

    run(files)

    sys.exit(0)