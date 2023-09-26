*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${variavel1}    teste
${BROWSER}      firefox

*** Keywords ***


*** Test Cases ***
Cenário 1: Teste de abrir navegador
    Open browser    https://www.youtube.com/watch?v=gyHlGC_ag1o&list=PL5ipcSFH2tk8RWxtvuaOK-qpdAvlWkSoo&index=4     ${BROWSER}