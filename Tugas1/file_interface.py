import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self, params=[]):
        filename = params[0]
        if(filename==''):
            return None
        try:
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
    
    def post(self, params=[]):
        filename = params[0]
        if(filename==''):
            return None
        try:
            ### methods post 
            pass
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
    def delete(self, params=[]):
        filename = params[0]
        if(filename==''):
            return None
        try:
            os.remove(filename)
            return dict(status='OK', msg=f"File {filename} berhasil dihapus")
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
if __name__=='__main__':
    f = FileInterface()