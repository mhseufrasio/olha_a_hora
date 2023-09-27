*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${BROWSER}      chrome

*** Keywords ***
abrir site do google
    Open browser    https://www.google.com     ${BROWSER}
fechar navegador
    Close browser

*** Test Cases ***
Cenário 1: Teste de abrir navegador
    Open browser    https://www.youtube.com/watch?v=gyHlGC_ag1o&list=PL5ipcSFH2tk8RWxtvuaOK-qpdAvlWkSoo&index=4     ${BROWSER}
    Close browser
Cenário 2: Teste de abrir site do google
    abrir site do google
    fechar navegador