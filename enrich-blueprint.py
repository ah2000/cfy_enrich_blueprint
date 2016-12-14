#!/usr/bin/env python

"""
enrich-blueprint
"""

import sys
import optparse
	
class dotdictify(dict):
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError, 'expected dict'
    def __setitem__(self, key, value):
        if '.' in key:
            myKey, restOfKey = key.split('.', 1)
            target = self.setdefault(myKey, dict())
            if not isinstance(target, dict):
                raise KeyError, 'cannot set "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target))
            target[restOfKey] = value
        else:
            if isinstance(value, dotdictify) and not isinstance(value, dict):
                value = dict(value)
            dict.__setitem__(self, key, value)
    def __getitem__(self, key):
        if '.' not in key:
            return dict.__getitem__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dict):
            raise KeyError, 'cannot get "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target))
        return target[restOfKey]
    def __contains__(self, key):
        if '.' not in key:
            return dict.__contains__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dict):
            return False
        return restOfKey in target
    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
        return self[key]
    __setattr__ = __setitem__
    __getattr__ = __getitem__
 
def deep_update(source, overrides):
    """Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.iteritems():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source 
    
    
def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = optparse.OptionParser(
        formatter=optparse.TitledHelpFormatter(width=78),
        add_help_option=None)

    # define options here:
    parser.add_option(      # customized description; put --help last
        '-h', '--help', action='help',
        help='Show this help message and exit.')

    settings, args = parser.parse_args(argv)

    # check number of arguments, verify values, etc.:
    if args:
        parser.error('program takes no command-line arguments; '
                     '"%s" ignored.' % (args,))

    # further process settings & args if necessary

    return settings, args

def load_mappings(configPath=None):
    mappings = {'t2.small':{'inputs':{ 'capabilties.host.properties.num_cpus': 1,'capabilties.host.properties.mem_size': 1  },'output':'aws.properties.instance_type'},\
    't2.medium':{'inputs':{ 'capabilties.host.properties.num_cpus': 4,'capabilties.host.properties.mem_size': 4  },'output': 'aws.properties.instance_type'},\
    't2.large':{'inputs':{ 'capabilties.host.properties.num_cpus': 9999,'capabilties.host.properties.mem_size': 9999  },'output': 'aws.properties.instance_type'},\
    }
    return mappings

def enrich(yamldic,mappingdic):
    #find the sub dictionary for our inputs
    
def main(argv=None):
    settings, args = process_command_line(argv)
	
    maps = load_mappings()
    docs = yaml.load_all(sys.stdin.readlines())
	for doc in docs:
        mappings = load_mappings()
		enrich(doc,mappings)
		print "\n",
    # application code here, like:
    
    # run(settings, args)
    return docs        # success

if __name__ == '__main__':
    status = main()
    sys.exit(status)
    
    
 
 
 {'web_server_host': {'type': 'multicloud.Instance', 'properties': {'azure_properties': {'some_property_to_ignore': 'ignore', 'some_other_property_to_ignore': 'ignore'}}, 'capabilities': {'host': {'some_property_to_ignore': 'ignore', 'properties': {'mem_size': 4, 'num_cpus': 2}, 'some_other_property_to_ignore': 'ignore'}}, 'aws_properties': {'some_property_to_ignore': 'ignore', 'some_other_property_to_ignore': 'ignore'}}}