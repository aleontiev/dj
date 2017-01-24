INSTALL_DIR := .dj

install: $(INSTALL_DIR)/bin/activate

$(INSTALL_DIR)/bin/activate: requirements.txt requirements.txt.dev setup.py
	@test -d $(INSTALL_DIR) || virtualenv $(INSTALL_DIR)
	@. $(INSTALL_DIR)/bin/activate; pip install -U pip setuptools
	@. $(INSTALL_DIR)/bin/activate; pip install -U -r requirements.txt
	@. $(INSTALL_DIR)/bin/activate; python setup.py develop
	@touch $(INSTALL_DIR)/bin/activate

test: install
	@. $(INSTALL_DIR)/bin/activate; pytest tests

clean:
	rm -rf dist/ build/

clean-all: clean
	rm -rf $(INSTALL_DIR)

distribute: clean-all install
	. $(INSTALL_DIR)/bin/activate; pip install pyinstaller
	. $(INSTALL_DIR)/bin/activate; pyinstaller dj.exe.spec
	ln -sf $(CURDIR)/dist/dj.exe/dj.exe /usr/local/bin/dj
