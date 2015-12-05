from collections import namedtuple
import inspect
from inspect import getfullargspec

def update_args(func, args, kwargs, update):
    ret = (
        inspect.getfullargspec(func))

    arg_names = ret[0]
    args = list(args)
    
    for i, (name, val) in enumerate(zip(arg_names, args)):
        if name in update:
            args[i] = update[name]
            del update[name]
    
    kwargs.update(update)
        
    return args, kwargs

Demander = namedtuple('Demander', ['feature', 'inst_feature', 'args', 'kwargs'])

class DependencyScope:
    
    def __init__(self):
        self.providers = {}
    
    def __setitem__(self, feature, provider):
        scope, base = split_feature(feature)
        
        if scope:
            self[scope][base] = provider
        else:
            if base.isnumeric():
                base = int(base)

            self.providers[base] = provider

    def __delitem__(self, feature):
        scope, base = split_feature(feature)
        
        if scope:
            del self[scope][base]
        else:
            if base.isnumeric():
                base = int(base)

            del self.providers[base]

    def __getitem__(self, feature):
        scope, base = split_feature(feature)
        try:
            if scope:
                return self[scope][base]
            else:
                if base.isnumeric():
                    base = int(base)

                return self.providers[base]

        except KeyError:
            raise KeyError("Unknown feature named {0}".format(feature))

    def __contains__(self, feature):
        try:
            _ = self[feature]
            return True
        except KeyError:
            return False
        

def anonymous(feature):
    return feature[-1] == '.'

def split_feature(feature):
    if isinstance(feature, int):
        return '', feature
    else:
        segments = feature.rpartition('.')
        
        if segments[-1]:
            return segments[0], segments[-1]
        else:
            if segments[1]:
                return segments[0], ''
            else:
                return '', segments[0]


def feature_base(feature):
    return split_feature(feature)[1]

def feature_scope(feature):
    return split_feature(feature)[0]

class DependencyContainer(DependencyScope):
    
    def __init__(self, allowReplace=False):
        DependencyScope.__init__(self)
        self.demanders = []
        self.allowReplace = allowReplace

    def create_scope(self, feature):
        self[feature] = DependencyScope()
    
    def provide(self, feature, provider):
        if not self.allowReplace:
            assert not (feature in self.providers), "Duplicate feature: %r" % feature

        feature_ext = feature

        if anonymous(feature):
            feature_ext += str(id(provider))
            
        if feature_ext[0] == '.':
            feature_ext = feature_ext[1:]

        self[feature_ext] = provider
        
        for d in self.demanders:
            if (d.feature == feature) or (d.inst_feature == feature):
                continue

            if anonymous(d.inst_feature) or (d.inst_feature not in self):
                demander = self[d.feature]
            
                _, _, _, _, _, _, annotations = getfullargspec(demander)
                
                dependencies = {}
                for name, a in annotations.items():
                    if isinstance(a, Dependency):
                        dependency = None
                        if (not anonymous(a.feature)) and (a.feature in self):
                            dependency = self[a.feature]
                        elif anonymous(a.feature) and feature_scope(a.feature) == feature_scope(feature):
                            dependency = provider
                        
                        if dependency:
                            dependencies[name] = dependency
                            if not a.assertion(dependencies[name]):
                                break
                        else:
                            break

                else:
                    args, kwargs = update_args(demander, d.args, d.kwargs, dependencies)
                    demander_inst = demander(*args, **kwargs)
                    demander_inst._dependents = {}
                    demander_inst_feature = self.provide(d.inst_feature, demander_inst)

                    for _, dep_provider in dependencies.items():
                        if not hasattr(dep_provider, '_dependents'):
                            dep_provider._dependents = {}
                            
                        dep_provider._dependents[demander_inst_feature] = demander_inst
                        
                    
                    
        return feature_ext
    
    def unprovide(self, feature):
        provider = self[feature]
        if hasattr(provider, '_dependents'):
            for d in provider._dependents:
                self.unprovide(d)
                
        del self[feature]
    
    def create_on_demand(self, feature, inst_feature=None, args=(), kwargs={}):
        self.demanders.append(Demander(feature, inst_feature, list(args), dict(kwargs)))

ddic = DependencyContainer()

def NoAssertion(obj): return True

class RequiredFeature(object):
    def __init__(self, feature, assertion=NoAssertion):
        self.feature = feature
        self.assertion = assertion
    def __get__(self, obj, T):
        return self.result # <-- will request the feature upon first call
    def __getattr__(self, name):
        assert name == 'result', "Unexpected attribute request other then 'result'"
        self.result = self.Request()
        return self.result
    def Request(self):
        obj = ddic[self.feature]
        assert self.assertion(obj), \
                 "The value %r of %r does not match the specified criteria" \
                 % (obj, self.feature)
        return obj

class CreationFeature(object):
    def __init__(self, feature=None, feature_scope='', assertion=NoAssertion):
        self.feature = feature
        self.assertion = assertion
        ddic.register_creation_dependency(self)
    def __get__(self, obj, T):
        return self.result # <-- will request the feature upon first call
    def __getattr__(self, name):
        assert name == 'result', "Unexpected attribute request other then 'result'"
        self.result = self.Request()
        return self.result
    def Request(self):
        obj = ddic[self.feature]
        assert self.assertion(obj), \
                 "The value %r of %r does not match the specified criteria" \
                 % (obj, self.feature)
        return obj

Dependency = namedtuple('Dependency', ['feature', 'scope', 'assertion'])
Dependency.__new__.__defaults__ = (None, None, NoAssertion)
    
class Test:
    def __init__(self, a, b: Dependency(feature='scope.'), c: Dependency(feature='mark')):
        self.b = b
        self.c = c
 
class Test1:
    def __init__(self, a, b: Dependency(feature='scope.'), c: Dependency(feature='scope.subscope.')):
        self.b = b
        self.c = c
 
     
class Mark:
    pass
 
def bla():
    pass    
 
ddic.provide('test', Test)
ddic.create_on_demand('test', '.', args=(1,))
 
ddic.provide('mark', Mark)
ddic.create_scope('scope')
ddic.provide('scope.test1', Test1)
ddic.create_on_demand('scope.test1', 'scope.subscope.Test1', args=(1,))
 
ddic.create_scope('scope.subscope')
ddic.provide('scope.', bla)
ddic.provide('scope.subscope.', bla)

ddic.unprovide('scope.' + str(id(bla)))
 
pass
