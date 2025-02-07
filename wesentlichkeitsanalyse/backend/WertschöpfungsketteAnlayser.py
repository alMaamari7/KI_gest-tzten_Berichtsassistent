from pathlib import Path
from typing import List
import pandas as pd
from OpenAIHelper import OpenAIHelper
import time



class ValueChainAnlayser:
    def __init__(self):
        pass


    def value_chain_mapping(self, stakeholder, nutzerdaten, muster ):
        value_chain = {}
        ai_helper = OpenAIHelper()
        einvironment = self.nutzerdata_lesen(nutzerdaten, "einvironment")
        time.sleep(40)
        governance = self.nutzerdata_lesen(nutzerdaten, "Governance")
        time.sleep(40)
        polices = self.nutzerdata_lesen(nutzerdaten, "polices")
        time.sleep(40)
        social = self.nutzerdata_lesen(nutzerdaten, "Social")
        time.sleep(40)
        wertschoepfungskette = self.nutzerdata_lesen(nutzerdaten, "wertschöpfungskette.txt")
        time.sleep(40)
        all_muster = einvironment +"\n\n---\n" + governance + "\n\n---\n" + polices +"\n\n---\n"+ social +"\n\n---\n"+ wertschoepfungskette +"\n\n---\n" + str(muster)
        #print(all_muster)
        for i in range(3):
          wertschoepfungskette_mapper = (
            "Du bist ein KI-gestütztes Analysetool, das Unternehmen bei der Nachhaltigkeitsberichterstattung unterstützt."
            "Deine Aufgabe ist es, die Wertschöpfungskette eines Unternehmens zu analysieren, relevante Prozesse und Aktivitäten zu identifizieren und diese den Bereichen Upstream, interne Prozesse und Downstream zuzuordnen."
            " Du arbeitest präzise und flexibel, um sowohl explizite als auch implizite Stakeholder zu erfassen.")

          with open( r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse/Prompts/Wertschöpfungskette/Wertschöpfungskette-Mapping","r", encoding="utf-8") as f:
            prompt = f.read()
            wertschoepfungskette_mapper_prompt = prompt
            wertschoepfungskette_mapper_prompt = wertschoepfungskette_mapper_prompt.replace("<Muster>",str(all_muster) if all_muster else "Keine MusterDaten")
            #print(wertschoepfungskette_mapper_prompt)
            #print("\n\n---\n")
            wertschoepfungskette_mapper_prompt = wertschoepfungskette_mapper_prompt.replace("<Daten>",str(nutzerdaten) if nutzerdaten else "Keine Daten")
            #print(wertschoepfungskette_mapper_prompt)
            #print("\n\n---\n")
            wertschoepfungskette_mapper_prompt = wertschoepfungskette_mapper_prompt.replace("<Stakeholder>",str(stakeholder) if stakeholder else "Keine StakeholderDaten")
            feedback = self.feedback_lesen("mapping")
            wertschoepfungskette_mapper_prompt = wertschoepfungskette_mapper_prompt.replace("<Feedback>",str(feedback) if feedback else "Keine FeedbackDaten")
            #print(wertschoepfungskette_mapper_prompt)
            response_mapping_table = ai_helper.get_openai_response(wertschoepfungskette_mapper,wertschoepfungskette_mapper_prompt)
            value_chain["Bereich_Aktivität"]=response_mapping_table
            bewertun = self.vollstaendigkeit(prompt,response_mapping_table)
            self.save_response_to_file(str(bewertun),r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse/Feedbacks/wirschöpfungskette/mapping")
            time.sleep(30)
        print(response_mapping_table)
        self.delete_saved_responses(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse/Feedbacks/wirschöpfungskette/mapping")

        for i in range(2):
          esg_identifiter = (
            "Du bist ein KI-gestütztes Analysetool für Nachhaltigkeitsberichte."
            "Deine Aufgabe ist es, ESG-Risiken und -Chancen entlang der Wertschöpfungskette zu identifizieren und den jeweiligen Bereichen (Upstream, interne Prozesse, Downstream) sowie den passenden Themen und ESG-Kategorien zuzuordnen."
            " Du arbeitest präzise und flexibel, um sowohl explizite als auch implizite Stakeholder zu erfassen.")

          with open( r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse/Prompts/Wertschöpfungskette/identifikation von ESG","r", encoding="utf-8") as f:
            prompt = f.read()
            esg_identifiter_prompt = prompt
            esg_identifiter_prompt = esg_identifiter_prompt.replace("<Muster>",str(all_muster)  if all_muster else "Keine MusterDaten")
            #print(wertschoepfungskette_mapper_prompt)
            #print("\n\n---\n")
            esg_identifiter_prompt = esg_identifiter_prompt.replace("<Daten>",str(nutzerdaten) if nutzerdaten else "Keine Daten")
            #print(wertschoepfungskette_mapper_prompt)
            #print("\n\n---\n")
            esg_identifiter_prompt = esg_identifiter_prompt.replace("<Stakeholder>",str(stakeholder) if stakeholder else "Keine Stakeholder")
            esg_identifiter_prompt = esg_identifiter_prompt.replace("<Mapping-Tabelle>", str(response_mapping_table) if response_mapping_table else "Keine Mapping")
            data = pd.read_excel(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\LSME_Themen.xlsx")
            data_str = data.to_string(index=False)
            esg_identifiter_prompt = esg_identifiter_prompt.replace("<Themen-Liste>", str(data_str) if data_str else "Keine Themen")
            feedback = self.feedback_lesen("risk_chance")
            esg_identifiter_prompt = esg_identifiter_prompt.replace("<Feedback>", str(feedback) if feedback else "Keine Feedback")
            response_esg_risk_chance_table = ai_helper.get_openai_response(esg_identifiter,esg_identifiter_prompt)
            time.sleep(30)
            bewertung = self.vollstaendigkeit(prompt,response_esg_risk_chance_table)
            #print(response_esg_risk_chance_table)
            # print(response_stakeholder_identifiter_pruefer)
            self.save_response_to_file(str(bewertung),
                                       r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse/Feedbacks/wirschöpfungskette/risk_chance")
        #value_chain["ESG_Risk_Chance"] = response_esg_risk_chance_table
        print(response_esg_risk_chance_table)
        self.delete_saved_responses(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse/Feedbacks/wirschöpfungskette/risk_chance")
        table= str(response_mapping_table) + str(response_esg_risk_chance_table)
        spaltenname= ("Bereich,Prozess/Aktivität,Quelle der Information,Anmerkungen" 
                      "Bereich,Thema,ESG-Kategorie,Risikotyp,Chancen,Impact,Wahrscheinlichkeit,Gesamtbewertung,Priorität")
        all_table = self.cvs_maker(table,2, str(spaltenname))
        #print(all_table)
        results = {}
        results["musters"] = all_muster
        results["ValueChain-Table"] = all_table
        #print(all_table)

        return results










    def delete_saved_responses(self, file_path: str):

        try:
            # Datei im Schreibmodus öffnen, ohne Inhalt (Überschreiben)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("")  # Datei mit leerem Inhalt überschreiben

            print(f"✅ Der Inhalt der Datei {file_path} wurde erfolgreich gelöscht.")

        except FileNotFoundError:
            print(f"⚠️ Datei {file_path} existiert nicht.")

        except Exception as e:
            print(f"⚠️ Fehler beim Löschen des Inhalts: {str(e)}")



    def feedback_lesen(self, path):
     file_path = Path(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\wirschöpfungskette")
     stakeholder_path = file_path / path
     with open(stakeholder_path, "r", encoding="utf-8") as x:
        feedback = x.read()
     return feedback





    def nutzerdata_lesen(self, nutzerdaten, path):
        response_stakeholder_muster = ""
        all_muster = ""
        if not nutzerdaten.strip():
            all_muster = "0"
            return all_muster
        else:

          try:
            ai_helper = OpenAIHelper()
           # Systemrolle definieren
            system_role_relevanz = (
                    "Du bist ein KI-System, das Unternehmen bei der Nachhaltigkeitsberichterstellung unterstützt. "
                    "Deine Aufgabe ist es, die hochgeladenen Nutzerdaten zu analysieren und relevante Informationen "
                    "direkt in das unten stehende Relevanz-Muster einzutragen. Das Muster enthält Hinweise, was in jede "
                    "Kategorie gehört. Zusätzlich hast du Zugriff auf Tabellen, die dir für jede Kategorie und jedes "
                    "Unterthema präzise Anforderungen an Vollständigkeit und Detaillierungsgrad liefern."
                )
            # Excel-Tabelle einlesen und konvertieren
            data = pd.read_excel(
                    r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\LSME_Themen.xlsx")
            csv_text = data.to_csv(index=False)
            data_str = data.to_string(index=False)
            with open(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\relevanz_prompt","r") as f:
             relevanz_prompt = f.read()
             relevanz_prompt = relevanz_prompt.replace("<Daten>", nutzerdaten)
             # stakeholder_muster einlesen
             file_path = Path( r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\relevanzMusters")
             stakeholder_path = file_path / path
             print(stakeholder_path)
             with open(stakeholder_path, "r", encoding="utf-8") as x:
              stakeholder_muster = x.read()
             # Platzhalter ersetzen
              relevanz_prompt = relevanz_prompt.replace("<Muster>", str(stakeholder_muster))
                # AI-Antwort abrufen
              response_stakeholder_muster = ai_helper.get_openai_response(system_role_relevanz, relevanz_prompt)
              all_muster =  str(response_stakeholder_muster)
            #print(all_muster)
          except Exception as e:
             print(f"Fehler: {e}")
        return all_muster

    def save_response_to_file(self, response: str, file_path: str):
        try:
            # Vorhandenen Inhalt der Datei lesen
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    existing_content = file.read()
            except FileNotFoundError:
                existing_content = ""  # Falls die Datei nicht existiert, setze einen leeren Inhalt

            # Neuen Inhalt vorbereiten: Neue Antwort an den Anfang setzen
            new_content = f"{response}\n\n---\n" + existing_content

            # Datei mit neuem Inhalt überschreiben
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_content)

            print(f"✅ Antwort erfolgreich gespeichert in {file_path} (am Anfang der Datei)")
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern der Antwort: {str(e)}")



    def vollstaendigkeit(self, soll, ist):
        ai_helper = OpenAIHelper()
        pruefer = (
            "Du bist ein Prüftool für Vollständigkeit und Qualität der LLM-Antworten. "
            "du bist spezialist für die Nachhaltigkeitsberichterstattung nach LSME-ESRS."
        )

        with open(
                r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\vollständigkeitsprüfung.txt","r",encoding="utf-8" ) as f:
            stakeholder_pruefer = f.read()
            stakeholder_pruefer = stakeholder_pruefer.replace("<IST>", str(ist))
            stakeholder_pruefer = stakeholder_pruefer.replace("<SOLL>", str(soll))
            response_stakeholder_identifiter_pruefer = ai_helper.get_openai_response(pruefer, stakeholder_pruefer)


        return str(response_stakeholder_identifiter_pruefer)

    def cvs_maker(self, tabellen, tabellenanzahl, spaltenname):
        def cvs_maker(self, tabellen, tabellenanzahl, spaltenname):
            ai_helper = OpenAIHelper()
            pruefer = (
                "Du bist ein KI-System, das Antworten von einem LLM filtert, um sie in ein maschinenlesbares CSV-Format zu konvertieren.  "
            )
            for i in range(2):
                with open(
                        r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Wertschöpfungskette\csv_maker",
                        "r", encoding="utf-8") as f:
                    csv_maker = f.read()
                    csv_maker = csv_maker.replace("<List>", str(tabellen))
                    # csv_maker = csv_maker.replace("<Anzahl>", str(tabellenanzahl))
                    # csv_maker = csv_maker.replace("<Spaltentabellen>", str(spaltenname))
                    feedback = self.feedback_lesen("csv")
                    csv_maker = csv_maker.replace("<Feedback>", str(feedback))
                    csv = csv_maker

                    response_csv_maker = ai_helper.get_openai_response(pruefer, csv_maker)
                    prufung = self.vollstaendigkeit(csv, response_csv_maker)
                    respnse = self.save_response_to_file(prufung,
                                                         r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\Stakeholder-Mapping\csv")
            self.delete_saved_responses(
                r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\Stakeholder-Mapping\csv")

            return response_csv_maker




def main():
      with open(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Stakeholder-Mapping\testdaten","r") as f:
       data   = f.read()
       with open(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Wertschöpfungskette\stakeholder_test.txt", "r") as x:
           stakeholder_test = x.read()
           s= ValueChainAnlayser()
           r = s.value_chain_mapping(stakeholder_test, data)
           print(r)
           """""
           stakeholder_identifikation = reusult.get("Bereich_Aktivität", "")
           print(stakeholder_identifikation)
           print("---------------------------------------------")
           stakeholder_anliegen = reusult.get("ESG_Risk_Chance", "")
           print(stakeholder_anliegen)
           print("---------------------------------------------")"""






if __name__ == "__main__":
    main()