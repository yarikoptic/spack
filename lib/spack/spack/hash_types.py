# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Definitions that control how Spack creates Spec hashes."""

import spack.dependency as dp

hashes = []


class SpecHashDescriptor(object):
    """This class defines how hashes are generated on Spec objects.

    Spec hashes in Spack are generated from a serialized JSON representation of the DAG.
    The representation may only include certain dependency types, and it may optionally
    include a canonicalized hash of the ``package.py`` for each node in the graph.

    """

    def __init__(self, deptype, package_hash, name):
        self.deptype = dp.canonical_deptype(deptype)
        self.package_hash = package_hash
        self.name = name
        hashes.append(self)

    @property
    def attr(self):
        """Private attribute stored on spec"""
        return "_" + self.name

    def __call__(self, spec):
        """Run this hash on the provided spec."""
        return spec.spec_hash(self)


#: Spack's deployment hash. Includes all inputs that can affect how a package is built.
dag_hash = SpecHashDescriptor(deptype=("build", "link", "run"), package_hash=True, name="hash")


#: Hash descriptor used only to transfer a DAG, as is, across processes
process_hash = SpecHashDescriptor(
    deptype=("build", "link", "run", "test"), package_hash=True, name="process_hash"
)


# Deprecated hash types, no longer used, but needed to understand old serialized
# spec formats

full_hash = SpecHashDescriptor(
    deptype=("build", "link", "run"), package_hash=True, name="full_hash"
)


build_hash = SpecHashDescriptor(
    deptype=("build", "link", "run"), package_hash=False, name="build_hash"
)
