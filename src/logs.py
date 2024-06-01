class logc:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class log:
    DEBUG = f"{logc.OKGREEN}{logc.BOLD}DEBUG{logc.ENDC} -"
    INFO = f"{logc.OKBLUE}{logc.BOLD}INFO{logc.ENDC} -"
    WARN = f"{logc.WARNING}{logc.BOLD}WARN{logc.ENDC} -"
    ERROR = f"{logc.FAIL}{logc.BOLD}ERROR{logc.ENDC} -"
    CRIT = f"{logc.FAIL}{logc.BOLD}CRITICAL{logc.ENDC} -"
    SUM = f"{logc.OKCYAN}{logc.BOLD}SUMMARY{logc.ENDC} -"