INSTALL_DIR := .v

$(INSTALL_DIR)/bin/activate: requirements.txt install_requires.txt
	@test -d $(INSTALL_DIR) || virtualenv $(INSTALL_DIR)
	@. $(INSTALL_DIR)/bin/activate; pip install -U pip
	@. $(INSTALL_DIR)/bin/activate; pip install -U -r requirements.txt
	@touch $(INSTALL_DIR)/bin/activate

install: $(INSTALL_DIR)/bin/activate
	@. $(INSTALL_DIR)/bin/activate; python setup.py install

distribute: clean-all install
	@. $(INSTALL_DIR)/bin/activate; pip install pyinstaller
	@. $(INSTALL_DIR)/bin/activate; pyinstaller dj.spec

test: install
	@. $(INSTALL_DIR)/bin/activate; py.test tests

clean:
	rm -rf dist/ build/ $(INSTALL_DIR)

clean-all: clean
	rm -rf $(INSTALL_DIR)
