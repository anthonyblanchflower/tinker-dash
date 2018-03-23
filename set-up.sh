#! /bin/bash

if [ $# -ne 1 ]; then
	echo "Which OS are you setting up for?
Options are:
--> mac
--> tinker
Please type answer:"

	read OS
else
	OS=$1
fi

if [ "$OS" == "tinker" ]; then
	echo "Setting up geckodriver for tinker OS"
	echo https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-arm7hf.tar.gz
	wget https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-arm7hf.tar.gz -O ./geckodriver-macos.tar.gz
	gunzip geckodriver-macos.tar.gz
	tar -xf geckodriver-macos.tar
	sudo mv geckodriver /usr/bin/
elif [ "$OS" == "mac" ]; then
	echo "Setting up geckodriver for Mac OS"
	echo https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-macos.tar.gz
	rm -f ~/Downloads/geckodriver-macos.tar*
	wget https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-macos.tar.gz -O ~/Downloads/geckodriver-macos.tar.gz
	pushd ~/Downloads
	gunzip geckodriver-macos.tar.gz
	tar -xf geckodriver-macos.tar
	sudo mv geckodriver /usr/bin/
	popd
else
	echo "OS $OS is not supported"
fi
