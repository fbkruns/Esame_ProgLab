class ExamException(Exception):
    pass

class CSVTimeSeriesFile:

    def __init__(self, name):
        
        # Setto il nome del file
        self.name = name
        
        
        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except ExamException as e:
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

                # Per controllare che il mese sia valido, splitto la stringa ed effettuo dei controlli. 
                # In particolare, controllo che siano effettivamente numeri (e poi validi). Non posso controllare 
                # direttamente se il mese sia un numero vedendo se converte in intero, in quanto i numeri che iniziano
                # per 0 non vengono riconosciuti come tali
                
                # Se NON sto processando l'intestazione...
                if elements[0] != 'date':
                    annomese = elements[0].split('-')
                    anno = annomese[0]
                    mese = annomese[1]
                try:
                    int(anno)
                except Exception:
                    continue

                # Verifichiamo che la lunghezza della stringa mese sia plausibile (2 caratteri)

                if(len(mese)!=2):
                    continue

                # Controlliamo di avere effettivamente un mese, quindi 1 o 0 alla prima cifra, non doppio 0,
                # e 1 o 2 se la prima cifra è 1
                if(mese[0]=='1'):
                    try:
                        if(int(mese[-1])>2):
                            continue
                    except Exception:
                        continue
                elif(mese[0]=='0'):
                    if(mese[1]=='0'):
                        continue
                else:
                    continue


                # if elements[0][]
                    # Aggiungo alla lista gli elementi di questa linea
                data.append(elements)
            
            # Chiudo il file
            my_file.close()
            
            # Alzo le eccezioni per i seguenti casi limite:
            if(len(data) == 0):
                raise ExamException('Errore, lista valori vuota')
            
            if(len(data[1]) == 0):
                raise ExamException('Errore, lista valori vuota')
            
            if(len(data[1]) == 0):
                raise ExamException('Errore, lista valori vuota')
            


            for osservazione in data:   #trasformo in numerica ogni osservazione riguardo al numero di passeggeri
                osservazione[1] = int(osservazione[1])
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