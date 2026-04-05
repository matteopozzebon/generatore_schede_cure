import os
import calendar
import datetime
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
    print("Seleziona l'azione da svolgere:")
    print("1) Generazione di una scheda cure vuota")
    print("2) Generazione dell'elenco delle cure")
    print("3) Generazione di una scheda cure vuota 2(celle su ultima colonna)")
    print("4) Esci")
    option = input("Seleziona l'opzione desiderata: ")

    Controllo_opzione(option)

    match int(option):
        case 1:
            anno_str = input("Inserisci l'anno: ")
            mese_str = input("Inserisci il mese: ")

            #region Creazione scheda vuota
            Controllo_Argomenti(anno_str, mese_str)

            anno = int(anno_str)
            mese = int(mese_str)

            calendar = Crea_Calendario(anno, mese)

            nome_mese = Trova_Nome_Mese(mese)

            Cancella_Vecchia_Scheda_Vuota_PDF("./Scheda_cure_vuota")

            Creazione_Scheda_Vuota(calendar, nome_mese, anno)

            Creazione_Scheda_Vuota_PDF("./Scheda_cure_vuota")

            Cancella_Vecchia_Scheda_Vuota_HTML("./Scheda_cure_vuota")
            #endregion
        case 2:
            anno_str = input("Inserisci l'anno: ")
            mese_str = input("Inserisci il mese: ")

            #region Creazione schede di cura

            #Controllo che gli argomenti inseriti siano corretti
            Controllo_Argomenti(anno_str, mese_str)

            anno = int(anno_str)
            mese = int(mese_str)

            calendar = Crea_Calendario(anno, mese)

            excel = Lettura_Excel_Cure('./Elenco_cure/Cure.xlsx')

            nome_mese = Trova_Nome_Mese(mese)

            Cancella_Vecchie_Schede_PDF()

            Creazione_Schede(excel, calendar, nome_mese, anno)

            Creazione_Schede_PDF()

            Cancella_Vecchie_Schede_HTML()

            Accoda_PDF(nome_mese, str(anno))
            #endregion

        case 3:
            anno_str = input("Inserisci l'anno: ")
            mese_str = input("Inserisci il mese: ")

            #region Creazione scheda vuota
            Controllo_Argomenti(anno_str, mese_str)

            anno = int(anno_str)
            mese = int(mese_str)

            calendar = Crea_Calendario(anno, mese)

            nome_mese = Trova_Nome_Mese(mese)

            Cancella_Vecchia_Scheda_Vuota_PDF("./Scheda_cure_vuota_2")

            Creazione_Scheda_Vuota_2(calendar, nome_mese, anno)

            Creazione_Scheda_Vuota_PDF("./Scheda_cure_vuota_2")

            Cancella_Vecchia_Scheda_Vuota_HTML("./Scheda_cure_vuota_2")

        case 4:
            exit()

#Funzione per controllo validità opzione selezionata
def Controllo_opzione(opzione: str):
    if opzione not in ("1", "2", "3", "4"):
        raise Exception('Opzione selezionata non valida!')
        
#Funzione per il controllo della validità degli argomenti
def Controllo_Argomenti(anno, mese: str):    
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
def Crea_Calendario(anno, mese: int) -> List[Day]:
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

    return days    
    
#Funzione per restituire i dati dell'excek (array of array)
def Lettura_Excel_Cure(path: str):
    df = pd.read_excel(path)
    data = df.values.tolist()
    return data

#Funzione per la cancellazione delle vecchie schede generate in formato pdf in formato html
def Cancella_Vecchie_Schede_HTML():
    directory = "./Schede_generate"

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".html"):
            os.remove(file_path)

#Funzione per la cancellazione delle vecchie schede generate in formato pdf
def Cancella_Vecchie_Schede_PDF():
    directory = "./Schede_generate"

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".pdf"):
            os.remove(file_path)

#Funzione per la creazione delle schede di cura
def Creazione_Schede(data_scheda, calendar: List[Day], mese: str, anno: int):

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

#Funzione per la conversione delle schede in formato PDF
def Creazione_Schede_PDF():
    directory = "./Schede_generate"

    print("Conversione in PDF delle schede generate...")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        name, ext = os.path.splitext(filename)    
        pdfkit.from_file(file_path, f"{directory}/{name}.pdf", options={"enable-local-file-access": ""})
    
    print("Conversione PDF eseguita")

#Funzione per la creazione di un solo PDF con tutte le schede
def Accoda_PDF(mese, anno: str):
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
    
    print("PDF con schede cura generato")

#Funzione per la creazione della scheda vuota in formato HTML
def Cancella_Vecchia_Scheda_Vuota_HTML(directory: str):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".html"):
            os.remove(file_path)

#Funzione per la creazione della scheda vuota in formato PDF
def Cancella_Vecchia_Scheda_Vuota_PDF(directory: str):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".pdf"):
            os.remove(file_path)

#Funzione per la creazione di una scheda di cura vuota
def Creazione_Scheda_Vuota(calendar: List[Day], mese: str, anno: int):

    #Carico template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("scheda_cure_vuota.html")

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
    with open(f"./Scheda_cure_vuota/{mese}_{str(anno)}_Vuota.html", "w") as f:
        f.write(output)
    
    print(f"Report generated: {mese}_{str(anno)}_Vuota.html")   

#Funzione per la creazione di una scheda di cura vuota 2
def Creazione_Scheda_Vuota_2(calendar: List[Day], mese: str, anno: int):

    #Carico template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("scheda_cure_vuota_2.html")

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
    with open(f"./Scheda_cure_vuota_2/{mese}_{str(anno)}_Vuota_2.html", "w") as f:
        f.write(output)
    
    print(f"Report generated: {mese}_{str(anno)}_Vuota_2.html")   

#Funzione per la conversione della scheda in PDF
def Creazione_Scheda_Vuota_PDF(directory: str):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        name, ext = os.path.splitext(filename)    
        pdfkit.from_file(file_path, f"{directory}/{name}.pdf")         

if __name__ == "__main__":
    main()