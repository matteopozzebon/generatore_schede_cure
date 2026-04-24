import os
import calendar
import datetime
import platform
import subprocess
from typing import List
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from dataclasses import dataclass
import pdfkit
from pypdf import PdfWriter

@dataclass
class Day:
    number: int
    name: str

def main(): 

    #region menu
    print("Seleziona l'azione da svolgere:")
    print("1) Generazione di una scheda cure vuota")
    print("2) Generazione schede vuote da mese a mese")
    print("3) Generazione di una scheda cure vuota 2(celle su ultima colonna)")
    print("4) Generazione schede vuote 2 da mese a mese(celle su ultima colonna)")
    print("5) Generazione dell'elenco delle cure")
    print("6) Esci")
    option = input("Seleziona l'opzione desiderata: ")
    #endregion

    match int(option):
        case 1:
            #region Creazione scheda vuota

            anno_str = input("Inserisci l'anno: ")
            mese_str = input("Inserisci il mese: ")

            Controllo_Argomenti(anno_str, mese_str)

            anno = int(anno_str)
            mese = int(mese_str)

            calendar = Crea_Calendario(anno, mese)

            nome_mese = Trova_Nome_Mese(mese)

            Cancella_Vecchie_Schede_PDF("./Modelli_Schede_Cura")

            Creazione_Scheda_Vuota(calendar, nome_mese, anno , "Modello_Schede_Cura.html", 1)

            Creazione_Scheda_Vuota_PDF("./Modelli_Schede_Cura")

            Cancella_Vecchie_Schede_HTML("./Modelli_Schede_Cura")

            print("1) Apri PDF")
            print("2) Stampa PDF")
            print("3) Esci")
            ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            while ApriStampa not in ("1", "2", "3"):
                print("1) Apri PDF")
                print("2) Stampa PDF")
                print("3) Esci")                
                ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            match int(ApriStampa):
                case 1:
                    for filename in os.listdir("./Modelli_Schede_Cura"):
                        os.system(f"xdg-open './Modelli_Schede_Cura/{filename}'")
                case 2:
                    try: 
                        for filename in os.listdir("./Modelli_Schede_Cura"):
                            Stampa_PDF(f"./Modelli_Schede_Cura/{filename}")
                    except:
                        raise Exception("Errore durante il tentativo di stampa!")
                case 3:
                    exit()

            #endregion
        
        case 2:
            #region Creazione lista modello cure
            print("Generazione modelli schede...")

            anno_str = input("Inserisci l'anno: ")
            daMese = input("Da mese: ")

            while daMese not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"): 
                daMese = input("Da mese: ")

            aMese = input("A mese: ")

            while aMese not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"): 
                aMese = input("A mese: ")

            if int(aMese) < int(daMese):
                raise Exception("Il mese di partenza non può essere successivo a quello di partenza!")    
            
            anno = int(anno_str)
            mese = int(daMese)

            Cancella_Vecchie_Schede_PDF("./Modelli_Schede_Cura")

            while mese <= int(aMese):
                calendar = Crea_Calendario(anno, mese)

                nome_mese = Trova_Nome_Mese(mese)

                Creazione_Scheda_Vuota_Lista(calendar, nome_mese, anno , "./Modello_Schede_Cura.html", 1, str(mese))
                mese +=1

            Creazione_Scheda_Vuota_PDF("./Modelli_Schede_Cura")    
            
            Cancella_Vecchie_Schede_HTML("./Modelli_Schede_Cura")

            Accoda_PDF_Modelli(daMese, aMese, anno_str, "./Modelli_Schede_Cura")
            print("Generazione completata!")

            print("1) Apri PDF")
            print("2) Stampa PDF")
            print("3) Esci")
            ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            while ApriStampa not in ("1", "2", "3"):
                print("1) Apri PDF")
                print("2) Stampa PDF")
                print("3) Esci")                
                ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            match int(ApriStampa):
                case 1:
                    for filename in os.listdir("./Modelli_Schede_Cura"):
                        os.system(f"xdg-open './Modelli_Schede_Cura/{filename}'")
                case 2:
                    try: 
                        for filename in os.listdir("./Modelli_Schede_Cura"):
                            Stampa_PDF(f"./Modelli_Schede_Cura/{filename}")
                    except:
                        raise Exception("Errore durante il tentativo di stampa!")
                case 3:
                    exit()            
            #endregion

        case 3:
            #region Creazione scheda vuota 2

            anno_str = input("Inserisci l'anno: ")
            mese_str = input("Inserisci il mese: ")

            Controllo_Argomenti(anno_str, mese_str)

            anno = int(anno_str)
            mese = int(mese_str)

            calendar = Crea_Calendario(anno, mese)

            nome_mese = Trova_Nome_Mese(mese)

            Cancella_Vecchie_Schede_PDF("./Modelli_Schede_Cura_2")

            Creazione_Scheda_Vuota(calendar, nome_mese, anno , "Modello_Schede_Cura_2.html", 2)

            Creazione_Scheda_Vuota_PDF("./Modelli_Schede_Cura_2")

            Cancella_Vecchie_Schede_HTML("./Modelli_Schede_Cura_2")

            print("1) Apri PDF")
            print("2) Stampa PDF")
            print("3) Esci")
            ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            while ApriStampa not in ("1", "2", "3"):
                print("1) Apri PDF")
                print("2) Stampa PDF")
                print("3) Esci")                
                ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            match int(ApriStampa):
                case 1:
                    for filename in os.listdir("./Modelli_Schede_Cura_2"):
                        os.system(f"xdg-open './Modelli_Schede_Cura_2/{filename}'")
                case 2:
                    try: 
                        for filename in os.listdir("./Modelli_Schede_Cura_2"):
                            Stampa_PDF(f"./Modelli_Schede_Cura_2/{filename}")
                    except:
                        raise Exception("Errore durante il tentativo di stampa!")
                case 3:
                    exit()
            #endregion
        
        case 4:
            #region Creazione lista modello cure 2
            print("Generazione modelli schede...")

            anno_str = input("Inserisci l'anno: ")
            daMese = input("Da mese: ")

            while daMese not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"): 
                daMese = input("Da mese: ")

            aMese = input("A mese: ")

            while aMese not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"): 
                aMese = input("A mese: ")

            if int(aMese) < int(daMese):
                raise Exception("Il mese di partenza non può essere successivo a quello di partenza!")    
            
            anno = int(anno_str)
            mese = int(daMese)

            Cancella_Vecchie_Schede_PDF("./Modelli_Schede_Cura_2")

            while mese <= int(aMese):
                calendar = Crea_Calendario(anno, mese)

                nome_mese = Trova_Nome_Mese(mese)

                Creazione_Scheda_Vuota_Lista(calendar, nome_mese, anno , "./Modello_Schede_Cura_2.html", 2, str(mese))
                mese +=1

            Creazione_Scheda_Vuota_PDF("./Modelli_Schede_Cura_2")    
            
            Cancella_Vecchie_Schede_HTML("./Modelli_Schede_Cura_2")

            Accoda_PDF_Modelli(daMese, aMese, anno_str, "./Modelli_Schede_Cura_2")
            print("Generazione completata!")

            print("1) Apri PDF")
            print("2) Stampa PDF")
            print("3) Esci")
            ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            while ApriStampa not in ("1", "2", "3"):
                print("1) Apri PDF")
                print("2) Stampa PDF")
                print("3) Esci")                
                ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            match int(ApriStampa):
                case 1:
                    for filename in os.listdir("./Modelli_Schede_Cura_2"):
                        os.system(f"xdg-open './Modelli_Schede_Cura_2/{filename}'")
                case 2:
                    try: 
                        for filename in os.listdir("./Modelli_Schede_Cura_2"):
                            Stampa_PDF(f"./Modelli_Schede_Cura_2/{filename}")
                    except:
                        raise Exception("Errore durante il tentativo di stampa!")
                case 3:
                    exit()            
            #endregion
        
        case 5:
            #region Creazione schede di cura

            anno_str = input("Inserisci l'anno: ")
            mese_str = input("Inserisci il mese: ")

            #Controllo che gli argomenti inseriti siano corretti
            Controllo_Argomenti(anno_str, mese_str)

            anno = int(anno_str)
            mese = int(mese_str)

            calendar = Crea_Calendario(anno, mese)

            excel = Lettura_Excel_Cure('./Elenco_cure/Cure.xlsx')

            nome_mese = Trova_Nome_Mese(mese)

            Cancella_Vecchie_Schede_PDF("./Schede_generate")

            Creazione_Schede(excel, calendar, nome_mese, anno)

            Creazione_Schede_PDF()

            Cancella_Vecchie_Schede_HTML("./Schede_generate")

            Accoda_PDF(nome_mese, str(anno))

            print("1) Apri PDF")
            print("2) Stampa PDF")
            print("3) Esci")
            ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            while ApriStampa not in ("1", "2", "3"):
                print("1) Apri PDF")
                print("2) Stampa PDF")
                print("3) Esci")                
                ApriStampa = input("Vuoi aprire o stampare il PDF generato? ")

            match int(ApriStampa):
                case 1:
                    for filename in os.listdir("./Schede_generate"):
                        os.system(f"xdg-open './Schede_generate/{filename}'")
                case 2:
                    try: 
                        for filename in os.listdir("./Schede_generate"):
                            Stampa_PDF(f"./Schede_generate/{filename}")
                    except:
                        raise Exception("Errore durante il tentativo di stampa!")
                case 3:
                    exit()
            #endregion

        case 6:
            exit()

#Funzione per controllo validità opzione selezionata
def Controllo_opzione_menu(opzione: str):
    if opzione not in ("1", "2", "3", "4"):
        raise Exception('Opzione selezionata non valida!')  

#Funzione per il controllo della validità degli argomenti
def Controllo_Argomenti(anno: str, mese: str):    
    current_year = datetime.date.today().year

    try:
        try:
            anno_int = int(anno)
            mese_int = int(mese)
        except:
            raise Exception("Anno o Mese digitati non validi!")
                
        if len(str(anno_int)) != 4:       
            raise Exception("L'anno inserito non è valido!")
        
        if (anno_int < current_year - 10):
            raise Exception(f"L'anno più vecchio consentito è: {current_year - 10}")
        
        if (anno_int > current_year + 10):
            raise Exception(f"L'anno più nuovo consentito è: {current_year + 10}")

        if mese_int < 1 or mese_int > 12:
            raise Exception("Il mese inserito non è valido!")
    except Exception as e:
        raise Exception(str(e))
    
#Funzione per la ricerca del nome del mese
def Trova_Nome_Mese(mese: int) -> str:
    match mese:
        case 1:
            return "Gennaio" 
        case 2:
            return "Febbraio"
        case 3:
            return  "Marzo"
        case 4:
            return "Aprile"
        case 5:
            return "Maggio"
        case 6:
            return "Giugno"
        case 7:
            return "Luglio"
        case 8:
            return "Agosto"
        case 9:
            return "Settembre"
        case 10:
            return "Ottobre"
        case 11:
            return "Novembre"
        case 12:
            return "Dicembre"
        
#Funzione per creare il calendario del mese    
def Crea_Calendario(anno: int, mese: int) -> List[Day]:
    print("Creazione Calendario...")

    cal = calendar.monthcalendar(anno,mese)

    days = []
    
    for week in cal:       
        index = 0
        while index <= 6:
            if week[index] > 0:
                date = datetime.date(anno, mese, week[index])
                day_index = date.weekday()
                match calendar.day_name[day_index]:
                    case "Monday":
                        days.append(Day(week[index], "Lunedì"))
                    case "Tuesday":
                        days.append(Day(week[index], "Martedì"))
                    case "Wednesday":
                        days.append(Day(week[index], "Mercoledì"))
                    case "Thursday":
                        days.append(Day(week[index], "Giovedì"))
                    case "Friday":
                        days.append(Day(week[index], "Venerdì"))
                    case "Saturday":
                        days.append(Day(week[index], "Sabato"))
                    case "Sunday":
                        days.append(Day(week[index], "Domenica"))    
            index += 1

    print("Calendario creato!")
    return days    
    
#Funzione per restituire i dati dell'excek (array of array)
def Lettura_Excel_Cure(path: str):
    print("Lettura file cure...")
    
    df = pd.read_excel(path)
    data = df.values.tolist()

    print("File cure analizzato!")

    return data

#Funzione per la cancellazione delle vecchie schede generate in formato pdf in formato html
def Cancella_Vecchie_Schede_HTML(directory: str):
    print("Cancellazione vecchie schede HTML...")
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".html"):
            os.remove(file_path)

    print("Cancellazione HTML eseguita!") 

#Funzione per la cancellazione delle vecchie schede generate in formato pdf
def Cancella_Vecchie_Schede_PDF(directory: str):
    print("Cancellazione vecchie schede PDF...")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".pdf"):
            os.remove(file_path)

    print("Cancellazione PDF eseguita!")            

#Funzione per la creazione delle schede di cura
def Creazione_Schede(data_scheda, calendar: List[Day], mese: str, anno: int):
    print("Creazione schede in formato HTML...")

    #Carico template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("scheda_cure.html")

    title = f"{mese} {str(anno)}"

    for row in data_scheda:
        # Data to inject
        data = {
            "title": title,
            "days": calendar,
            "days_number": len(calendar),
            "dati": row,
        }

        # Render HTML
        output = template.render(data)

        # Save report
        with open(f"./Schede_generate/{row[0]}.html", "w") as f:
            f.write(output)

        print(f"Report generated: {row[0]}.html")       

    print("Creazione schede HTML eseguita!")

#Funzione per la conversione delle schede in formato PDF
def Creazione_Schede_PDF():
    directory = "./Schede_generate"

    print("Conversione in PDF delle schede generate...")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        name, ext = os.path.splitext(filename)    
        pdfkit.from_file(file_path, f"{directory}/{name}.pdf", options={"enable-local-file-access": ""})
    
    print("Conversione PDF eseguita!")

#Funzione per la creazione di un solo PDF con tutte le schede
def Accoda_PDF(mese: str, anno: str):
    print("Creazione di un singolo PDF con tutte le schede cura...")
    pdf_files = []
    directory = "./Schede_generate"

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)    
        pdf_files.append(file_path)
    
    pdf_files.sort()

    merger = PdfWriter()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(f"{directory}/{mese}_{anno}.pdf")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        print(filename)
        if os.path.isfile(file_path) and filename != f"{mese}_{anno}.pdf":
            os.remove(file_path)        
    
    print("PDF con schede cura generato!")

#Funzione per la creazione di un solo PDF con i modelli da mese a mese
def Accoda_PDF_Modelli(daMese: str, aMese: str, anno: str, directory: str):
    print("Creazione di un singolo PDF con tutti modelli delle schede cura...")
    pdf_files = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)    
        pdf_files.append(file_path)

    print(pdf_files)
    pdf_files.sort()
    
    merger = PdfWriter()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(f"{directory}/{daMese}_{aMese}_{anno}.pdf")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        print(filename)
        if os.path.isfile(file_path) and filename != f"{daMese}_{aMese}_{anno}.pdf":
            os.remove(file_path)        
    
    print("PDF con modelli schede cura generato!")

#Funzione per la creazione di una scheda di cura vuota
#Tipi scheda --> • 1: con rowspan • 2: senza rowspan
def Creazione_Scheda_Vuota(calendar: List[Day], mese: str, anno: int, temp: str, scheda: int):
    print("Creazione scheda...")

    #Carico template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(temp)

    title = f"{mese} {str(anno)}"

    # Data to inject
    data = {
        "title": title,
        "days": calendar,
        "days_number": len(calendar),
    }
    # Render HTML
    output = template.render(data)
    # Save report

    match scheda:
        case 1:
            with open(f"./Modelli_Schede_Cura/{mese}_{str(anno)}_Vuota.html", "w") as f:
                f.write(output)
        case 2:
            with open(f"./Modelli_Schede_Cura_2/{mese}_{str(anno)}_Vuota_2.html", "w") as f:
                f.write(output)
    
    match scheda:
        case 1:
            print(f"Report generated: {mese}_{str(anno)}_Vuota.html")   
        case 2:
            print(f"Report generated: {mese}_{str(anno)}_Vuota_2.html")

    print("Scheda generata!")

#Funzione per la creazione di una scheda di cura vuota nella lista
#Tipi scheda --> • 1: con rowspan • 2: senza rowspan
def Creazione_Scheda_Vuota_Lista(calendar: List[Day], mese: str, anno: int, temp: str, scheda: int, n_mese: str):
    print("Creazione scheda...")

    #Carico template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(temp)

    title = f"{mese} {str(anno)}"

    # Data to inject
    data = {
        "title": title,
        "days": calendar,
        "days_number": len(calendar),
    }
    # Render HTML
    output = template.render(data)
    # Save report

    match scheda:
        case 1:
            with open(f"./Modelli_Schede_Cura/{n_mese}_{str(anno)}_Vuota.html", "w") as f:
                f.write(output)
        case 2:
            with open(f"./Modelli_Schede_Cura_2/{n_mese}_{str(anno)}_Vuota_2.html", "w") as f:
                f.write(output)
    
    match scheda:
        case 1:
            print(f"Report generated: {n_mese}_{str(anno)}_Vuota.html")   
        case 2:
            print(f"Report generated: {n_mese}_{str(anno)}_Vuota_2.html")

    print("Scheda generata!")

#Funzione per la conversione della scheda in PDF
def Creazione_Scheda_Vuota_PDF(directory: str):
    print("Conversione PDF...")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        name, ext = os.path.splitext(filename)    
        pdfkit.from_file(file_path, f"{directory}/{name}.pdf")         
    
    print("Conversione eseguita!")

def Stampa_PDF(pdf_path):
    """
    Print a PDF file using the default system printer.
    Works on Linux, Windows, and macOS.
    """
    system = platform.system()

    if system == "Linux":
        # Use lp command (CUPS)
        try:
            subprocess.run(["lp", pdf_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error printing PDF on Linux: {e}")
    elif system == "Darwin":  # macOS
        try:
            subprocess.run(["lp", pdf_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error printing PDF on macOS: {e}")
    elif system == "Windows":
        try:
            os.startfile(pdf_path, "print")
        except Exception as e:
            print(f"Error printing PDF on Windows: {e}")
    else:
        print("Unsupported OS")


if __name__ == "__main__":
    main()