"""EditorConfig command line interface

Licensed under PSF License (see LICENSE.txt file).

"""

import getopt
import sys

from editorconfig import __version__, VERSION
from editorconfig.versiontools import split_version
from editorconfig.handler import EditorConfigHandler
from editorconfig.exceptions import ParsingError, PathError, VersionError


def version():
    print "Version %s" % __version__


def usage(command, error=False):
    if error:
        out = sys.stderr
    else:
        out = sys.stdout
    print >> out, "%s [OPTIONS] FILENAME" % command
    print >> out, ('-f                 '
            'Specify conf filename other than ".editorconfig".')
    print >> out, ("-b                 "
            "Specify version (used by devs to test compatibility).")
    print >> out, "-h OR --help       Print this help message."
    print >> out, "-v OR --version    Display version information."


def main():
    command_name = sys.argv[0]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhb:f:", ["version", "help"])
    except getopt.GetoptError, err:
        print str(err)
        usage(command_name, error=True)
        sys.exit(2)
    if len(args) > 1:
        usage(command_name, error=True)
        sys.exit(2)

    version_tuple = VERSION
    conf_filename = '.editorconfig'

    for option, arg in opts:
        if option in ('-h', '--help'):
            usage(command_name)
            sys.exit()
        if option in ('-v', '--version'):
            version()
            sys.exit()
        if option == '-f':
            conf_filename = arg
        if option == '-b':
            version_tuple = split_version(arg)
            if version_tuple is None:
                sys.exit("Invalid version number: %s" % arg)

    if len(args) < 1:
        usage(command_name, error=True)
        sys.exit(2)
    filename = args[0]

    handler = EditorConfigHandler(filename, conf_filename, version_tuple)
    try:
        options = handler.get_configurations()
    except (ParsingError, PathError, VersionError), e:
        print >> sys.stderr, str(e)
        sys.exit(2)
    for key, value in options.items():
        print "%s=%s" % (key, value)
