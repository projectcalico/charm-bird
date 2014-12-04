def pre_install():
    """
    Do any setup required before the install hook.
    """
    install_charmhelpers()
    install_other_dependencies()


def install_charmhelpers():
    """
    Install the charmhelpers library, if not present.
    """
    try:
        import charmhelpers  # noqa
    except ImportError:
        import subprocess
        subprocess.check_call(['apt-get', 'install', '-y', 'python-pip'])
        subprocess.check_call(['pip', 'install', 'charmhelpers'])

def install_other_dependencies():
    """
    Install our other dependencies, if not present.
    """
    try:
        import netifaces
    except ImportError:
        import subprocess
        subprocess.check_call(['apt-get', 'install', '-y', 'python-pip', 'python-dev'])
        subprocess.check_call(['pip', 'install', 'netifaces'])

    try:
        import netaddr
    except ImportError:
        import subprocess
        subprocess.check_call(['apt-get', 'install', '-y', 'python-pip'])
        subprocess.check_call(['pip', 'install', 'netaddr'])
