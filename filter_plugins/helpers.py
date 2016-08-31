def userdn(name, domain):
  dn = "cn=" + name
  for part in domain.split("."):
    dn += "," + "dc=" + part
  return dn

def domaindn(domain):
  parts = domain.split(".")
  return "dc=" + ",dc=".join(parts)
  
class FilterModule(object):
  def filters(self):
    return {'userdn': userdn, 'domaindn': domaindn}
