# coding=utf-8

from thirdparty.colorama import Fore, init

init(autoreset=True)


COLORS = {
    "blank": "",
    "ordinary": "[ORDINARY] {}",
    "error": f"{Fore.RED}[ERROR] {{}}{Fore.RESET}",
    "warning": f"{Fore.YELLOW}[WARNING] {{}}{Fore.RESET}",
    "normal": f"{Fore.GREEN}[NORMAL] {{}}{Fore.RESET}",
    "string": f"{Fore.GREEN}{{}}{Fore.RESET}",
}


def printf(string, status="blank"):
    """
    printf function
    status default is blank
    """

    format_string = COLORS.get(status, f"{Fore.BLUE}No {status}{Fore.RESET}")
    print(format_string.format(string))


SCAN_COLORS = {
    "1": Fore.LIGHTBLACK_EX,
    "2": Fore.LIGHTGREEN_EX,
    "3": Fore.LIGHTCYAN_EX,
    "4": Fore.LIGHTRED_EX,
    "5": Fore.LIGHTMAGENTA_EX,
}


def print_scanned_url(code, url):
    code_init = str(code)[0]

    color = SCAN_COLORS.get(code_init, "")
    print(f"{color}<{code}>\t{url}{Fore.RESET}")
