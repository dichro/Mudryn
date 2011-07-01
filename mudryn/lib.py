class ClassNotFoundError(AttributeError):
  def __init__(self, target, module, attr):
    self.target = target
    self.module = module
    self.attr = attr

  def __str__(self):
    return 'Subclass %s not found in module %s for %s' % (
        self.attr, self.module, self.target)


def get_class(kls):
  parts = kls.split('.')
  module = ".".join(parts[:-1])
  m = __import__( module )
  for comp in parts[1:]:
    try:
      m = getattr(m, comp)
    except AttributeError:
      raise ClassNotFoundError(kls, m.__name__, comp)
  return m
