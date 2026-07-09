#!/bin/bash

echo "================================"
echo " Internet Monitor Release"
echo "================================"
echo

read -p "Bitte Versionsnummer eingeben (z.B. 0.2.0): " VERSION

if [ -z "$VERSION" ]; then
    echo
    echo "Fehler: Keine Versionsnummer angegeben."
    exit 1
fi

echo
echo "Folgende Version wird veröffentlicht:"
echo
echo "    $VERSION"
echo

read -p "Fortfahren? (y/n): " CONFIRM

if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo
    echo "Abgebrochen."
    exit 0
fi

git add .

git commit -m "Release $VERSION"

git tag "v$VERSION"

git push origin main
git push origin "v$VERSION"

echo
echo "================================"
echo "Release $VERSION abgeschlossen."
echo "================================"