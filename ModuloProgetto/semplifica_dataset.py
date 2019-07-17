import pandas as pd

def elimina_ridondanza(D,col_ridondanti=None):
    
    if not col_ridondanti:
        col_ridondanti=[c for c in D.columns if 'erbbands' in c or 'melbands' in c or\
                             'mfcc' in c or 'gfcc' in c or ('hpcp' in c and not 'thpcp' in c) or\
                             c=='rhythm.beats_count']

    D=D.drop(col_ridondanti,axis=1)
    return X

def elimina_generi(D,gen=['Rock','Pop-Altro','Blues','Ambient','Funk']):
    t=[i for i in D.index if D.loc[i,'GENERE'] in gen]
    D=D.drop(t).reset_index(drop=True)
    return D
