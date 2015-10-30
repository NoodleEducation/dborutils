# dborutils

Code shared among multiple Noodle repositories


## Installation

See docker/README.md in the build repo.  dborutils is imported as a
dependency in other repos; no explicit setup is required.


## Tests

In build/docker:

fig run dborutils bash -c "./reset_environment.sh"
fig run dborutils bash -c "./run_tests.sh"
