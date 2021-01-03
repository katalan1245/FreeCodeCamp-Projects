import hashlib

def crack_sha1_hash(hash, use_salts=False):
    f = open('top-10000-passwords.txt','r')
    passes = [i.strip() for i in f]
    f.close()

    f = open('known-salts.txt','r')
    salts = f.read().split('\n')
    f.close()
    
    for password in passes:
      if use_salts:
        for p in salts:
          res1 = hashlib.sha1(bytes(password + p, 'utf-8')).hexdigest()
          res2 = hashlib.sha1(bytes(p + password,'utf-8')).hexdigest()
          if res1 == hash or res2 == hash:
            return password
        
      res = hashlib.sha1(bytes(password,'utf-8')).hexdigest()
      if res == hash:
        return password
 
    
    return "PASSWORD NOT IN DATABASE"
