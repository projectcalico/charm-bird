# Overview

The BIRD project aims to develop a fully functional dynamic IP routing daemon primarily targeted on (but not limited to) Linux, FreeBSD and other UNIX-like systems and distributed under the GNU General Public License.

Currently this charm only supports deploying BIRD as a BGP route reflector. If you would like to deploy BIRD in other roles, please contact the charm maintainer.

For more information, check out the [BIRD homepage](http://bird.network.cz/).

# Usage

To deploy this charm, simply run:

    juju deploy bird

To use a BIRD daemon as a route reflector (e.g. for the open source [Project Calico](http://www.projectcalico.org/)), type the following:

    juju add-relation bird neutron-calico

# Configuration

There are no configuration options for BIRD at this time. If you need some, please contact the maintainer.

# Contact Information

- Find out more on [BIRD website](http://bird.network.cz/).
- Report bugs with this charm on [Launchpad](https://code.launchpad.net/~cory-benfield/calico-charms/bird).

