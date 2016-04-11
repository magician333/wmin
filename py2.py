from colorama import Fore

def printf(string,status = "blank"):
    
    """
    printf function\n
    status default is ordinary
    ordinary == White
    normal == Green
    warning == Yellow
    error == Red
    """
    if "blank" == status:
        print string
    elif "ordinary" == status:
        print "[Ordinary] "+string

    elif "error" == status:
        print Fore.RED+"[Error] "+string+Fore.RESET

    elif "warning" == status:
        print Fore.YELLOW+"[Warning] "+string+Fore.RESET

    elif "normal" == status:
        print Fore.GREEN+"[Normal] "+string+Fore.RESET
    else:
        print Fore.BLUE+"No "+status+Fore.RESET
