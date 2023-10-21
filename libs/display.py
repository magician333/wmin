# coding=utf-8

from thirdparty.colorama import Fore, init

init(autoreset=True)


def printf(string, status="blank"):
    """
    printf function
    status default is ordinary
    ordinary == White
    normal == Green
    warning == Yellow
    error == Red
    """

    if "blank" == status:
        print(string)

    elif "ordinary" == status:
        print("[ORDINARY] "+string)

    elif "error" == status:
        print(Fore.RED+"[ERROR] "+string+Fore.RESET)

    elif "warning" == status:
        print(Fore.YELLOW+"[WARNING] "+string+Fore.RESET)

    elif "normal" == status:
        print(Fore.GREEN+"[NORMAL] "+string+Fore.RESET)

    elif "string" == status:
        print(Fore.GREEN+string+Fore.RESET)

    else:
        print(Fore.BLUE+"No "+status+Fore.RESET)


def printweb(code, web):
    code_init = str(code)[0]

    if "1" == code_init:
        print(Fore.LIGHTBLACK_EX+"<"+str(code)+">\t"+web+Fore.RESET)
    if "2" == code_init:
        print(Fore.LIGHTGREEN_EX+"<"+str(code)+">\t"+web+Fore.RESET)
    if "3" == code_init:
        print(Fore.LIGHTCYAN_EX+"<"+str(code)+">\t"+web+Fore.RESET)
    if "4" == code_init:
        print(Fore.LIGHTRED_EX+"<"+str(code)+">\t"+web+Fore.RESET)
    if "5" == code_init:
        print(Fore.LIGHTMAGENTA_EX+"<"+str(code)+">\t"+web+Fore.RESET)
