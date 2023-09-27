*** Settings ***
Library     SeleniumLibrary

*** Variables ***
${BROWSER}      chrome
${input_first_name}     name:firstname
${input_last_name}      name:lastname
${input_sex}            id:sex-0
${input_years}          id:exp-0
${input_date}           id:datepicker
${input_profession}     id:profession-1
${input_tools}          id:tool-2
${input_continents}     name:continents
${input_selenium}       id:selenium_commands
${button_submit}        name:submit

*** Keywords ***
abrir site para teste
    open browser    https://www.techlistic.com/p/selenium-practice-form.html    ${BROWSER}
fechar navegador
    close browser
preencher campos
    input text                         ${input_first_name}      Matheus
    input text                         ${input_last_name}       Henrique
    click element                      ${input_sex}
    click element                      ${input_years}
    input text                         ${input_date}            11/07/1997
    click element                      ${input_profession}
    click element                      ${input_tools}
    select from list by index          ${input_continents}      1
    select from list by index          ${input_selenium}        1

clicar em submit
    sleep           15s
    click button    ${button_submit}

*** Test Cases ***
Cenário 1: Preencher formulário
    abrir site para teste
    preencher campos
    clicar em submit
    fechar navegador