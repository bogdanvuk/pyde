from collections import namedtuple
import inspect
from inspect import getfullargspec
from weakref import WeakValueDictionary

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

class Demander:
    
    def __init__(self, feature, inst_feature, args, kwargs):
        self.feature = feature
        self.inst_feature = inst_feature
        self.args = args
        self.kwargs = kwargs
        self.dependencies = {}
        self.dependencies_by_feature = {}
        self.satisfied = WeakValueDictionary()
        self.provider = None
        
        if self.extract_dependencies():
            for d in self.dependencies:
                if d in ddic:
                    self.satisfied_on_feature_provided(d, ddic[d])
                        
    def all_satisfied(self):
        return len(self.satisfied) == len(self.dependencies)
    
    def extract_dependencies(self):
        if self.dependencies:
            return True
        elif self.feature not in ddic:
            return False
        else:
            self.provider = ddic[self.feature]
            _, _, _, _, _, _, annotations = getfullargspec(self.provider)
                
            self.dependencies = {}
            for name, a in annotations.items():
                if isinstance(a, Dependency):
                    self.dependencies[name] = a
                    self.dependencies_by_feature[a.feature] = a

    def satisfied_on_feature_provided(self, feature, provider):
        if self.extract_dependencies():
            if feature in self.satisfied:
                del self.satisfied[feature]

            if feature in self.dependencies_by_feature:
                if self.dependencies_by_feature[feature].assertion(provider):
                    self.satisfied[feature] = provider
                    
                return self.all_satisfied()
            elif (feature_scope(feature) + '/') in self.dependencies_by_feature:
                if self.dependencies_by_feature[feature_scope(feature) + '/'].assertion(provider):
                    self.satisfied[feature_scope(feature) + '/'] = provider
                    return self.all_satisfied()

        return False
                
# Demander = namedtuple('Demander', ['feature', 'inst_feature', 'args', 'kwargs'])
# Demander.__new__.__defaults__ = (None, None, (), {})

sep = '/'

class DependencyScope:
    
    def __init__(self, name, parent):
        self.providers = {}
        self.parent = parent
        self.name = name

    def provide(self, feature, provider):
        self.parent.provide(self.name + sep + feature, provider)
    
#     def provide_on_demand(self, feature, provider=None, inst_feature=None, inst_args=(), inst_kwargs={}):
#         self.parent.provide(self.name + '.' + self.feature, provider, inst_provider)
    
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
    return feature[-1] == sep

def split_feature(feature):
    if isinstance(feature, int):
        return '', feature
    else:
        segments = feature.rpartition(sep)
        
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
        DependencyScope.__init__(self, name=None, parent=None)
        self.demanders = []
        self.allowReplace = allowReplace

    def create_scope(self, feature):
        scope = DependencyScope(name=feature, parent=self)
        self[feature] = scope
        self.check_demands(feature, scope)

    def inst_demander(self, demander):
        dependencies = {}
        for d in demander.dependencies:
            dependencies[d] = demander.satisfied[demander.dependencies[d].feature]
                
        args, kwargs = update_args(demander.provider, demander.args, demander.kwargs, dependencies)
        demander_inst = demander.provider(*args, **kwargs)
        if demander.inst_feature != '':
            demander_inst._dependents = {}
            demander_inst_feature = self.provide(demander.inst_feature, demander_inst)

            for _, dep_provider in dependencies.items():
                if not hasattr(dep_provider, '_dependents'):
                    dep_provider._dependents = {}
                    
                dep_provider._dependents[demander_inst_feature] = demander_inst

    def check_demands(self, feature, provider):
        inst_on_demand = set()
        for d in reversed(self.demanders):
            if d.satisfied_on_feature_provided(feature, provider):
                if d.inst_feature not in inst_on_demand:
                    self.inst_demander(d)
                    inst_on_demand.add(d.inst_feature)

    def provide(self, feature, provider):
        if not self.allowReplace:
            assert not (feature in self.providers), "Duplicate feature: %r" % feature

        feature_ext = feature

        if anonymous(feature):
            feature_ext += str(id(provider))
            
        if feature_ext[0] == sep:
            feature_ext = feature_ext[1:]

        self[feature_ext] = provider
        
        self.check_demands(feature, provider)
        
        return feature_ext
    
    def provide_on_demand(self, feature, provider=None, inst_feature=None, inst_args=(), inst_kwargs={}):
        assert inst_feature is not None, "Have to provide feature to be instantiated!"
        
        if provider is not None:
            self.provide(feature, provider)
        
        demander = Demander(feature, inst_feature, list(inst_args), dict(inst_kwargs))
        self.demanders.append(demander)
        if demander.all_satisfied():
            self.inst_demander(demander)
    
    def unprovide(self, feature):
        provider = self[feature]
        if hasattr(provider, '_dependents'):
            for d in provider._dependents:
                self.unprovide(d)
                
        del self[feature]
    
#     def create_on_demand(self, feature, inst_feature=None, args=(), kwargs={}):
#         self.demanders.append(Demander(feature, inst_feature, list(args), dict(kwargs)))

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

Dependency = namedtuple('Dependency', ['feature', 'assertion'])
Dependency.__new__.__defaults__ = (None, NoAssertion)

#      
# class Test:
#     def __init__(self, a, b: Dependency(feature='scope.'), c: Dependency(feature='mark')):
#         self.b = b
#         self.c = c
#   
# class Test1:
#     def __init__(self, a, b: Dependency(feature='scope.'), c: Dependency(feature='scope.subscope.')):
#         self.b = b
#         self.c = c
#   
#       
# class Mark:
#     pass
#   
# def bla():
#     pass    
#   
# ddic.provide('test', Test, '.', inst_args=(1,))
#   
# ddic.provide('mark', Mark)
# ddic.create_scope('scope')
# ddic.provide('scope.test1', Test1, 'scope.subscope.Test1', inst_args=(1,))
#   
# ddic.create_scope('scope.subscope')
# ddic.provide('scope.', bla)
# ddic.provide('scope.subscope.', bla)
#  
# ddic.unprovide('scope.' + str(id(bla)))
#   
# pass
