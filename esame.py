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
        
def find_min_max(time_series)->dict:
    diz = {}
    mese_max = [None]
    mese_min = [None]
    anno = 0
    max_pass = -1
    min_pass = 999999
    for i in range(0, len(time_series)):
        if time_series[i][0][0:4] == anno:
            if (max_pass < time_series[i][1]):
                max_pass = time_series[i][1]
                mese_max.clear()
                mese_max.append(time_series[i][0][-2:])
            elif (max_pass == time_series[i][1]):
                print('Il mese uguale che viene aggiunto è: {}'.format(time_series[i][0][-2:]))
                mese_max.append(time_series[i][0][-2:])   
            if (min_pass > time_series[i][1]):
                min_pass = time_series[i][1]
                mese_min.clear()
                mese_min.append(time_series[i][0][-2:])
            elif (min_pass == time_series[i][1]):
                print('Il mese uguale che viene aggiunto è: {}'.format(time_series[i][0][-2:]))
                mese_max.append(time_series[i][0][-2:])   


        else:

            diz[anno] = {'max': mese_max, 'min': mese_min}
            mese_max = [None]
            mese_min = [None]
            anno = time_series[i][0][0:4]
            max_pass = time_series[i][1]
            min_pass = time_series[i][1]
    return diz

    