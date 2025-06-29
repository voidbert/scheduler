PYTHON_SOURCE_DIR := ../scheduler
DOCS_SOURCE_DIR   := source
DOCS_BUILD_DIR    := build

PYTHON_SOURCE_FILES := $(shell find $(PYTHON_SOURCE_DIR) -type f -name '*.py')

$(DOCS_BUILD_DIR): $(PYTHON_SOURCE_FILES) conf.py index.rst Makefile
	mkdir -p $(DOCS_BUILD_DIR)/_static
	sphinx-apidoc -d 1 --no-toc --separate -e -o $(DOCS_SOURCE_DIR) $(PYTHON_SOURCE_DIR)
	cp custom.css $(DOCS_BUILD_DIR)/_static
	sphinx-build . $(DOCS_BUILD_DIR)
	touch $(DOCS_BUILD_DIR)

.PHONY: clean
clean:
	rm -r $(DOCS_SOURCE_DIR) $(DOCS_BUILD_DIR) 2>/dev/null ||:
