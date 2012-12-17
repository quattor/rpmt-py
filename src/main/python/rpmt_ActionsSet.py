#!/usr/bin/python -tt
# -- coding: iso8859-1

""" RPMT-PY Actions Set Module.

This module provides the rpmtActionsSet class which is used to parse each
action from a rpmt actions file.

"""

__version__ = "1.0.8"

import os,sys

class rpmtActionsSet:
    """ RPMT Actions Set Class
    """

    def __init__(self, filename):
        """ This is the default constructor.

        @param filename: the actions file name
        """
        self._file = open(filename, 'r')
        self._filename = filename
        self._lineno = 0

    def nextAction(self):
        """ The nextAction() method moves to the next action in the file and
        returns a dictionnary:

         - ('action':'a', 'package':'p', 'options': []) where:
          - a is the action : 'install', 'upgrade' or 'erase' (string)
          - p is the package file name (string)
          - [] is a sequence of options (not used yet)
         - or ('error':'error message') if something wrong happened.

        None is returned if the end of the file is reached.
        """
        
        words = []

        # Move to next action
        while not words:
            line = self._file.readline()
            self._lineno += 1
            # EOF ?
            if not line: return None
            words = line.split()
            # Comment ?
            if words and words[0][0] == '#':
                words = []
        
        if words[0] == '-i':
            return {
                'action':'install',
                'package':words[1],
                'options': words[2:]
                }         
        elif words[0] == '-u':
            return {
                'action':'upgrade',
                'package':words[1],
                'options': words[2:]
                }           
        elif words[0] == '-e':
            return {
                'action':'erase',
                'package':words[1],
                'options': words[2:]
                }              
        else:
            return {'error':'Unknown command ' + words[0] +
                    ' on file \"' + self._filename +
                    '\" at line ' + str(self._lineno)
                    }
            

# Module Test
if __name__=="__main__":
    try:       
        rpmt_as = rpmtActionsSet('test.rpmta')
    except IOError, error:
        sys.exit(error)

    # Process each action
    action = rpmt_as.nextAction()
    while action:
        try:
            print action['action'], action['package'], action['options']
        except KeyError:
            print action['error']
            
        action = rpmt_as.nextAction()

    
