*** Settings ***
Library     SeleniumLibrary
Resource    ./varGLOB.robot

*** Variables ***
${BROWSER}              chrome
${NAME}                 Matheus Henrique Santos Eufrasio
${email_confirm}        //div[@id="i5"]
${name_select}          //span[@class="vRMGwf oJeWuf"]
${horario_1}            //div[@id="i16"]
${horario_2}            //div[@id="i19"]
${horario_3}            //div[@id="i25"]
${area_estudo}          //div[@id="i47"]
${project}              //div[@id="i85"]
${textarea_atv}         //textarea[@jsname="YPqjbf"]
${button_submit}        //div[@jsname="M2UYVd"]

${email_validacao}      //*[@id="identifierId"]
${BOTAO_AVANCE1}        //*[@id="identifierNext"]

${INPUT_PASSWORD}       //*[@id="password"]
${BOTAO_AVANCE2}        //*[@id="passwordNext"]

*** Keywords ***
abrir site para teste
    open browser        https://forms.gle/HcQALhH8VNh7gtxG6    ${BROWSER}
fazer login
    input text          ${email_validacao}                      ${EMAIL}
    click element       ${BOTAO_AVANCE1}
    sleep               5s
    click element       ${INPUT_PASSWORD}
    input password      ${INPUT_PASSWORD}                       ${PASSWORD}
    click element       ${BOTAO_AVANCE2}
fechar navegador
    close browser
preencher campos
    click element                      ${email_confirm}
    select from list by label          ${name_select}           ${NAME}
    click element                      ${horario_1}
    click element                      ${area_estudo}
    click element                      ${project}
    input text                         ${textarea_atv}          ${TEXTO}

clicar em submit
    click button    ${button_submit}
    sleep           15s

*** Test Cases ***
Cenário 1: Preencher formulário
    abrir site para teste
    fazer login
    preencher campos
    clicar em submit
    fechar navegador