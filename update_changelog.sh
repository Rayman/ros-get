#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
FILE="$DIR/CHANGELOG.rst"
gitchangelog > "$FILE" && git commit -m "!minor Update changelog" "$FILE"
