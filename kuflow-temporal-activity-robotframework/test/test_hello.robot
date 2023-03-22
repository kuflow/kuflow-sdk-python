*** Settings ***
Documentation       Hello Robot Framework Bot


*** Variables ***
${my_var}     _DEFAULT_VALUE_


*** Tasks ***
Test Hello
    Log To Console    My var: ${my_var}

