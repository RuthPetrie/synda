#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains paths and configuration parameters."""

import os
import argparse
import sdtools
import sdcfloader
import sdcfbuilder
from sdexception import SDException
# this module do not import 'sdapp' to prevent circular reference
# this module do not import 'sdlog' as used by sddaemon module (i.e. double fork pb)

def get_path(name,default_value):
    path=config.get('core',name)
    if len(path)>0:
        return path
    else:
        return default_value

def get_project_default_selection_file(project):
    path="%s/default_%s.txt"%(selection_default_folder,project)
    return path

def find_selection_file(file):
    if os.path.isfile(file):
        # file found

        return file
    else:
        if '/' in file:
            # path

            # if we are here, path is incorrect.
            # we return the path 'as is'
            # (it will trigger an error message in the calling func)

            return file
        else:
            # filename

            # if we are here, we expect the file to be in the 'selection' folder

            return "%s/%s"%(selections_folder,file)

def check_path(path):
    if not os.path.exists(path):
        raise SDException("SDATYPES-101","Path not found (%s)"%path)

def print_(name):
    if name is None:
        # print all configuration parameters

        sdtools.print_module_variables(globals())
    else:
        # print given configuration parameter

        if name in globals():
            print globals()[name]

def is_openid_set():
    if openid=='https://esgf-node.ipsl.fr/esgf-idp/openid/foo':
        return False
    else:
        return True

def is_special_user():
    """
    Notes
        - special-user can be
            - root (when using system package installation)
            - <user> who performed synda installation from source (can be root or a normal user)
    """

    if multiuser:
        # in system package based installation, root is always the special-user

        if sdtools.is_root():
            return True
        else:
            return False

    else:
        # in source based installation, the special-user can be any user

        if sdtools.is_file_read_access_OK(credential_file):

            # note that root is always considered 'special-user'
            # because of the side-effect that he have access to all files.
            # maybe use 'file owner' here instead to fix this.

            return True
        else:
            return False

# Init module.

multiuser=False # TODO: rename to 'system_pkg_install'

if not multiuser:
    if 'ST_HOME' not in os.environ:
        raise SDException('SDCONFIG-010',"'ST_HOME' is not set")

    root_folder=os.environ['ST_HOME']
    tmp_folder="%s/tmp"%root_folder
    log_folder="%s/log"%root_folder
    conf_folder="%s/conf"%root_folder
    selections_folder="%s/selection"%root_folder

    default_db_folder="%s/db"%root_folder
    default_data_folder="%s/data"%root_folder
    default_sandbox_folder="%s/sandbox"%root_folder
else:
    root_folder='/usr/share/python/synda/sdt'
    tmp_folder='/var/tmp/synda/sdt'
    log_folder='/var/log/synda/sdt'
    conf_folder='/etc/synda/sdt'
    selections_folder='/etc/synda/sdt/selection'

    default_db_folder='/var/lib/synda/sdt'
    default_data_folder='/srv/synda/sdt/data'
    default_sandbox_folder='/srv/synda/sdt/sandbox'

bin_folder="%s/bin"%root_folder
selection_default_folder="%s/default"%conf_folder

data_download_script_http="%s/sdget.sh"%bin_folder
data_download_script_gridftp="%s/sdgetg.sh"%bin_folder

logon_script="%s/sdlogon.sh"%bin_folder
cleanup_tree_script="%s/sdcleanup_tree.sh"%bin_folder
default_selection_file="%s/default.txt"%selection_default_folder

configuration_file="%s/sdt.conf"%conf_folder
credential_file="%s/credentials.conf"%conf_folder

user_root_dir=os.path.expanduser("~/.sdt")
user_conf_dir=os.path.join(user_root_dir,'conf')

user_configuration_file=os.path.join(user_conf_dir,"sdt.conf")
user_credential_file=os.path.join(user_conf_dir,"credentials.conf")

stacktrace_log_file="%s/stacktrace.log"%log_folder

daemon_pid_file="%s/daemon.pid"%tmp_folder
ihm_pid_file="%s/ihm.pid"%tmp_folder


# set security_dir
if sdtools.is_daemon():

    # better keep tmp_folder for this case
    # (if HOME is used here, it can be root or daemon
    # unprivileged user which increase complexity)

    security_dir="%s/.esg"%tmp_folder
else:

    #if is_special_user():
    #if multiuser:
    security_dir="%s/.esg"%os.environ['HOME']


# set x509 paths
esgf_x509_proxy=os.path.join(security_dir,'credentials.pem')
esgf_x509_cert_dir=os.path.join(security_dir,'certificates')

check_path(root_folder)
check_path(selections_folder)

prevent_daemon_and_modification=False # prevent modification while daemon is running
prevent_daemon_and_ihm=False # prevent daemon/IHM concurrent accesses
prevent_ihm_and_ihm=False    # prevent IHM/IHM concurrent accesses

files_download=True # if set to False, daemon do not renew certificate nor download files (useful to use synda in post-processing mode only)

dataset_filter_mecanism_in_file_context='dataset_id' # dataset_id | query

max_metadata_parallel_download_per_index=3
sdtc_history_file=os.path.expanduser("~/.sdtc_history")

http_client='wget' # wget | urllib

daemon_command_name='sdtaskscheduler'

# note that variable below only set which low_level mecanism to use to find the nearest (i.e. it's not an on/off flag (the on/off flag is the 'nearest' selection file parameter))
nearest_schedule='post' # pre | post

unknown_value_behaviour='error' # error | warning

# this is to switch between 'sdmyproxy.py' and 'sdlogon.sh'
use_myproxy_module=True

mono_host_retry=False
proxymt_progress_stat=False
poddlefix=True
fix_encoding=False

twophasesearch=False # Beware before enabling this: must be well tested/reviewed as it seems to currently introduce regression.

if not is_special_user():
    # if we are here, it means we have no access to the machine-wide credential file.

    # also if we are here, we are not in daemon mode (daemon mode is
    # currently only available for special-user. see TAG43J2K253J43 for more
    # infos.)

    # create user credential file sample
    os.mkdir(user_conf_dir)
    sdcfbuilder.create_credential_file_sample(user_credential_file)
    os.chmod(user_credential_file,0600)

config=sdcfloader.load(configuration_file,credential_file,user_configuration_file,user_credential_file,special_user=is_special_user())

# aliases
openid=config.get('esgf_credential','openid')
password=config.get('esgf_credential','password')

db_folder=get_path('db_path',default_db_folder)
data_folder=get_path('data_path',default_data_folder)
sandbox_folder=get_path('sandbox_path',default_sandbox_folder)

db_file="%s/sdt.db"%db_folder

check_path(data_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--name',default=None,help='Name of the parameter to be displayed (if not set, all parameters are displayed)')
    args = parser.parse_args()

    print_(args.name)
