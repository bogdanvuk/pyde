from collections import namedtuple

Demander = namedtuple('Demander', ['feature', 'inst_name', 'inst_scope', 'args', 'kwargs'])

class DependencyContainer:
    
    def __init__(self, allowReplace=False):
        self.providers = {}
        self.demanders = []
        self.allowReplace = allowReplace
    
    def provide(self, feature, provider, *args, **kwargs):
        if not self.allowReplace:
            assert not (feature in self.providers), "Duplicate feature: %r" % feature
        if callable(provider):
            def call(): return provider(*args, **kwargs)
        else:
            def call(): return provider

        self.providers[feature] = call
        self.feature_added(feature)
    
    def create_on_demand(self, feature, inst_name=None, inst_scope='', *args, **kwargs):
        self.demanders.append(Demander(feature, inst_name, inst_scope, list(args), dict(kwargs)))
    
    def all2kwargs(func, *args, **kwargs):
        arg_names, varargs, varkw, defaults = (
            inspect.getfullargspec(func))
    
        params = kwargs
        
        if defaults:
            # Add all the arguments that have a default value to the kwargs
            for name, val in zip(reversed(arg_names), reversed(defaults)):
                if name not in params:
                    params[name] = val
    
        for name, val in zip(arg_names, args):
            params[name] = val
        
        args = args[len(arg_names)]
    
        return params

    
    def feature_added(self, feature):
        for d in self.demanders:
            feature = self[d.feature]
            
            if hasattr(feature, "__annotations__"):
                annotations = feature.__annotations__
            else:
                annotations = feature.__init__.__annotations__
            
            dependency = {}
            for name, a in annotations.items():
                if isinstance(a, Dependency):
                    try:
                        dependency[name] = self[a.feature]
                        if not a.assertion(dependency[name]):
                            break
                    except KeyError:
                        break
            else:
                kwargs = dict(d.kwargs)
                obj = feature()
                
            
        
    def __getitem__(self, feature):
        try:
            provider = self.providers[feature]
        except KeyError:
            raise KeyError("Unknown feature named {0}".format(feature))
        return provider()


ddic = DependencyContainer()

class DependencyScope:
    pass

def NoAssertion(obj): return True

def IsInstanceOf(*classes):
    def test(obj): return isinstance(obj, classes)
    return test

def HasAttributes(*attributes):
    def test(obj):
        for each in attributes:
            if not hasattr(obj, each): return False
        return True
    return test

def HasMethods(*methods):
    def test(obj):
        for each in methods:
            try:
                attr = getattr(obj, each)
            except AttributeError:
                return False
            if not callable(attr): return False
        return True
    return test

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

def CreateOnDemand(cls):
    ddic

Dependency = namedtuple('Dependency', ['feature', 'scope', 'assertion'])
Dependency.__new__.__defaults__ = (None, None, None)
    
class Test:
    def __init__(self, a, b: Dependency(scope='asdf.as'), c: Dependency(feature='mark')):
        self.b = b
        self.c = c
    
CreateOnDemand(Test)
# ddic.provide(obj, feature)
# ddic.create_on_demand(feature, inst_name, inst_scope)
