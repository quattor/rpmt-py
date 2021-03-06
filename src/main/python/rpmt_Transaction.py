#!/usr/bin/python -tt
# -- coding: iso8859-1

""" RPMT-PY Transaction Module

This module provides everything rpmt needs to handle transaction operations correctly.
"""

import sys,os
import urlparse,urllib,urllib2
import rpm

""" These constants are used to check if the transaction set
has to be checked and ordered.

@see: rpmlib.h
"""
INSTALL_NODEPS = (1<<2)
INSTALL_NOORDER = (1<<3)

class simpleCallback:
    """ This class is used to provide a callback to the transaction set
    run() method.

    @see: rpmtTransaction.
    """
    
    def __init__(self):
        self.fdnos = {}
        
    def verboseCallback(self, what, amount, total, mydata, wibble):
        """ This method provides a verbose callback.

        @param what: callback type
        @param amount: bytes processed
        @param total: total bytes
        @param mydata: package key (hdr, path)
        @param wibble: user data
        """

        if wibble: print wibble
        
        if what == rpm.RPMCALLBACK_TRANS_START:
            pass

        elif what == rpm.RPMCALLBACK_INST_OPEN_FILE:
            hdr, path = mydata
            print "Installing %s\r" % (hdr["name"])
            fdno = os.open(path, os.O_RDONLY)
            nvr = '%s-%s-%s' % ( hdr['name'], hdr['version'], hdr['release'] )
            self.fdnos[nvr] = fdno
            return fdno
        
        elif what == rpm.RPMCALLBACK_INST_CLOSE_FILE:
            hdr, path = mydata
            nvr = '%s-%s-%s' % ( hdr['name'], hdr['version'], hdr['release'] )
            os.close(self.fdnos[nvr])

        elif what == rpm.RPMCALLBACK_INST_PROGRESS:
            hdr, path = mydata
            print "%s:  %.5s%% done\r" % (hdr["name"], (float(amount) / total) * 100)

        return None

    def simpleCallback (self, what, amount, total, mydata, wibble):
        """ This method provides a simple callback.

        @param what: callback type
        @param amount: bytes processed
        @param total: total bytes
        @param mydata: package key (hdr, path)
        @param wibble: user data
        """
        
        if wibble: print wibble

        if what == rpm.RPMCALLBACK_TRANS_START:
            pass

        elif what == rpm.RPMCALLBACK_INST_OPEN_FILE:
            hdr, path = mydata
            fdno = os.open(path, os.O_RDONLY)
            nvr = '%s-%s-%s' % ( hdr['name'], hdr['version'], hdr['release'] )
            self.fdnos[nvr] = fdno
            return fdno


class rpmtTransaction:
    """ RPMT Transaction Class
    """

    def __init__(self, verbose, interface_flags, rpmts_flags, rpmprob_filter, vsflags, rootdir='/', cachedir='/var/cache/rpmt/', revproxylist=[], proxy_info=None):
        """ This is the default constructor.

        @param verbose: verbose state (0 = quiet | (not 0) = verbose)
        @param interface_flags: install flags
        @param rpmts_flags: transaction set flags
        @param rpmprob_filter: problem filter flags
        @param vsflags: verify flags
        @param rootdir: top level directory
        @param cachedir: cache directory for remote packages
        @param revproxylist: list of reverse proxy servers
        @param proxy_info: dictionnary with protocols as keys and corresponding proxies as values
        """
        
        if verbose:
            print "Initializing transaction set"

        self._ts = rpm.TransactionSet(rootdir, vsflags)

        self._verbose = verbose
        self._interface_flags = interface_flags

        self._ts.setFlags(rpmts_flags)
        self._ts.setProbFilter(rpmprob_filter)

        self._cachedir = cachedir
        self._revproxylist = revproxylist
        self._proxy_info = proxy_info
        
    def _handlePackage(self, package, options):
        """ This method handles a package (local or remote) and returns the related rpm header.

        @param package: the package to handle
        @param options: not used yet
        
        @return: (package, hdr) where package is the local package name and hdr is the related rpm header
        """ 

        ###########################################################
        # Is it a remote package ?
        ###########################################################        
        protocol = urlparse.urlsplit(package)
        if protocol[0] not in ['file', ''] :
            # It is a remote file ?
            remote = 1

            #------------------------------------------------------
            # Build the server list (by priority)
            #------------------------------------------------------
            url = list(urlparse.urlsplit(package))
            originalserver = url[1] 
            serverlist = list()
            
            # Do we have to use a proxy in priority ?
            if self._revproxylist:
                if self._verbose:
                    print "Using reverse proxy list", self._revproxylist
                serverlist = list(self._revproxylist)

            serverlist.append(originalserver)
                
            if self._verbose:
                print "Full server list is", serverlist

            #------------------------------------------------------
            # Try to download the package using the server list
            #------------------------------------------------------
            nb_try = 1
            error = 0
            serverlist.reverse()

            while 1:
                try:
                    # Which server do we have to use ?
                    if error != 1 or nb_try == 1:
                        # A new one ?
                        nb_try = 2
                        error = 0
                        # Is there any server left ?
                        if len(serverlist) > 0:
                            server = serverlist.pop()
                            sameserver = 2
                            # Replace the server in the url
                            url[1] = server
                            new_url = urlparse.urlunsplit(url)                            
                        else :
                            break
                    else:
                        # The current server ?
                        # An error occured, we use the sameserver
                        nb_try = nb_try - 1
                        error = 0
                        
                    
                    if self._verbose:
                        print "Trying with server", server
                        print "Retrieving", new_url


                    # Proxy handling
                    if self._proxy_info:
                        if self._verbose:
                            print "Using proxy info:", self._proxy_info
                        proxy_handler = urllib2.ProxyHandler(self._proxy_info)
                        opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler, urllib2.FTPHandler)
                        urllib2.install_opener(opener)
                        
                    # Try to open the file (will provoque a HTTPError if it fails)
                    fin = urllib2.urlopen(new_url)
                    urlhdr = fin.info()
                    
                    # Retrieve the package
                    package = self._cachedir + os.path.basename(package)
                    
                    fout = open(package, 'w')
                    fout.write(fin.read())

                    fin.close()
                    fout.close()

                    sameserver = 0

                    # Get the rpm header
                    fdno = os.open(package, os.O_RDONLY)
                    hdr = self._ts.hdrFromFdno(fdno)
                    os.close(fdno)                    
                    return package, hdr
                
                except urllib2.HTTPError, err:
                    #if hasattr(err, 'code'):
                    #    if err.code in (404,401,403):
                    #        print err
                    
                    # If a HTTPError occurs, we propagate the exception
                    # (the server was reachable but the error comes from the package itself)
                    raise err

                except IOError, err:
                    #if hasattr(err, 'reason'):
                    #    print err.reason
                    
                    # If an IOError occurs, we try another server (next one)                    
                    print err
                    continue
                
                except rpm.error, err:
                    # If a rpm exception occurs, we retry to download the file again
                    error = 1
                    print err
                    
                except Exception, err:
                    dir(err)
                    raise err
                
        ###########################################################
        # It is a local file ?
        ###########################################################
        else:            
            # Simply open the package to get its rpm header
            fdno = os.open(package, os.O_RDONLY)
            hdr = self._ts.hdrFromFdno(fdno)
            os.close(fdno)
            return package, hdr

        # If we reach this point, an error occured during the process of a remote package
        raise IOError, "It was impossible to retrieve the package %s" % os.path.basename(package)
    
    def _check(self):
        """ This method checks the transaction set dependencies and conflicts.

        @return: error messages if something wrong happened.
        """

        deperrors = 0
        conferrors = 0
        msgs = ""

        errors = self._ts.check()

        if errors:	    
            sys.stderr.write("Errors found:\n")
            # After 4.8.0 RPM version the rpm-python bindings change
            if self._rpm_version() > '4.8':
                for ((name, version, release), (reqname, reqversion), \
			flags, sense, suggest) in errors:
		
                    if sense == rpm.RPMDEP_SENSE_REQUIRES:
                        deperrors += 1
                        msgs += (" depcheck: package %s %s-%s needs %s\n") % \
                            (name, version, release, self._formatRequire(reqname, reqversion, flags))
		    
                    elif sense == rpm.RPMDEP_SENSE_CONFLICTS:
                        conferrors += 1
                        msgs += (" depcheck: package %s %s-%s conflicts with %s\n") % \
                            (name, version, release, reqname)
		
                    if self._verbose and suggest:
                        print suggest

            else:
                for ((name, version, release), (reqname, reqversion), \
			flags, suggest, sense) in errors:
		
                    if sense == rpm.RPMDEP_SENSE_REQUIRES:
                        deperrors += 1
                        msgs += (" depcheck: package %s %s-%s needs %s\n") % \
                            (name, version, release, self._formatRequire(reqname, reqversion, flags))
		    
                    elif sense == rpm.RPMDEP_SENSE_CONFLICTS:
                        conferrors += 1
                        msgs += (" depcheck: package %s %s-%s conflicts with %s\n") % \
                            (name, version, release, reqname)
		
                    if self._verbose and suggest:
                        print suggest
		    
            msgs += (" there were %d dependency problem(s) and %d conflict(s)\n") % (deperrors, conferrors)

        if msgs == "":
            return None
        else:
            return msgs
    
    def _formatRequire (self, name, version, flags):
        """ This method formats the given name and version strings
        according to the rpm flags.

        @return: the formatted string
        """
        
        s = name
        
        if flags:
            if flags & (rpm.RPMSENSE_LESS | rpm.RPMSENSE_GREATER |
                        rpm.RPMSENSE_EQUAL):
                s = s + " "
                if flags & rpm.RPMSENSE_LESS:
                    s = s + "<"
                if flags & rpm.RPMSENSE_GREATER:
                    s = s + ">"
                if flags & rpm.RPMSENSE_EQUAL:
                    s = s + "="
                if version:
                    s = "%s %s" %(s, version)
        return s
    
    def handleInstall(self, package, options):
        """ This method handles the installation of the given package.

        @param package: the package to install.
        @param options: options for the installation (not used yet).
        """
        
        if self._verbose:
            print "Add installation of package:", package, "with options:", options

        package, hdr = self._handlePackage(package, options)
        self._ts.addInstall(hdr,(hdr,package), "i")
  
    def handleUpgrade(self, package, options):
        """ This method handles the upgrade of the given package.

        @param package: the package to upgrade.
        @param options: options for the upgrade (not used yet).
        """
                
        if self._verbose:
            print "Add upgrading of package:", package, "with options:", options

        package, hdr = self._handlePackage(package, options)
        self._ts.addInstall(hdr,(hdr,package), "u")

    def handleErase(self, package, options):
        """ This method handles the removal of the given package.

        @param package: the package to erase.
        @param options: options for the removal (not used yet).
        """
        
        if self._verbose:   
            print "Add removal of package:", package, "with options:", options
            
        self._ts.addErase(package)

    def run(self):
        """ This method runs the transaction set.
        If required, it checks and orders it.

        @return: error messages if something wrong happened.
        """
        
        if self._verbose:   
            print "Run transaction set"

        # check for dependencies problems
        if not (self._interface_flags & INSTALL_NODEPS):
            msgs = self._check()
            if msgs:
                raise rpm.error, msgs

        # order if required
        if not(self._interface_flags & INSTALL_NOORDER):
            self._ts.order()        
      	
        # run transaction set and check for problems
        cb = simpleCallback()
        
        if self._verbose:
            errors = self._ts.run(cb.verboseCallback,'')
        else:
            errors = self._ts.run(cb.simpleCallback,'')

        return errors

    def clean(self):
        """ This method cleans the cache directory used by the transaction.
        """

        for file in os.listdir(self._cachedir):
            if self._verbose:
                print "Removing cache file %s" % (self._cachedir + file)
            os.remove(self._cachedir + file)

    def _rpm_version(self):
        """ This method returns the version of rpm package.
        """

        try:
            rpm_ver=rpm.__version__
        except AttributeError:
            ts = rpm.TransactionSet()
            mi = ts.dbMatch( 'name', 'rpm')
            for h in mi:
                rpm_ver = h['version']
        return rpm_ver

   
# Module Test   
if __name__=="__main__":
    t = rpmtTransaction(1, 0, 0, rpm.RPMPROB_FILTER_OLDPACKAGE, rpm._RPMVSF_NOSIGNATURES, revproxylist=['a','b','localhost','c'], proxy_info={"ftp":"http://www.eee.org:91"})

    try:
        #t.handleInstall("rpms/eboard-0.9.0-1.i386.rpm", [])    
        #t.handleUpgrade("rpms/hodie-1.4-2.i386.rpm", [])
        t.handleUpgrade("ftp://ftp.pbone.net/mirror/ftp.sourceforge.net/pub/sourceforge/h/ho/hodie/hodie-1.4-2.i386.rpm", [])
        #t.handleUpgrade("http://localhost/hodie-1.4-2.i386.rpm", [])
        #t.handleUpgrade("http://localhost/big.rpm", [])
        #t.handleUpgrade("rpms/pvpgn-1.6.4-1.fc2.i386.rpm", [])
        #t.handleErase("plife",[])
    except Exception, err:
        print err
        sys.exit(1)

    t.run()

    t.clean()
    
