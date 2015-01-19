from charmhelpers.fetch import apt_install


def pre_install():
    """
    Do any setup required before the install hook.
    """
    install_other_dependencies()


def install_other_dependencies():
    """
    Install our other dependencies, if not present.
    """
    try:
        import netifaces
    except ImportError:
        apt_install('python-netifaces')

    try:
        import netaddr
    except ImportError:
        apt_install('python-netaddr')
