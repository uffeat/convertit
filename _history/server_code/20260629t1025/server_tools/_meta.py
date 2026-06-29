from tools import meta as _meta

class meta:
  def __getattr__(self, key):
    return getattr(_meta, key, None)
  
meta = meta()
   
    
