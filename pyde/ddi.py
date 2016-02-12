from collections import namedtuple
import inspect
from inspect import getfullargspec, signature
from weakref import WeakValueDictionary
from PyQt4 import QtCore
from functools import wraps, partial

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
    
    def __init__(self, feature, inst_feature, args = (), kwargs = {}, deps={}):
        self.feature = feature
        self.inst_feature = inst_feature
        self.args = args
        self.kwargs = kwargs
        self.deps = deps
        self.dependencies = {}
        self.dir_dependencies = []
        self.simple_dependencies = []
        self.dependencies_by_feature = {}
        self.satisfied = set() #WeakValueDictionary()
        self.provider = None
        self.extract_dependencies()
#             for name, d in self.dependencies.items():
#                 if d.feature in ddic:
#                     self.satisfied_on_feature_provided(d.feature, ddic[d.feature])
                        
    def all_satisfied(self):
        return len(self.satisfied) == len(self.dependencies)
    
    def extract_dependencies(self):
        if self.dependencies:
            return True
        elif self.feature not in ddic:
            return False
        else:
            self.provider = ddic[self.feature]

            self.dependencies = {}            
            for name, d in self.deps.items():
                self.dependencies[name] = d
                self.dependencies_by_feature[d.feature] = d
            
            _, _, _, _, _, _, annotations = getfullargspec(self.provider)
                
            for name, a in annotations.items():
                if isinstance(a, Dependency):
                    if name not in self.dependencies:
                        self.dependencies[name] = a
                        self.dependencies_by_feature[a.feature] = a

            for dep_name, a in self.dependencies.items():
                if anonymous(a.feature):
                    self.dir_dependencies.append(dep_name)
                else:
                    self.simple_dependencies.append(dep_name)

            return True

    def all_simple_satisfied(self):
        return len(self.satisfied) == len(self.simple_dependencies)

    def check_unsatisfied_simple_dependencies(self):
        newly_satisfied = False
        for dependency in self.simple_dependencies:
            feature = self.dependencies[dependency].feature
            if (not feature in self.satisfied) and (feature in ddic):
                provider = ddic[feature]
                if self.dependencies_by_feature[feature].assertion(provider):
                    self.satisfied.add(feature) #] = provider
                    newly_satisfied = True
                    
        return newly_satisfied

    def satisfied_on_recurrent_feature_provided(self, feature):
        if (feature_scope(feature) + '/') in self.dependencies_by_feature:
            provider = ddic[feature]
            if self.dependencies_by_feature[feature_scope(feature) + '/'].assertion(provider):
#                 self.satisfied[feature_scope(feature) + '/'] = provider
                return self.all_simple_satisfied()

#     def satisfied_on_feature_provided(self, feature, provider):
#         if self.extract_dependencies():
#             if feature in self.satisfied:
#                 del self.satisfied[feature]
# 
#             if feature in self.dependencies_by_feature:
#                 if self.dependencies_by_feature[feature].assertion(provider):
#                     self.satisfied[feature] = provider
#                     
#                 return self.all_satisfied()
#             elif (feature_scope(feature) + '/') in self.dependencies_by_feature:
#                 if self.dependencies_by_feature[feature_scope(feature) + '/'].assertion(provider):
#                     self.satisfied[feature_scope(feature) + '/'] = provider
#                     return self.all_satisfied()
# 
#         return False
                
# Demander = namedtuple('Demander', ['feature', 'inst_feature', 'args', 'kwargs'])
# Demander.__new__.__defaults__ = (None, None, (), {})

sep = '/'

class DependencyScope(QtCore.QObject):
    
    provided = QtCore.pyqtSignal(QtCore.QObject, str)
    
    def __init__(self, name, parent=None, providers_cls = dict):
        super().__init__()
        self.providers = providers_cls()
        self.parent = parent
        self.name = name

    @property
    def uri(self):
        if self.parent:
            uri = self.parent.uri + [self.name]
        else:
            uri = []
            
        return uri

    def create_scope(self, feature):
        parent_scope_name, scope_base_name = split_feature(feature)
        scope = DependencyScope(name=feature)
        self[feature] = scope
        if parent_scope_name:
#             self[parent_scope_name][scope_base_name] = scope  
            scope.parent = self[parent_scope_name]
        else:
#             self[scope_base_name] = scope  
            scope.parent = self
           
        return scope
    
#     def provide_on_demand(self, feature, provider=None, inst_feature=None, inst_args=(), inst_kwargs={}):
#         self.parent.provide(self.name + '.' + self.feature, provider, inst_provider)
    
    def __iter__(self):
        return self.providers.__iter__()
    
    def _provide(self, feature, provider):
        scope, base = split_feature(feature)
        
        if scope:
            try:
                self[scope]._provide(base, provider)
            except KeyError:
                self.create_scope(scope)
                self[scope]._provide(base, provider)
        else:
            if base.isnumeric():
                base = int(base)

            self.providers[base] = provider
            self.provided.emit(self, str(base))

    def unprovide(self, feature):
        self.parent.unprovide(sep.join([self.name, feature]))

    def provide(self, feature, provider):
        self.parent.provide(sep.join([self.name, feature]), provider)
    
    def __setitem__(self, feature, provider):
        self.provide(feature, provider)

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
        scope = super().create_scope(feature)
#         scope = DependencyScope(name=feature, parent=self)
#         self[feature] = scope
        self.check_demands(feature, scope)

    def inst_demander(self, demander, recurrent_feature=None):
        dependencies = {}
        for d in demander.simple_dependencies:
            dependencies[d] = self[demander.dependencies[d].feature]
#             dependencies[d] = demander.satisfied[demander.dependencies[d].feature]
            
        if recurrent_feature is not None:
            for d in demander.dir_dependencies:
                if (feature_scope(recurrent_feature) + '/') == demander.dependencies[d].feature:
                    provider = ddic[recurrent_feature]
                    if demander.dependencies_by_feature[feature_scope(recurrent_feature) + '/'].assertion(provider):
                        dependencies[d] = provider

        args, kwargs = update_args(demander.provider, demander.args, demander.kwargs, dependencies)
        demander_inst = demander.provider(*args, **kwargs)
        if demander.inst_feature:
            demander_inst._dependents = {}
            demander_inst_feature = self.provide(demander.inst_feature, demander_inst)

#             for _, dep_provider in dependencies.items():
#                 if not hasattr(dep_provider, '_dependents'):
#                     dep_provider._dependents = {}
#                     
#                 dep_provider._dependents[demander_inst_feature] = demander_inst

    def check_and_inst_demander(self, d, feature, provider = None, already_inst = set()):
        if not d.all_satisfied():
            if d.check_unsatisfied_simple_dependencies():
                if d.all_satisfied():
                    self.inst_demander(d)
                    return

            if d.all_simple_satisfied() and (not d.all_satisfied()):
#                 if len(d.dir_dependencies) == 1:
#                     dir_dep = d.dir_dependencies[0]
#                     dir_feature = feature_scope(dir_dep) 
#                     if dir_feature in self:
#                         for f in self[dir_feature]:
#                             self.inst_demander(d, dir_dep + f)
                            
                if d.satisfied_on_recurrent_feature_provided(feature):
                    self.inst_demander(d, feature)

#         if not provider:
#             provider = self[feature]
#             
#         if demander.satisfied_on_feature_provided(feature, provider):
#             if not demander.inst_feature or (demander.inst_feature not in already_inst):
#                 already_inst.add(demander.inst_feature)
#                 self.inst_demander(demander)
#                 return True
#             
#         return False


    def check_demands(self, feature, provider = None):
#         inst_on_demand = set()
        for d in reversed(self.demanders):
            if d.feature == 'mode/cls/python' and feature == 'view/QsciScintillaCompat.py':
                pass
            self.check_and_inst_demander(d, feature)
#             if not d.all_satisfied():
#                 if d.check_unsatisfied_simple_dependencies():
#                     if len(d.dir_dependencies) == 1:
#                         dir_dep = d.dir_dependencies[0]
#                         dir_feature = feature_scope(dir_dep) 
#                         if dir_feature in self:
#                             for f in self[dir_feature]:
#                                 self.inst_demander(d, dir_dep + f)
# #                                 self.check_and_inst_demander(d, dir_dep + f)
#                 if d.all_simple_satisfied() and (not d.all_satisfied()):
#                     if d.satisfied_on_recurrent_feature_provided(feature):
#                         self.inst_demander(d, feature)
                    
#             if not self.check_and_inst_demander(d, feature, provider, inst_on_demand):
#                 if len(d.dir_dependencies) == 1:
#                     dir_dep = d.dir_dependencies[0]
#                     dir_feature = feature_scope(dir_dep) 
#                     if dir_feature in self:
#                         for f in self[dir_feature]:
#                             self.check_and_inst_demander(d, dir_dep + f)
            
    def provide(self, feature, provider):
        if feature == 'init_layout':
            pass
        
        if not self.allowReplace:
            assert not (feature in self.providers), "Duplicate feature: %r" % feature

        feature_ext = feature

        if anonymous(feature):
            feature_ext += str(id(provider))
            
        if feature_ext[0] == sep:
            feature_ext = feature_ext[1:]

#         self[feature_ext] = provider
        self._provide(feature_ext, provider)
        
        self.check_demands(feature_ext, provider)
        
        return feature_ext
    
    def provide_on_demand(self, feature, provider=None, inst_feature=None, inst_args=(), inst_kwargs={}, deps={}):
#         assert inst_feature is not None, "Have to provide feature to be instantiated!"
        
        if provider is not None:
            self.provide(feature, provider)
        
        demander = Demander(feature, inst_feature, list(inst_args), dict(inst_kwargs), deps)
        self.demanders.append(demander)
        
        if demander.all_satisfied():
            self.inst_demander(demander)
        elif len(demander.dir_dependencies) == 1:
            dir_dep = demander.dir_dependencies[0]
            dir_feature = feature_scope(dir_dep) 
            if dir_feature in self:
                for f in self[dir_feature]:
                    self.check_and_inst_demander(demander, dir_dep + f)
        else:
            self.check_and_inst_demander(demander, feature)
    
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

def diinit(func):
    _, _, _, _, _, _, annotations = getfullargspec(func)
    
    dependencies = {}
    dep_dflts = {}
    
    for name, a in annotations.items():
        if isinstance(a, Dependency):
            dependencies[name] = a
            dep_dflts[name] = None

#     if dep_dflts:
#         func = partial(func, **dep_dflts)

    @wraps(func)
    def wrapper(*args, **kwargs):
#         print('HERE!')
        dependency_kwargs = {}
        
        for name, a in dependencies.items():
            provider = ddic[a.feature]
            if a.assertion(provider):
                dependency_kwargs[name] = provider
        
        args, kwargs = update_args(func, args, kwargs, dependency_kwargs)
        return func(*args, **kwargs)
    
    if dependencies:
        sig = signature(wrapper)
        params = []
        for p in sig.parameters.values():
            if p.name not in dependencies:
                params.append(p)
                 
        sig = sig.replace(parameters=tuple(params))
        wrapper.__signature__ = sig

    return wrapper #wraps(wrapper)(func) 

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
