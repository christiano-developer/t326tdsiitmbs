#!/usr/bin/env bash
# Decode the q-termlog-rec-server cipher: undo hex, then reversal, then ROT13 (reversal and ROT13 commute).
# Usage (inside the termlog recording):  curl -s "<Q13 URL from the exam page>" | bash decode.sh
#   or:                                  echo <hex string> | bash decode.sh
grep -v '^#' | tr -d ' \n' | xxd -r -p | rev | tr 'A-Za-z' 'N-ZA-Mn-za-m'; echo
