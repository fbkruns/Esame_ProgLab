class ExamException(Exception):
    pass

#==============================
#  Classe per file CSV
#==============================


class CSVFile:

    def __init__(self, name):
        
        # Setto il nome del file
        self.name = name
        
        
        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False
            print('Errore in apertura del file: "{}"'.format(e))


    def get_data(self):
        
        if not self.can_read:
            
            # Se nell'init ho settato can_read a False vuol dire che
            # il file non poteva essere aperto o era illeggibile
            print('Errore, file non aperto o illeggibile')
            
            # Esco dalla funzione tornando "niente".
            return None

        else:
            # Inizializzo una lista vuota per salvare tutti i dati
            data = []
    
            # Apro il file
            my_file = open(self.name, 'r')

            # Leggo il file linea per linea
            for line in my_file:
                
                # Faccio lo split di ogni linea sulla virgola
                elements = line.split(',')
                
                # Posso anche pulire il carattere di newline 
                # dall'ultimo elemento con la funzione strip():
                elements[-1] = elements[-1].strip()
                
                # p.s. in realta' strip() toglie anche gli spazi
                # bianchi all'inizio e alla fine di una stringa.
    
                # Se NON sto processando l'intestazione...
                if elements[0] != 'Date':
                        
                    # Aggiungo alla lista gli elementi di questa linea
                    data.append(elements)
                    
            for osservazione in data:   #trasformo in numerica ogni osservazione riguardo al numero di passeggeri
                osservazione[1] = int(osservazione[1])
            # Chiudo il file
            my_file.close()
            
            # Quando ho processato tutte le righe, ritorno i dati
            return data

#==============================
#  Esempio di utilizzo
#==============================

#mio_file = CSVFile(name='shampoo_sales.csv')
#print('Nome del file: "{}"'.format(mio_file.name))
#print('Dati contenuti nel file: "{}"'.format(mio_file.get_data()))

#mio_file_numerico = NumericalCSVFile(name='shampoo_sales.csv')
#print('Nome del file: "{}"'.format(mio_file_numerico.name))
#print('Dati contenuti nel file: "{}"'.format(mio_file_numerico.get_data()))
    
class CSVTimeSeriesFile:

    def __init__(self, name):
        
        # Setto il nome del file
        self.name = name
        
        
        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False
            print('Errore in apertura del file: "{}"'.format(e))


    def get_data(self):
        
        if not self.can_read:
            
            # Se nell'init ho settato can_read a False vuol dire che
            # il file non poteva essere aperto o era illeggibile
            print('Errore, file non aperto o illeggibile')
            
            # Esco dalla funzione tornando "niente".
            return None

        else:
            # Inizializzo una lista vuota per salvare tutti i dati
            data = []
    
            # Apro il file
            my_file = open(self.name, 'r')

            # Leggo il file linea per linea
            for line in my_file:
                
                # Faccio lo split di ogni linea sulla virgola
                elements = line.split(',')
                
                # Posso anche pulire il carattere di newline 
                # dall'ultimo elemento con la funzione strip():
                elements[-1] = elements[-1].strip()
                
                # p.s. in realta' strip() toglie anche gli spazi
                # bianchi all'inizio e alla fine di una stringa.
    
                # Se NON sto processando l'intestazione...
                if elements[0] != 'Date':
                        
                    # Aggiungo alla lista gli elementi di questa linea
                    data.append(elements)
            
            # Chiudo il file
            my_file.close()
            
            # Quando ho processato tutte le righe, ritorno i dati
            return data
        
def find_min_max(time_series) -> dict:
    diz = {}
    mese_max = []
    mese_min = []
    max_pass = time_series[0][1]
    min_pass = time_series[0][1]
    anno = time_series[0][0][0:4]
    
    for i in range(len(time_series)):
        anno_nuovo = time_series[i][0][0:4]
        
        if anno_nuovo == anno:
            if max_pass < time_series[i][1]:
                max_pass = time_series[i][1]
                mese_max = [time_series[i][0][-2:]]
            elif max_pass == time_series[i][1]:
                mese_max.append(time_series[i][0][-2:])
                
            if min_pass > time_series[i][1]:
                min_pass = time_series[i][1]
                mese_min = [time_series[i][0][-2:]]
            elif min_pass == time_series[i][1]:
                mese_min.append(time_series[i][0][-2:])
        else:
            diz[anno] = {'min': mese_min, 'max': mese_max}
            mese_max = [time_series[i][0][-2:]]
            mese_min = [time_series[i][0][-2:]]
            anno = anno_nuovo
            max_pass = time_series[i][1]
            min_pass = time_series[i][1]
    
    diz[anno] = {'max': mese_max, 'min': mese_min}  # aggiungo massimo e minimo dell'ultimo anno

    return diz