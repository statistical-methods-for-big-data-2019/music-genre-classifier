import pandas as pd
from sklearn.base import TransformerMixin

class AbortError(Exception):
    pass


class Sost_Mancanti(TransformerMixin):
    '''
        questa classe e' inseribile in una pipeline di scikitlearn e permette di sostituire eventuali valori mancanti
        di un dataset. i parameetri di inzializzazione 'sost_categoriali' e 'elimina' permettono di modificare il comportamento
        nel seguente modo:
        - se 'sost_categoriali' e' posto uguale a 'True', eventuali valori NaN presenti tra le variabili categoriali del dataset
          verranno sostituiti dalla modalita' che le unita' del dataset assumono piu' frequentemente per tali variabili. In caso contrario le
          variabili categoriali resteranno inalterate.
        - se 'elimina' e' posto pari a 'True' non verra' effettuata alcuna sostitizione ma bensi' verranno eliminate dal dataset tutte le unita' che
          assumono valori NaN per almeno una variabile.

        I valori Nan presenti nelle variabili quantitative verranno sostituiti con la media delle rispettive variabili, sempre che il parametro
        'elimina' non sia 'True'.
    '''
        
    
    def __init__(self,sost_categoriali=False,elimina=False):
        self.sost_categoriali=sost_categoriali
        self.elimina=elimina

    def fit(self,X,y=None):
        
        if self.sost_categoriali:
            self.col_quant=X.select_dtypes(include=['int64','float64']).columns
            self.col_cat=X.select_dtypes(include=['object']).columns
            return self

        self.col_quant=X.select_dtypes(include=['int64','float64']).columns
        self.col_cat=[]
        return self
                        

    def transform(self,X):
        if self.elimina:
            for col in self.col_quant:
                X=X.drop(D.index([ X[col].isnull()]))
            for col in self.col_cat:
                X=X.drop(D.index([ X[col].isnull()]))
            return X
                
        for col in self.col_quant:
            X.loc[ X[col].isnull(), col] = X[col].mean()
        for col in self.col_cat:
            X.loc[ X[col].isnull(), col] = X[col].value_counts().idxmax()
        return X
        
  

class Elimina_Costanti(TransformerMixin):
    
    '''
        questa classe e' inseribile in una pipeline di scikitlearn e permette di eliminare dal dataset eventuali variabili che assumono lo stesso valore su
        tutte le unita' del dataset e che non sono percio' informative, permettendo cosi' anche di evitare la creazione di valori NaN nel momento
        della standardizzazione (si andrebbe infatti a dividere per la deviazione stardard, che , per tali variabili, sarebbe pari a zero).
    '''

    def __init__(self):
        pass

    def fit(self,X,y=None):
        self.col_costanti=[col for col in X.columns if X[col].nunique()==1]
        return self

    def transform(self,X):
        X=X.drop(self.col_costanti,axis=1)
        return X



class Elimina_Correlate(TransformerMixin):
    '''
        questa classe e' inseribile in una pipeline di scikitlearn e permette di eliminare dal dataset una variabile per ognuna delle coppie di variabili quantitative
        correlate maggiormente di una soglia fissata per default a 0.98 (ma modificabile).Se il parametro 'risparmia_RAM' e' True la funzione fit non calcola all'inizio
        una unica matrice di correlazione per tutto il dataset ciclando poi su di essa per trovare le variabili correlate ma calcola ad ogni passo la correlazione
        per la coppia di variabili prese in considerazione; questo rende piu' lento l'algoritmo ma permette di non saturare la RAM
    '''

    def __init__(self,soglia=0.98, risparmia_RAM=False):
        self.soglia=soglia
        self.risparmia_RAM=risparmia_RAM

    def fit(self,X,y=None):
        iquant=X.select_dtypes(include=['int64','float64']).columns
        self.var_da_togliere=[]
        
        if self.risparmia_RAM:
            for i,ind in enumerate(iquant[:-1]):
                if ind in self.var_da_togliere:
                    continue                     ### se la variabile e' gia' stata tolta avanzo di una riga
                for j in range(i+1,len(iquant)):
                    if abs(X.iloc[:,[i,j]].corr().iloc[1,0])>abs(self.soglia) and not iquant[j] in self.var_da_togliere:
                        self.var_da_togliere.append(iquant[j])
            return self
        
        corr=X[iquant].corr()
        for i,ind in enumerate(corr.index[:-1]):
            if ind in self.var_da_togliere:
                continue                     ### se la variabile e' gia' stata tolta avanzo di una riga
            for j in range(i+1,len(corr.columns)):
                if abs(corr.iloc[i,j])>abs(self.soglia) and not corr.columns[j] in self.var_da_togliere:
                    self.var_da_togliere.append(corr.columns[j])
        return self
        

    def transform(self,X):
        X=X.drop(self.var_da_togliere,axis=1)
        return X
    
                    
                    
class Standardizza(TransformerMixin):
    '''
        questa classe e' inseribile in una pipeline di scikitlearn e permette di standardizzare le variabili del dataset permettendo
        di scegliere se dividere oppure no per la deviazione standard 
    '''

    def __init__(self,s=True):
        self.div_std=s
        

    def fit(self,X,y=None):
        if [col for col in X.select_dtypes(include=['object']).columns]:
            print('il dataset contiene variabili categoriali o non numeriche, impossibile standardizzare..')
            raise AbortError
            
        self.media=X.mean()
        self.std=X.std()
        return self

    def transform(self,X):
        X-=self.media
        if self.div_std:
            X/=self.std
        return X

    def inverse_transform(self,X):
        if self.div_std:
            X*=self.std
        X+=self.media
        return X


class Ottieni_Dummies(TransformerMixin):
    '''
        questa classe e' inseribile in una pipeline di scikitlearn e permette di trasformare le variabili categoriali di un dataset in variabili dummy
    '''

    def __init__(self):
        pass

    def fit(self,X,y=None):
        return self

    def transform(self,X):
        X=pd.get_dummies(X,drop_first=True)
        return X

        
        
        
