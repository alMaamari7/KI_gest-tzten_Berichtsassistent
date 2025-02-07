
from typing import List, Dict
import pandas as pd
from io import StringIO
import time

from MaterialitätAnalyser import MaterialitaetAnalyser
from Stakeholder import Stakeholder
from WertschöpfungsketteAnlayser import ValueChainAnlayser


class DoupleMateriality ():
    def __init__(self):
        pass



    def step_1(self, nutzerdaten):
        stakeholder = Stakeholder()
        result_stakeholder = stakeholder.stakeholder_mapping(nutzerdaten)
        return result_stakeholder

    def step_2(self, nutzerdaten, stakeholder,muster):
        value_chain = ValueChainAnlayser()
        result_value_chain = value_chain.value_chain_mapping(stakeholder,nutzerdaten, muster)
        return result_value_chain

    def step_3(self, nutzerdaten, stakeholder, value_chain,muster):
        materiality = MaterialitaetAnalyser()
        result_materiality = materiality.materialtaetpruefung(stakeholder, value_chain, nutzerdaten, muster)
        return result_materiality


def main():
    with open(
            r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Stakeholder-Mapping\testdaten",
            "r") as f:
        data = f.read()

    with open(
            r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Wertschöpfungskette\stakeholder_test.txt",
            "r") as x:
        stakeholder_test = x.read()

    with open(
            r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Matrialitätsbewrtung\wertschöpfungstest",
            "r") as y:
        wertscho_test = y.read()

        test = """ESG-Kategorie,Risikotyp,Chancen,Impact,Wahrscheinlichkeit,Gesamtbewertung,Priorität
    Upstream,Verstöße gegen Arbeitsstandards in Textillieferkette Asien,Soziales (S),Arbeitsbedingungen bei Lieferanten,Verbesserung der Arbeitsbedingungen,2,3,2.2,Mittel
    Upstream,Lokale Gemeinschaften klagen über Wasserknappheit in Südamerika,Umwelt (E),Wasserknappheit,Wassermanagementprogramm implementieren,2,2,2.0,Mittel
    Upstream,Kritik an fehlender Transparenz bezüglich Rohstoffquellen,Governance (G),Transparenz bei Lieferanten,Erhöhte Transparenz bei Rohstoffquellen,2,2,2.0,Mittel
    Interne Prozesse,80 % Verpackungen bestehen aus recycelten Materialien,Umwelt (E),Ressourcennutzung und Kreislaufwirtschaft,Reduzierung von Verpackungsabfällen,2,3,2.2,Mittel
    Interne Prozesse,CO₂-Einsparung durch Einsatz erneuerbarer Energien,Umwelt (E),Klimawandel (CO₂-Reduktion),Reduzierung der CO₂-Emissionen,3,2,2.6,Hoch
    Downstream,Start eines Biodiversitätsprogramms zur Wiederherstellung geschädigter Ökosysteme,Umwelt (E),Biodiversität und Ökosysteme,Steigerung der Biodiversität,3,3,3.0,Hoch
    Downstream,Kritik von NGOs aufgrund mangelnder Transparenz Umweltmaßnahmen,Umwelt (E),Transparenz,Verbesserung der Umweltmaßnahmen-Transparenz,2,3,2.4,Mittel
    """





    # die Daten die von Nutzer hochgeladen werden in text umgewandelt und zusammengeführt
    nutzerdaten = ""

    # erste Schritt
    doupleMateriality = DoupleMateriality()
    stakeholder = doupleMateriality.step_1(data)
    print(stakeholder)

    muster_1 = stakeholder["musters"]
    tabelle_1 = stakeholder.get("Stakeholder-Table", "")
    print(tabelle_1)

    # SCV-Tabellen
    stakeholder_viewe = doupleMateriality.split_csv_tables(tabelle_1)
    print("CSV-Funktion")
    print(stakeholder_viewe)

"""""
    time.sleep(60)
    value_chain = doupleMateriality.step_2(str(tabelle_1),data,str(muster_1))
    #print(value_chain)
    time.sleep(60)
    muster_2 = value_chain["musters"]
    tabelle_2 = value_chain["Stakeholder-Table"]
    print(tabelle_2)
    materiality = doupleMateriality.step_3(str(tabelle_1),str(tabelle_2),data,str(muster_2))
    #print(materiality)"""





if __name__ == "__main__":
    main()











