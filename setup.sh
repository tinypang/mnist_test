#!/bin/sh

set -e

REMOTE_REPO=~suits/pub/dotfiles-v2
LOCAL_REPO=~/.dotfiles
SOURCE_BRANCH=suits
TARGET_BRANCH=$USER

if [ "$TARGET_BRANCH" = suits ]; then
#    echo "This script doesn't really work for the suits user."
    echo "Target branch $TARGET_BRANCH would be the same as source branch $SOURCE_BRANCH."
    echo "Using TARGET_BRANCH=suits-user instead."
    TARGET_BRANCH=suits-user
#    exit 2
fi

# if you change this, please fix it in the debug output below as well
BACKUP=~/oldsettings

S="0 0"

TMPFILE=`mktemp`

on_exit () {
    rm -f "$TMPFILE"
}
trap on_exit EXIT

# gather information from the user

guess_name () {
    getent passwd "$USER" |
    cut -f5 -d: |
    sed -r 's/(.*); ([^ ]*) .*/\2 \1/'
}

guess_email () {
    echo "$USER@uni.sydney.edu.au"
}

dialog \
    --msgbox "\
SUITS dotfiles setup script
---------------------------

This script will install or upgrade your dotfiles to the new SUITS dotfiles.
This is a one-time operation, as the default dotfiles setup will auto-upgrade
every so often, keeping your account up-to-date with all the latest goodies.

If you already have some dotfiles in your home folder, the script will
automatically create a folder called oldsettings in your home directory
($BACKUP) and move any conflicting files into there.

If you do not wish to install the SUITS dotfiles now, please press Escape or
Control-C now.

Before we install the dotfiles, we need to know your name and email, so that
various programs (most obviously, version control systems like git and
mercurial) will know who you are.

For your email, you should use your primary email address, the one which you
expect to still have in many years time.
" $S

dialog \
    --inputbox "Please enter your name:" $S "`guess_name`" \
    --inputbox "Please enter your primary email address:" $S "`guess_email`" \
2> $TMPFILE

name=$(cut -f1 "$TMPFILE")
email=$(cut -f2 "$TMPFILE")
echo $name
echo $email

# actually do the migration

on_error () {
    cat <<EOF
Migration failed!
echo "Warning: do not log out. You may not be able to log back "
echo "in again if you do. Your setup is possibly in an "
echo "inconsistent state. Please grab the nearest Unix guru "
echo "(your tutor perhaps?) and ask for help."
EOF
    exit 2
}

trap on_error ERR

echo 'Making personal copy of the SUITS dotfiles repository:'
hg clone "$REMOTE_REPO" "$LOCAL_REPO"

cd $LOCAL_REPO

# branch from suits -> user1234
hg up "$SOURCE_BRANCH"
hg branch "$TARGET_BRANCH"

sed -i "
s/#export NAME=.*/export NAME='$name'/
s/#export EMAIL=.*/export EMAIL='$email'/
" .shell/login

hg ci \
    --config "ui.username=$name <$email>" \
    -m "New branch for user $USER (SUITS setup script)."

# for every file which exists
echo "Moving existing files out of the way."
if [ ! -d "$BACKUP" ]; then
    mkdir "$BACKUP"
fi

(
    IFS=
    while read line
    do
        existing=~/$line
        backup=$BACKUP/$line
        if [ -e "$existing" ]; then
            echo "Moving ~/$line -> ~/oldsettings/$line"
            mkdir -p `dirname "$backup"`
            mv -b "$existing" "$backup"
        fi
    done
) <<EOF
$(
    find ! -type d |\
        sed -n 's!^\./!!p' |\
        grep -v -f .dotfiles-ignore
)
EOF

rmdir --ignore-fail-on-non-empty "$BACKUP"

echo 'Installing new dotfiles:'
python install.py

