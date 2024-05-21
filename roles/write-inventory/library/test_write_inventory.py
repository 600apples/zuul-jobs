# Copyright (C) 2018 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import testtools
import fixtures
import os

import yaml

from .write_inventory import run

INPUT = yaml.safe_load("""
bionic:
  ansible_connection: ssh
  ansible_host: 104.130.217.77
  ansible_port: 22
  ansible_user: zuul
  nodepool:
    az: null
    cloud: rax
    interface_ip: 104.130.217.77
    label: ubuntu-bionic
    private_ipv4: 10.210.196.115
    provider: rax-ord
    public_ipv4: 104.130.217.77
    region: ORD
xenial:
  ansible_connection: ssh
  ansible_host: 149.202.170.85
  ansible_port: 22
  ansible_user: zuul
  nodepool:
    az: nova
    cloud: ovh
    interface_ip: 149.202.170.85
    label: ubuntu-xenial
    private_ipv4: 149.202.170.85
    provider: ovh-gra1
    public_ipv6: 2001:41d0:302:1000::17:a32b
    region: GRA1
""")

GROUPS_INPUT = yaml.safe_load("""
all: []
ungrouped: []
puppet:
  - bionic
  - xenial
""")


class TestWriteInventory(testtools.TestCase):
    def assertOutput(self, dest, ref):
        with open(dest) as f:
            out = yaml.safe_load(f)
        self.assertEqual(ref, out)

    def test_all(self):
        '''Test passing all variables'''
        dest = self.useFixture(fixtures.TempDir()).path
        dest = os.path.join(dest, 'out.yaml')
        run(dest, INPUT, GROUPS_INPUT, None, None, None, None)

        self.assertOutput(dest, {
            'all': {
                'children': {
                    'puppet': {
                        'hosts': {
                            'bionic': None,
                            'xenial': None,
                        },
                    },
                },
                'hosts': {
                    'bionic': {
                        "ansible_connection": "ssh",
                        "ansible_user": "zuul",
                        "ansible_host": "104.130.217.77",
                        "ansible_port": 22
                    },
                    'xenial': {
                        "ansible_connection": "ssh",
                        "ansible_user": "zuul",
                        "ansible_host": "149.202.170.85",
                        "ansible_port": 22,
                    }
                }
            }
        })

    def test_include(self):
        '''Test incuding vars'''
        dest = self.useFixture(fixtures.TempDir()).path
        dest = os.path.join(dest, 'out.yaml')
        run(dest, INPUT, GROUPS_INPUT, ['ansible_host'], None, None, None)

        self.assertOutput(dest, {
            'all': {
                'children': {
                    'puppet': {
                        'hosts': {
                            'bionic': None,
                            'xenial': None,
                        },
                    },
                },
                'hosts': {
                    'bionic': {
                        "ansible_host": "104.130.217.77",
                    },
                    'xenial': {
                        "ansible_host": "149.202.170.85",
                    }
                }
            }
        })

    def test_exclude(self):
        '''Test passing all variables'''
        dest = self.useFixture(fixtures.TempDir()).path
        dest = os.path.join(dest, 'out.yaml')
        run(dest, INPUT, GROUPS_INPUT, None, ['ansible_user'], None, None)

        self.assertOutput(dest, {
            'all': {
                'children': {
                    'puppet': {
                        'hosts': {
                            'bionic': None,
                            'xenial': None,
                        },
                    },
                },
                'hosts': {
                    'bionic': {
                        "ansible_connection": "ssh",
                        "ansible_host": "104.130.217.77",
                        "ansible_port": 22
                    },
                    'xenial': {
                        "ansible_connection": "ssh",
                        "ansible_host": "149.202.170.85",
                        "ansible_port": 22,
                    }
                }
            }
        })

    def test_additional(self):
        '''Test passing additional variables'''
        dest = self.useFixture(fixtures.TempDir()).path
        dest = os.path.join(dest, 'out.yaml')
        run(dest, INPUT, GROUPS_INPUT, None, None,
            {'public_v4': 'nodepool.public_ipv4',
             'public_v6': 'nodepool.public_ipv6',
            },
            None)

        self.assertOutput(dest, {
            'all': {
                'children': {
                    'puppet': {
                        'hosts': {
                            'bionic': None,
                            'xenial': None,
                        },
                    },
                },
                'hosts': {
                    'bionic': {
                        "ansible_connection": "ssh",
                        "ansible_user": "zuul",
                        "ansible_host": "104.130.217.77",
                        "ansible_port": 22,
                        "public_v4": "104.130.217.77",
                    },
                    'xenial': {
                        "ansible_connection": "ssh",
                        "ansible_user": "zuul",
                        "ansible_host": "149.202.170.85",
                        "ansible_port": 22,
                        "public_v6": "2001:41d0:302:1000::17:a32b",
                    }
                }
            }
        })

    def test_per_host(self):
        '''Test passing additional variables per host'''
        dest = self.useFixture(fixtures.TempDir()).path
        dest = os.path.join(dest, 'out.yaml')
        run(dest, INPUT, GROUPS_INPUT, None, None,
            {
                'public_v4': 'nodepool.public_ipv4',
                'public_v6': 'nodepool.public_ipv6',
            },
            {
                'bionic': {
                    'a': 'extra',
                    'b': 'variable',
                },
                'xenial': {
                    'c': 'extra',
                    'd': 'variable',
                },
            })

        self.assertOutput(dest, {
            'all': {
                'children': {
                    'puppet': {
                        'hosts': {
                            'bionic': None,
                            'xenial': None,
                        },
                    },
                },
                'hosts': {
                    'bionic': {
                        "ansible_connection": "ssh",
                        "ansible_user": "zuul",
                        "ansible_host": "104.130.217.77",
                        "ansible_port": 22,
                        "public_v4": "104.130.217.77",
                        "a": "extra",
                        "b": "variable"
                    },
                    'xenial': {
                        "ansible_connection": "ssh",
                        "ansible_user": "zuul",
                        "ansible_host": "149.202.170.85",
                        "ansible_port": 22,
                        "public_v6": "2001:41d0:302:1000::17:a32b",
                        "c": "extra",
                        "d": "variable"
                    }
                }
            }
        })
