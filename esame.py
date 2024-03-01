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
                
                #Se non ci sono almeno due campi, posso passare alla riga successiva                
                if(len(elements) < 2):
                    continue
                # Pulisco gli elementi che mi interessano
                # con la funzione strip():
                elements[1] = elements[1].strip()                
                elements[0] = elements[0].strip()

                # Se NON sto processando l'intestazione...
                if elements[0] != 'date':
                    annomese = elements[0].split('-')
                    anno = annomese[0]
                    mese = annomese[1]

                # Per saltare le righe contenenti degli spazi bianchi:
                for string in elements[0:2]:
                    for charachter in string:
                        if charachter == " ":
                            continue


                try:
                    int(anno)
                except Exception:
                    continue
                
                # Verifichiamo che la lunghezza della stringa mese sia plausibile (2 caratteri)
                # Nel caso il mese sia incorrettamente registrato con una sola cifra, la riga
                # sarà ignorata.

                if(len(mese)!=2):
                    continue

                # Controlliamo di avere effettivamente un mese, quindi 1 o 0 alla prima cifra, non doppio 0,
                # e 1 o 2 se la prima cifra è 1
                if(mese[0] == '1'):
                    try:
                        if(int(mese[-1]) > 2):
                            continue
                    except Exception:
                        continue
                elif(mese[0] == '0'):
                    if(mese[1] == '0'):
                        continue
                else:
                    continue
                
                # Per quanto riguarda gli anni non poniamo limiti particolari, anche se
                # ovviamente per lo specifico esempio degli aerei ce ne sarebbero, tranne uno:
                if anno == '0':
                    continue

                # Aggiungo alla lista gli elementi rilevanti (mese,anno) di questa linea 
                data.append(elements[0:2])
                
                # Per rendere meno intricato il codice, controllo alla fine se ci sono
                # eccezioni da alzare relative ai timestamps:

            # Chiudo il file
            my_file.close()
            
            if(len(data) == 0):
                raise ExamException('Errore, lista valori vuota')
            
            # Per rendere meno intricato il codice, controllo alla fine se ci sono
            # eccezioni da alzare relative ai timestamps:
                        
            anno_vecchio = int(data[0][0][0:4])
            mese_vecchio = (data[0][0][5:])
            for lista in data[1:]:
                anno_corrente = int(lista[0][0:4])
                mese_corrente = (lista[0][5:])
                if(anno_corrente == anno_vecchio and mese_corrente == mese_vecchio):
                    raise ExamException('La serie temporale contiene un timestamp duplicato! Ci sono due {}'.format(str(anno_corrente) + '-' + mese_corrente))
                if(anno_corrente < anno_vecchio):
                    raise ExamException('La serie temporale non è ordinata! Si veda l\'osservazione {} e la precedente'.format((str(anno_corrente) + '-' + mese_corrente)))
                if(anno_corrente == anno_vecchio): 
                    if(mese_corrente[0] == mese_vecchio[0]):
                        if(int(mese_corrente[1]) < int(mese_vecchio[1])):
                            raise ExamException('La serie temporale non è ordinata! Si veda l\'osservazione {} e la precedente'.format((str(anno_corrente) + '-' + mese_corrente)))
                    if(int(mese_corrente[0]) < int(mese_vecchio[0])):
                        raise ExamException('La serie temporale non è ordinata! Si veda l\'osservazione {} e la precedente'.format((str(anno_corrente) + '-' + mese_corrente)))
                anno_vecchio = anno_corrente
                mese_vecchio = mese_corrente
            
            for osservazione in data:   #trasformo in numerica ogni osservazione riguardo al numero di passeggeri
                osservazione[1] = int(osservazione[1])
            # Quando ho processato tutte le righe, ritorno i dati
            return data

        
def find_min_max(time_series):
    anno_inizio = int(time_series[0][0][0:4])
    anno_fine = int(time_series[-1][0][0:4])
    diz = {key: {} for key in range(anno_inizio, anno_fine + 1)} #righe aggiunte qualora fosse necessario avere anche i dizionari vuoti
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