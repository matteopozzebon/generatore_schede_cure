import sys
import calendar
import datetime
from typing import List
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from dataclasses import dataclass

@dataclass
class Day:
    number: int
    name: str

def main(): 
   
    #Controllo che gli argomenti inseriti siano corretti
    Controllo_Argomenti(sys.argv[1], sys.argv[2])

    anno = int(sys.argv[1])
    mese = int(sys.argv[2])

    calendar = Crea_Calendario(anno, mese)

    excel = Lettura_Excel_Cure('./Elenco_cure/Cure.xlsx')

    nome_mese = Trova_Nome_Mese(mese);

    Creazione_Scheda(excel, calendar, nome_mese); 



        
#funzione per il controllo della validità degli argomenti
def Controllo_Argomenti(anno, mese: str):    
    current_year = datetime.date.today().year

    try:
        if len(sys.argv) != 3:
            raise Exception("Il numero di argomenti inseriti non è valido!")

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

    
#Leggo e restituisco un array of array
def Lettura_Excel_Cure(path: str):
    df = pd.read_excel(path)
    data = df.values.tolist()
    return data

def Creazione_Scheda(data_scheda, calendar: List[Day], mese: str):

    #Carico template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("scheda_cure.html")

    for row in data_scheda:
        # Data to inject
        data = {
            "title": mese,
            "days": calendar,
            "days_number": len(calendar),
            "dati": row,
        }

        # Render HTML
        output = template.render(data)

        # Save report
        with open(f".Schede_generate/{row[0]}.html", "w") as f:
            f.write(output)

        print(f"Report generated: {row[0]}.html")       


if __name__ == "__main__":
    main()