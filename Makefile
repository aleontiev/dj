distribute: clean
	virtualenv .v
	. .v/bin/activate; pip install -r requirements.txt
	. .v/bin/activate; pip install pyinstaller
	. .v/bin/activate; pyinstaller django-cli.spec

clean:
	rm -rf dist/ build/ .v/
