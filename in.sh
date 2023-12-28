#!/bin/bash

# Assumptions:
# 	Using bash
# 	Using Arch Linux
# 	The script is in the root directory
# 	Someone is there to take over incase of anything
# 	Nothing will go wrong
# 	No spaces or any funny characters in file && dir name
# 	No one runs this script in a serious env

# Check if the user wants interactive or non-interactive mode

if [[ "$1" == "-i" ]]; then
	INTERACTIVE=true
else
	INTERACTIVE=false
fi

# The regex to test if the user accepted (yes) or declined (no)
yes_regex="^([yY][eE][sS]|[yY])$" # Yes
no_regex="^([nN][oO]|[nN])$"       # No

# Install the "global" packages in the list file

FILE_NAME="list"

# Check if the user is root (or at least has the necessary permissions)
# This doesn't affect the execution but issues a warning to the user
# Check this comment about permissions (and the whole question by extension)
# https://stackoverflow.com/questions/18215973/how-to-check-if-running-as-root-in-a-bash-script#comment125628861_52586842
# The test can also be "faked" by fakeroot, so let the user run the script
# If the user is not root, append 'sudo' to the commands that require it.

is_root(){ [ "${EUID:-$(id -u)}" -eq 0 ] }

if is_root; then
	PACMAN_INSTALL="pacman -S"
	HOMEBREW_INSTALL="brew install"
else
	PACMAN_INSTALL="sudo pacman -S"
	HOMEBREW_INSTALL="sudo brew install"
fi

# Install the package managers (and update them)

# Update pacman (and syncronize packages)

if is_root; then
	pacman -Syu pacman
else
	sudo pacman -Syu pacman
fi

# Install Homebrew
# Check if the user wants to install homebrew
if $INTERACTIVE; then
	read -rp "Install Homebrew?(yes/no)" ihome
	if [[ $ihome =~ $yes_regex ]]; then
		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	fi
fi

# Check the file that contains the list of programs to be installed
# Check what they are using and install them appropritely

while IFS=, read -r package pkm; do
	# Map the pkm to the appropriate install command
	if [[ $pkm == "homebrew" ]]; then
		INSTALL_PKM=$HOMEBREW_INSTALL
	else 
		if [[ $pkm == "pacman" ]]; then
			INSTALL_PKM=$PACMAN_INSTALL
		fi
	# Incase there is no package manager specified,
	# 	use pacman
	else
		INSTALL_PKM=$PACMAN_INSTALL
	fi
	echo "Installing $package..."
	echo "$INSTALL_PKM $package"
	$INSTALL_PKM $package
done < $FILE_NAME

# Check the folders in in the current directory

DIRECTORIES_P=$(ls -d */)

IFS="/ "

for DIR in $DIRECTORIES_P; do
	# Run the scripts of each folder
done

