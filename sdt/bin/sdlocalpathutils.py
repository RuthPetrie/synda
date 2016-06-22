#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
# 						 All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains local path utils."""

import sdapp
import sdconst
import sdpostpipelineutils
from sdexception import SDException

def build_dataset_local_path(f):
    fmt=sdpostpipelineutils.get_attached_parameter(f,'local_path_format',sdconst.DEFAULT_LOCAL_PATH_FORMAT)

    if fmt=="treevar":
        path="%(dataset_path)s"%f # note that we don't add var folder here (we do it only for the file local path)
    elif fmt=="tree":
        path="%(dataset_path)s"%f
    elif fmt=="custom":

        # note: 'sdreducecol' filter must be disabled when using this format

        custom_dataset_template=sdpostpipelineutils.get_attached_parameter(f,'local_path_drs_template')
        if custom_dataset_template is not None:
            path=custom_dataset_template%f
        else:
            raise SDException('SDLOCALP-014',"'local_path_drs_template' must be set when 'local_path_format' is set to 'custom'.")

    elif fmt=="homemade":

        # note: 'sdreducecol' filter must be disabled when using this format

        path=local_path_homemade_transform(f)
    elif fmt=="notree":
        path=""
    else:
        raise SDException('SDLOCALP-010',"'local_path_format' is incorrect (%s)"%fmt)

    return path    

def build_file_local_path(f):
    fmt=sdpostpipelineutils.get_attached_parameter(f,'local_path_format',sdconst.DEFAULT_LOCAL_PATH_FORMAT)

    if fmt=="treevar":
        path="%(dataset_local_path)s/%(variable)s/%(filename)s" % f
    elif fmt=="tree":
        path="%(dataset_local_path)s/%(filename)s"%f
    elif fmt=="custom":
        path="%(dataset_local_path)s/%(filename)s"%f
    elif fmt=="homemade":
        path="%(dataset_local_path)s/%(filename)s"%f
    elif fmt=="notree":
        path="%(filename)s"%f
    else:
        raise SDException('SDLOCALP-001',"'local_path_format' is incorrect (%s)"%fmt)

    return path

def local_path_homemade_transform(f):
    """
    This is to implement complex rules to build local_path (rules which cannot
    fit even using custom format).

    TODO
        Make a plugin of this func
    """

    # user code goes here
    #
    # sample
    path="%(dataset_path)s"%f

    return path