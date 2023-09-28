*** Settings ***
Library     SeleniumLibrary
Resource    ./varGLOB.robot

*** Variables ***
${BROWSER}              chrome
${NAME}                 Matheus Henrique Santos Eufrasio
${email_confirm}        //div[@id="i5"]
${name_select}          //*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div
${name_select_box}      //*[@id="mG61Hd"]//div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[1]
${name_select_myname}   //*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[24]

${horario_1}            //div[@id="i16"]
${horario_2}            //div[@id="i19"]
${horario_3}            //div[@id="i25"]
${area_estudo}          //div[@id="i47"]
${project}              //div[@id="i85"]
${textarea_atv}         //textarea[@jsname="YPqjbf"]
${button_submit}        //div[@jsname="M2UYVd"]
${ATUALIZAR}            //div[@jsname="LgbsSe"]

${email_validacao}      //*[@id="identifierId"]
${BOTAO_AVANCE1}        //*[@id="identifierNext"]

${INPUT_PASSWORD}       //*[@name="Passwd"]
${BOTAO_AVANCE2}        //*[@id="passwordNext"]

*** Keywords ***
abrir site para teste
    open browser        https://forms.gle/HcQALhH8VNh7gtxG6    ${BROWSER}
fazer login
    input text          ${email_validacao}                      ${EMAIL}
    click element       ${BOTAO_AVANCE1}
    sleep               3s
    input text          ${INPUT_PASSWORD}                       ${PASSWORD}
    click element       ${BOTAO_AVANCE2}
fechar navegador
    close browser
ATUALIZAR
    element should be enabled          ${ATUALIZAR}
    click element                      ${ATUALIZAR}
confirmar email
    wait until element is enabled      ${email_confirm}         10s
    click element                      ${email_confirm}
preencher campos
    click element                      ${name_select}
    sleep                              2s
    mouse over                         ${name_select_box}
    mouse over                         ${name_select_myname}
    click element                      ${name_select_myname}
    sleep                              2s
continuar preenchimento
    click element                      ${horario_1}
    sleep                              2s
    click element                      ${area_estudo}
    sleep                              2s
    click element                      ${project}
    sleep                              2s
    input text                         ${textarea_atv}          ${TEXTO}
clicar em submit
    click element                   ${button_submit}
    sleep                              10s

*** Test Cases ***
Cenário 1: Preencher formulário
    abrir site para teste
    fazer login
    confirmar email
    ATUALIZAR
    preencher campos
    continuar preenchimento
    clicar em submit
    fechar navegador