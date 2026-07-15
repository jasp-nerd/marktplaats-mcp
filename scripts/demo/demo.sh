#!/usr/bin/env bash
# Staged Claude Code session replayed for the README demo GIF.
# Rendered by demo.tape (charmbracelet/vhs): vhs scripts/demo/demo.tape
set -euo pipefail

ORANGE=$'\e[38;5;208m'; DIM=$'\e[2m'; BOLD=$'\e[1m'; RESET=$'\e[0m'
GREEN=$'\e[32m'; GRAY=$'\e[38;5;245m'

type_out() {
  local s="$1"
  for ((i = 0; i < ${#s}; i++)); do
    printf '%s' "${s:i:1}"
    sleep 0.03
  done
  printf '\n'
}

printf '%s\n' "${DIM}──────────────────────────────────────────────────────────────────────${RESET}"
printf '%s' "${BOLD}>${RESET} "
sleep 0.6
type_out "find me a used racefiets under €500 within 25 km of Amsterdam"
printf '%s\n' "${DIM}──────────────────────────────────────────────────────────────────────${RESET}"
sleep 0.7

printf '\n%s %s%s\n' "${GREEN}⏺${RESET}" "${BOLD}marktplaats — search_listings ${RESET}" \
  "${GRAY}(query: \"racefiets\", condition: \"used\", price_to: 500,${RESET}"
printf '%s\n' "  ${GRAY} postcode: \"1011 AB\", distance_km: 25)${RESET}"
sleep 1.4
printf '%s\n' "  ${GRAY}⎿ 241 results · 5 organic listings returned · promos filtered${RESET}"
sleep 0.9

printf '\n%s Found solid options under budget:\n\n' "${GREEN}⏺${RESET}"
sleep 0.5
printf '%s\n' "  1. ${BOLD}Triban RC 100, recently serviced${RESET}   ${ORANGE}bidding from € 220${RESET}  ${GRAY}Leiden · 37 km${RESET}"
sleep 0.5
printf '%s\n' "  2. ${BOLD}Giant Contend 2, size M${RESET}            ${ORANGE}€ 375${RESET}               ${GRAY}Haarlem · 19 km${RESET}"
sleep 0.5
printf '%s\n' "  3. ${BOLD}Bianchi Via Nirone 7 (2019)${RESET}        ${ORANGE}€ 495${RESET}               ${GRAY}Amstelveen · 11 km${RESET}"
sleep 0.9

printf '\n%s\n' "  The Giant is the best value: verified seller (bank + phone),"
printf '%s\n' "  4.8★ reviews. Want me to watch for new listings under €400?"
sleep 3
