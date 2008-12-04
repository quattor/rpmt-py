#!/usr/bin/python
# -- coding: iso8859-1

""" RPMT-PY Option Parser Module.

This module is used to parse the command line options given to the rpmt-py tool.

It provides a simple class to define each option by extending the L{generic_OptionParser} module.

"""

from generic_OptionParser import *

class rpmtOptionParser(genericOptionParser):
    """ RPMT Option Parser class.
    """
    
    def __init__(self):
        genericOptionParser.__init__(self, self._define_options(), self._define_order())

    def _define_order(self):
        """ This method simply defines the order of the options
        (for printing purposes)
        """
        
        o = (
            'input',            
            'version',
            'quiet',
            'verbose',
            #'debug',
            #'rcfile',
            'dbpath',
            'root',
            'cachedir',
            'revproxy',
            'httpproxy',
            'httpport',
            'ftpproxy',
            'ftpport',
            'noclean',
            'forceclean',
            'allfiles',
            'excludedocs',
            'force',
            'ignoresize',
            'ignorearch',
            'ignoreos',
            'justdb',
            'nodeps',
            'noorder',
            'noscripts',
            'notriggers',
            'repackage',
            'replacefiles',
            'replacepkgs',
            'test',
            'nodigest',
            'nosignature'
            )

        return o
        
    def _define_options(self):
        """ This method defines each option
        using the genericOptionParser format :

        
        'option_var' : \
        ('short=<short option>',
        'long=<long option>',
        'help=<help string>',
        'meta=<meta variable>',
        'default=<default value>',
        'type=<option type>'
        )
        type = string (default) OR bool
        """
                
        o = {
            ######
            # general options
                        
            'version': ('short=V',
                        'long=version',
                        'help=print version number of rpmt-py being used',
                        'type=bool'),
            
            'quiet': ('short=q',
                      'long=quiet',
                      'help=provide less detailed output',
                      'type=bool'),
            
            'verbose': ('short=v',
                        'long=verbose',
                        'help=provide more detailed output',
                        'type=bool'),

            ######
            # input file name
            
            'input': ('short=i',
                      'long=in',
                      'help=input file (actions)',
                      'meta=<IN>'),           
            
            #'debug': ('short=d',
            #          'long=debug',
            #          'help=provide debugging information output',
            #          'type=bool'),

            # --rcfile is not used anymore
            #'rcfile': ('short=',
            #           'long=rcfile',
            #           'help=read <FILE> instead of default configuration file',
            #           'meta=<FILE>'),
            
            'dbpath': ('short=',
                       'long=dbpath',
                       'help=use database in <DIR> instead of default path',
                       'meta=<DIR>'),
            
            'root': ('short=r',
                     'long=root',
                     'help=use <ROOT> as top level directory (default is /)',
                     'meta=<ROOT>'),

            'cachedir': ('short=',
                         'long=cachedir',
                         'help=use <CACHEDIR> when retrieving remote packages (default is /var/cache/rpmt/)',
                         'meta=<CACHEDIR>'),

            'revproxy': ('short=',
                         'long=revproxy',
                         'help=use one or multiple reverse proxies when retrieving remote packages (multiple servers are delimited by a comma)',
                         'meta=<REVPROXYLIST>'),
            

            'httpproxy': ('short=',
                          'long=httpproxy',
                          'help=the <HTTPPROXY> will be used as a proxy server for all http transfers',
                          'meta=<HTTPPROXY>'),
            

            'httpport': ('short=',
                         'long=httpport',
                         'help=use the specified <PORT> instead of the default port',
                         'meta=<HTTPPORT>'),
            

            'ftpproxy': ('short=',
                         'long=ftpproxy',
                         'help=the <FTPPROXY> will be used as a proxy server for all ftp transfers',
                         'meta=<FTPPROXY>'),
            

            'ftpport': ('short=',
                        'long=ftpport',
                        'help=use the specified <PORT> instead of the default port',
                        'meta=<FTPPORT>'),
            
            'noclean': ('short=',
                        'long=noclean',
                        'help=never clean the cache after running the transaction set',
                        'type=bool'),

            'forceclean': ('short=',
                        'long=forceclean',
                        'help=always clean the cache even if transaction fails',
                        'type=bool'),
            
            ######
            # installation and upgrading options

            'allfiles': ('short=',
                         'long=allfiles',
                         'help=install all files, even conf. which might otherwise be skipped',
                         'type=bool'),
            
            'excludedocs': ('short=',
                            'long=excludedocs',
                            'help=do not install documentation',
                            'type=bool'),

            'force': ('short=',
                      'long=force',
                      'help=short hand for --replacepkgs --replacefiles',
                      'type=bool'),

            'ignoresize': ('short=',
                           'long=ignoresize',
                           'help=don\'t check disk space before installing',
                           'type=bool'),

            'ignorearch': ('short=',
                           'long=ignorearch',
                           'help=don\'t verify package architecture',
                           'type=bool'),

            'ignoreos': ('short=',
                         'long=ignoreos',
                         'help=don\'t verify package operating system',
                         'type=bool'),

            'justdb': ('short=',
                       'long=justdb',
                       'help=update the database, but do not modify the filesystem',
                       'type=bool'),

            'nodeps': ('short=',
                       'long=nodeps',
                       'help=do not verify package dependencies',
                       'type=bool'),

            'noorder': ('short=',
                        'long=noorder',
                        'help=do not reorder package installation to satisfy dependencies',
                        'type=bool'),

            'noscripts': ('short=',
                          'long=noscripts',
                          'help=do not execute package scriptlet(s)',
                          'type=bool'),

            'notriggers': ('short=',
                           'long=notriggers',
                           'help=do not execute any scriptlet(s) triggered by package(s)',
                           'type=bool'),

            # --oldpackage is assumed true

            'repackage': ('short=',
                          'long=repackage',
                          'help=re-package files before erasing',
                          'type=bool'),
            
            'replacefiles': ('short=',
                             'long=replacefiles',
                             'help=install even if the package replaces installed files',
                             'type=bool'),
            
            'replacepkgs': ('short=',
                            'long=replacepkgs',
                            'help=reinstall if the package is already present',
                            'type=bool'),
            
            'test': ('short=',
                     'long=test',
                     'help=don\'t install, but tell if it would work or not',
                     'type=bool'),
            
            ######
            # erase options
            
            # the following erase options have been already implemented:
            # --nodeps
            # --noscripts
            # --notriggers
            # --repackage
            # --test
            
            ######
            # verification options            
            
            'nodigest': ('short=',
                          'long=nodigest',
                          'help=don\'t verify package digest(s)',
                          'type=bool'),
            
            'nosignature': ('short=',
                            'long=nosignature',
                            'help=don\'t verify package signature(s)',
                            'type=bool')      
            }
        
        return o


# Module Test  
if __name__=="__main__":
    r = rpmtOptionParser()
    optdict = r.parse_arguments()

    for key,value in optdict.items():
        print key, value

        
                    
