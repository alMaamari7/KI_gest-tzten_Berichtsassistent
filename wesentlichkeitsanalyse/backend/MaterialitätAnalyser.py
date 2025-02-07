from pathlib import Path
from typing import List
import os
import pandas as pd
from OpenAIHelper import OpenAIHelper
import time


class MaterialitaetAnalyser:
    def __init__(self):
        pass



    def materialtaetpruefung(self, stakeholder, value_chain, nutzerdaten, muster):
        ai_helper = OpenAIHelper()


        material = self.nutzerdata_lesen(nutzerdaten, "materialitätsprüfung")
        all_muster = str(muster) + "\n\n---\n" + material
        #print(all_muster)


        for i in range(3):

          impact_analyser = (
            "Du bist ein Nachhaltigkeitsexperte mit Fokus auf die Impact-Wesentlichkeit nach ESRS. Dein Ziel ist es, die Auswirkungen eines Unternehmens auf Umwelt, Gesellschaft und Stakeholder zu bewerten.."
            " Du arbeitest präzise und flexibel, um sowohl explizite als auch implizite Stakeholder zu erfassen.")

          with open(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Matrialitätsbewrtung\Matrialitätsbewertung","r", encoding="utf-8") as f:
            prompt = f.read()
            impact_prompt = prompt
            impact_prompt = impact_prompt.replace("<Muster>", str(all_muster) if all_muster else "Keine MusterDaten")
            impact_prompt = impact_prompt.replace("<Stakeholder>", str(stakeholder) if stakeholder else "Keine StakeholderDaten")
            impact_prompt = impact_prompt.replace("<daten>", str(nutzerdaten) if nutzerdaten else "Keine NutzerDaten")
            response_impact_prompt = ai_helper.get_openai_response(impact_analyser,impact_prompt)
            bewertung = self.vollstaendigkeit(prompt, response_impact_prompt)
            self.save_response_to_file(str(bewertung), r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\materialität\impact")
            time.sleep(30)
        self.delete_saved_responses(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\materialität\impact")
        print(response_impact_prompt)

        for i in range(3):
          financal_analyser = (
            "Du bist ein Finanzanalyst mit Expertise in ESG-Risiken und finanzieller Wesentlichkeit. Dein Ziel ist es, die finanziellen Auswirkungen von ESG-Themen auf das Unternehmen zu bewerten."
            " Du arbeitest präzise und flexibel, um sowohl explizite als auch implizite Stakeholder zu erfassen.")

          with open(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Matrialitätsbewrtung\Finanziele_Impact", "r", encoding="utf-8") as f:
            prompt = f.read()
            financal_prompt = prompt
            financal_prompt = financal_prompt.replace("<Muster>", str(all_muster) if all_muster else "Keine MusterDaten" )
            financal_prompt = financal_prompt.replace("<ESG>", str(value_chain) if value_chain else "Keine ESGDaten")
            financal_prompt = financal_prompt.replace("<daten>", str(nutzerdaten) if nutzerdaten else "Keine NutzerDaten")
            response_financal_prompt = ai_helper.get_openai_response(financal_analyser, financal_prompt)
            bewertung = self.vollstaendigkeit(prompt,response_financal_prompt)
            self.save_response_to_file(str(bewertung),r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\materialität\finance")
            time.sleep(30)
        self.delete_saved_responses(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\materialität\finance")
        print(response_financal_prompt)


        for i in range(3):
          financal_impact_zusammenfuehrer = (
            "Du bist ein Nachhaltigkeits- und Finanzanalyst, spezialisiert auf die doppelte Wesentlichkeit. Dein Ziel ist es, die Impact- und finanzielle Wesentlichkeit zu kombinieren und die Themen zu priorisieren."
            " Du arbeitest präzise und flexibel, um sowohl explizite als auch implizite Stakeholder zu erfassen.")

          with open(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Matrialitätsbewrtung\impact_und_finanziel_tabelle","r", encoding="utf-8") as f:
            prompt = f.read()
            financal_impact_prompt = prompt
            financal_impact_prompt = financal_impact_prompt.replace("<Finance>", str(response_financal_prompt) if all_muster else "Keine FinanceDaten" )
            financal_impact_prompt = financal_impact_prompt.replace("<Impact>", str(response_impact_prompt) if value_chain else "Keine ImpactDaten")
            response_financal_impact_prompt = ai_helper.get_openai_response(financal_impact_zusammenfuehrer, financal_impact_prompt)
            bewertung = self.vollstaendigkeit(prompt,response_financal_impact_prompt)
            self.save_response_to_file(str(bewertung), r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\materialität\impact_finance")
            time.sleep(30)
        self.delete_saved_responses(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\materialität\impact_finance")
        print(response_financal_impact_prompt)



        table= str(response_impact_prompt) + str(response_financal_prompt)+str(response_financal_impact_prompt)
        spaltenname= ("Thema,Schweregrad, Reichweite, Irreparabilität,Wahrscheinlichkeit,Gesamtscore,Impact-Wesentlichkeit,Priorität,Empfohlene Maßnahme" 
                      "Thema,Finanzielle Größenordnung,Wahrscheinlichkeit,Langfristige Auswirkungen,Gesamtscore Finanzielle Wesentlichkeit,Priorität, Empfohlene Maßnahme"
                      "Thema,Impact-Wesentlichkeit,Finanzielle Wesentlichkeit,Gesamtbewertung,Priorität,LSME-Referenz,Finale empfohlene Maßnahme")
        all_table= self.cvs_maker(table,3, str(spaltenname))
        results = {}
        results["musters"] = all_muster
        results["Stakeholder-Table"] = all_table
        #print(all_table)

        return results



    def vollstaendigkeit(self, soll, ist):
        ai_helper = OpenAIHelper()
        pruefer = (
            "Du bist ein Prüftool für Vollständigkeit und Qualität der LLM-Antworten. "
            "du bist spezialist für die Nachhaltigkeitsberichterstattung nach LSME-ESRS."
        )

        with open(
                r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\vollständigkeitsprüfung.txt",
                "r", encoding="utf-8") as f:
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
                        r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\Matrialitätsbewrtung\csv_maker",
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


    def feedback_lesen(self, path):
        file_path = Path(
            r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Feedbacks\materialität")
        stakeholder_path = file_path / path
        with open(stakeholder_path, "r", encoding="utf-8") as x:
            feedback = x.read()
        return feedback

    def nutzerdata_lesen(self, nutzerdaten, path):
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
                with open(r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\relevanz_prompt","r") as f:
                    relevanz_prompt = f.read()
                    relevanz_prompt = relevanz_prompt.replace("<Daten>", nutzerdaten)
                    # stakeholder_muster einlesen
                    file_path = Path(
                        r"C:\Users\asahm\Desktop\Asaad_HTW\Abschlussarbeit\Berichtserstellung_AI_Berater\wesentlichkeitsanalyse\Prompts\relevanzMusters")
                    stakeholder_path = file_path / path
                    print(stakeholder_path)
                    with open(stakeholder_path, "r", encoding="utf-8") as x:
                        stakeholder_muster = x.read()
                        # Platzhalter ersetzen
                        relevanz_prompt = relevanz_prompt.replace("<Muster>", str(stakeholder_muster))
                        # AI-Antwort abrufen
                        response = ai_helper.get_openai_response(system_role_relevanz,relevanz_prompt)
                        all_muster = str(response)
                # print(all_muster)
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

        test=  """ESG-Kategorie,Risikotyp,Chancen,Impact,Wahrscheinlichkeit,Gesamtbewertung,Priorität
Upstream,Verstöße gegen Arbeitsstandards in Textillieferkette Asien,Soziales (S),Arbeitsbedingungen bei Lieferanten,Verbesserung der Arbeitsbedingungen,2,3,2.2,Mittel
Upstream,Lokale Gemeinschaften klagen über Wasserknappheit in Südamerika,Umwelt (E),Wasserknappheit,Wassermanagementprogramm implementieren,2,2,2.0,Mittel
Upstream,Kritik an fehlender Transparenz bezüglich Rohstoffquellen,Governance (G),Transparenz bei Lieferanten,Erhöhte Transparenz bei Rohstoffquellen,2,2,2.0,Mittel
Interne Prozesse,80 % Verpackungen bestehen aus recycelten Materialien,Umwelt (E),Ressourcennutzung und Kreislaufwirtschaft,Reduzierung von Verpackungsabfällen,2,3,2.2,Mittel
Interne Prozesse,CO₂-Einsparung durch Einsatz erneuerbarer Energien,Umwelt (E),Klimawandel (CO₂-Reduktion),Reduzierung der CO₂-Emissionen,3,2,2.6,Hoch
Downstream,Start eines Biodiversitätsprogramms zur Wiederherstellung geschädigter Ökosysteme,Umwelt (E),Biodiversität und Ökosysteme,Steigerung der Biodiversität,3,3,3.0,Hoch
Downstream,Kritik von NGOs aufgrund mangelnder Transparenz Umweltmaßnahmen,Umwelt (E),Transparenz,Verbesserung der Umweltmaßnahmen-Transparenz,2,3,2.4,Mittel
"""

    m = MaterialitaetAnalyser()
    print(m.materialtaetpruefung(stakeholder_test, test, data))

if __name__ == "__main__":
    main()
