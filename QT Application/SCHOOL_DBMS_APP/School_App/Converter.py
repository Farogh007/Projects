from PyQt4 import uic

fin = open('START.ui','r')
fout = open('START_ui.py','w')
uic.compileUi(fin,fout,execute=False)
fin.close()
fout.close()