rrsync
===
# What is rrsync?
rrsync is a tool using rsync to synchronized your project to remote.

# Install
```
python3 ./setup.py install
```

# How to use it?
```
$rrsync --help
Usage: rrsync [OPTIONS]

Options:
  --local-path TEXT           set the local path, default path will be
                              your current directory
  --observer-timeout INTEGER  The observer timeout, default 1
  --rsync-options TEXT        rsync command options
  --modify_config             modify rsync config
  --help                      Show this message and exit.
```

# python version
use python3 please
