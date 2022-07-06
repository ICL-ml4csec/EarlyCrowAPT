import re

def IoC_parser(_FILENAME):
    DOMAIN = 'domain\t(.*)'
    IP = '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'


    domain = re.compile(
        r'{}'.format(
            DOMAIN), re.IGNORECASE)

    ip = re.compile(
        r'{}'.format(
            IP), re.IGNORECASE)

    with open(_FILENAME, 'r', encoding='utf-8') as IoC:
        IoC = IoC.read()
        results_domain = domain.findall(IoC)
        results_ip = ip.findall(IoC)

    # Drop duplicate just in case
    results_domain = list(dict.fromkeys(results_domain))
    results_ip = list(dict.fromkeys(results_ip))
    return results_domain, results_ip



