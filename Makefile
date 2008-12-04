####################################################################
# Distribution Makefile
####################################################################

.PHONY: configure install clean

all: configure

#
# BTDIR needs to point to the location of the build tools
#
BTDIR := ../quattor-build-tools
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

configure: $(COMP) $(RPMPY_SOURCES) $(COMP).pod


####################################################################
# Install
####################################################################

install: configure man
	@echo installing ...
	@mkdir -p $(PREFIX)/$(QTTR_BIN)
	@mkdir -p $(PREFIX)/$(QTTR_MAN)/man$(MANSECT)
	@mkdir -p $(PREFIX)/$(QTTR_DOC)
	@mkdir -p $(PREFIX)/$(QTTR_PYTHLIB)/rpmt
	@mkdir -p $(PREFIX)/$(RPMT_CACHE)
	@install -m 0755 $(COMP) $(PREFIX)/$(QTTR_BIN)/$(COMP)
	@for i in $(RPMPY_SOURCES) ; do \
		install -m 0444 $$i $(PREFIX)/$(QTTR_PYTHLIB)/rpmt/$$i ; \
	done

	@install -m 0444 $(COMP).$(MANSECT).gz \
	                 $(PREFIX)$(QTTR_MAN)/man$(MANSECT)/$(COMP).$(MANSECT).gz
	@for i in MAINTAINER ChangeLog README ; do \
		install -m 0444 $$i $(PREFIX)/$(QTTR_DOC)/$$i ; \
	done

epydoc: configure
	@epydoc -o epydoc *.py

man: configure
	@pod2man $(_podopt) ./$(COMP).pod >$(COMP).$(MANSECT)
	@gzip -f $(COMP).$(MANSECT)

####################################################################


clean::
	@echo cleaning $(NAME) files ...
	@rm -f $(COMP) $(COMP).$(MANSECT).gz
	@rm -f *.pyc *.py
	@rm -rf TEST


