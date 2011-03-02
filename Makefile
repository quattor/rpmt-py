####################################################################
# Distribution Makefile
####################################################################

.PHONY: configure install clean

all: configure selinux

#
# BTDIR needs to point to the location of the build tools
#
BTDIR := quattor-build-tools
#
#
_btincl   := $(shell ls $(BTDIR)/quattor-buildtools.mk 2>/dev/null || \
             echo quattor-buildtools.mk)
include $(_btincl)


####################################################################
# Configure
####################################################################


RPMPY_SOURCES = rpmt_ActionsSet.py rpmt_OptionParser.py \
                rpmt_Transaction.py generic_OptionParser.py

SELINUX_DIR = /usr/share/selinux/targeted/

SELINUX_FILES = selinux/rpmt-py.te selinux/rpmt-py.context

configure: $(COMP) $(RPMPY_SOURCES) $(COMP).pod  $(SELINUX_FILES)


####################################################################
# Install
####################################################################

install: configure man selinux
	@echo installing ...
	@mkdir -p $(PREFIX)/$(QTTR_BIN)
	@mkdir -p $(PREFIX)/$(QTTR_MAN)/man$(MANSECT)
	@mkdir -p $(PREFIX)/$(QTTR_DOC)
	@mkdir -p $(PREFIX)/$(QTTR_PYTHLIB)/rpmt
	@mkdir -p $(PREFIX)/$(RPMT_CACHE)
	@mkdir -p $(PREFIX)$(SELINUX_DIR)
	@install -m 0755 $(COMP) $(PREFIX)/$(QTTR_BIN)/$(COMP)
	@for i in $(RPMPY_SOURCES) ; do \
		install -m 0444 $$i $(PREFIX)/$(QTTR_PYTHLIB)/rpmt/$$i ; \
	done

	@install -m 0444 $(COMP).$(MANSECT).gz \
	                 $(PREFIX)$(QTTR_MAN)/man$(MANSECT)/$(COMP).$(MANSECT).gz
	@for i in MAINTAINER ChangeLog README ; do \
		install -m 0444 $$i $(PREFIX)/$(QTTR_DOC)/$$i ; \
	done

	@install -m 0444 rpmt-py.pp $(PREFIX)/$(SELINUX_DIR)

epydoc: configure
	@epydoc -o epydoc *.py

man: configure
	@pod2man $(_podopt) ./$(COMP).pod >$(COMP).$(MANSECT)
	@gzip -f $(COMP).$(MANSECT)

selinux: rpmt-py.pp

rpmt-py.pp: selinux/
	@checkmodule -M -m selinux/rpmt-py.te -o tmp
	@semodule_package -o rpmt-py.pp -m tmp -f selinux/rpmt-py.context

####################################################################


clean::
	@echo cleaning $(NAME) files ...
	@rm -f $(COMP) $(COMP).$(MANSECT).gz
	@rm -f *.pyc *.py
	@rm -rf TEST
	@rm -rf *pp tmp
	@rm -rf $(SELINUX_FILES)
