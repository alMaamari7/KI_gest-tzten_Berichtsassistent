import os

from streamlit import feedback

from OpenAIHelper import OpenAIHelper
from pathlib import Path
from typing import List
import time
import pandas as pd

import yaml

from paths import (
    STAKEHOLDER_PROMPTS_DIR,
    RELEVANCE_TEMPLATES_DIR,
    COMPLETENESS_PROMPT_FILE,
    STAKEHOLDER_FEEDBACK_DIR,
)


class Stakeholder:
    def __init__(self):
        pass


    def stakeholder_mapping(self, nutzerdaten, path="Stakeholder_Muster"):

        response_stakeholder_muster = self.nutzerdata_lesen(
            nutzerdaten,
            [path]
        )

        if response_stakeholder_muster == "0":

            return "Keine Nutzerdaten vorhanden. Bitte geben Sie die erforderlichen Eingaben an."


        #print(response_stakeholder_muster)
        ai_helper = OpenAIHelper()
        nutzerdaten = str(nutzerdaten)

        for i in range(2):
            # Stakeholder identifizieren
            stakeholder_identifiter = (
                "Du bist ein KI-gestütztes Analysetool, das Stakeholder-Gruppen aus bereitgestellten Relevanz-Mustern und Nutzerdaten identifiziert und kategorisiert."
                " Du arbeitest präzise und flexibel, um sowohl explizite als auch implizite Stakeholder zu erfassen."
            )

            with open(
                STAKEHOLDER_PROMPTS_DIR / "Stakeholder_Iderntifkater.txt",
                "r",
                encoding="utf-8"
            ) as f:
                prompt = f.read()

                stakeholder_identifiter_prompt = prompt

                stakeholder_identifiter_prompt = stakeholder_identifiter_prompt.replace(
                    "<Muster>",
                    str(response_stakeholder_muster)
                    if str(response_stakeholder_muster)
                    else "Keine MusterDaten"
                )

                stakeholder_identifiter_prompt = stakeholder_identifiter_prompt.replace(
                    "<Daten>",
                    nutzerdaten
                    if nutzerdaten
                    else "nutzerdaten"
                )

                feedback = self.feedback_lesen(
                    "Stakeholder_identifikation"
                )

                stakeholder_identifiter_prompt = stakeholder_identifiter_prompt.replace(
                    "<Feedback>",
                    str(feedback)
                    if str(feedback)
                    else "Feedbacks"
                )

                response_stakeholder_table = ai_helper.get_openai_response(
                    stakeholder_identifiter,
                    stakeholder_identifiter_prompt
                )


            # Stakeholder identifizieren prüfen
            pruefer = (
                "Du bist ein Prüftool für Vollständigkeit und Qualität der LLM-Antworten. "
                "du bist spezialist für die Nachhaltigkeitsberichterstattung nach LSME-ESRS."
            )

            with open(
                COMPLETENESS_PROMPT_FILE,
                "r",
                encoding="utf-8"
            ) as f:
                stakeholder_pruefer = f.read()

                stakeholder_pruefer = stakeholder_pruefer.replace(
                    "<IST>",
                    str(response_stakeholder_table)
                )

                stakeholder_pruefer = stakeholder_pruefer.replace(
                    "<SOLL>",
                    str(prompt)
                )

                stakeholder_pruefer = stakeholder_pruefer.replace(
                    "<Schrittname>",
                    "Stakeholder identifizieren"
                )

                response_stakeholder_identifiter_pruefer = (
                    ai_helper.get_openai_response(
                        pruefer,
                        stakeholder_pruefer
                    )
                )

                #print(response_stakeholder_identifiter_pruefer)

                self.save_response_to_file(
                    str(response_stakeholder_identifiter_pruefer),
                    STAKEHOLDER_FEEDBACK_DIR / "Stakeholder_identifikation"
                )

        #print(response_stakeholder_table)

        self.delete_saved_responses(
            STAKEHOLDER_FEEDBACK_DIR / "Stakeholder_identifikation"
        )


        for i in range(3):
            # Anliegen zu Stakeholder zuordnen
            stakeholder_anlieger = (
                "Du bist ein KI-gestütztes Analysetool für Nachhaltigkeitsberichte. Deine Aufgabe ist es:"
                "Stakeholder-Anliegen aus den bereitgestellten Dokumenten zu extrahieren."
                "Diese Anliegen den bekannten Stakeholder-Gruppen basierend auf expliziten Verweisen, kontextuellen Hinweisen und assoziativen Verbindungen zuzuordnen. "
                "Anliegen, die keinem Stakeholder zugeordnet werden können, separat zu dokumentieren und für weitere Analysen vorzubereiten."
                "Du arbeitest präzise, strukturiert und berücksichtigst potenzielle Mehrdeutigkeiten, die du entsprechend markierst"
            )

            with open(
                STAKEHOLDER_PROMPTS_DIR / "anliegen_zuordnung.txt",
                "r",
                encoding="utf-8"
            ) as f:
                prompt = f.read()

                stakeholder_anlieger_prompt = prompt

                stakeholder_anlieger_prompt = stakeholder_anlieger_prompt.replace(
                    "<Muster>",
                    str(response_stakeholder_muster)
                    if str(response_stakeholder_muster)
                    else "Kein Musterdaten"
                )

                stakeholder_anlieger_prompt = stakeholder_anlieger_prompt.replace(
                    "<Daten>",
                    nutzerdaten
                    if nutzerdaten
                    else "kein nutzerdaten"
                )

                stakeholder_anlieger_prompt = stakeholder_anlieger_prompt.replace(
                    "<Stakeholder>",
                    str(response_stakeholder_table)
                    if str(response_stakeholder_table)
                    else "Kein Stakeholder"
                )

                feedback = self.feedback_lesen(
                    "Anliegen_zu_Stakholder.txt"
                )

                stakeholder_anlieger_prompt = stakeholder_anlieger_prompt.replace(
                    "<Feedback>",
                    str(feedback)
                    if str(feedback)
                    else "Kein Feedback"
                )

                response_stakeholder_anliegen = (
                    ai_helper.get_openai_response(
                        stakeholder_anlieger,
                        stakeholder_anlieger_prompt
                    )
                )


            # Stakeholder anliegen prüfen
            pruefer = (
                "Du bist ein Prüftool für Vollständigkeit und Qualität der LLM-Antworten. "
                "du bist spezialist für die Nachhaltigkeitsberichterstattung nach LSME-ESRS."
            )

            with open(
                COMPLETENESS_PROMPT_FILE,
                "r",
                encoding="utf-8"
            ) as f:
                stakeholder_pruefer = f.read()

                stakeholder_pruefer = stakeholder_pruefer.replace(
                    "<IST>",
                    str(response_stakeholder_anliegen)
                )

                stakeholder_pruefer = stakeholder_pruefer.replace(
                    "<SOLL>",
                    str(prompt)
                )

                stakeholder_pruefer = stakeholder_pruefer.replace(
                    "<Schrittname>",
                    "Anliegen zu Stakeholder zuordnen"
                )

                response_stakeholder_anlieger_pruefer = (
                    ai_helper.get_openai_response(
                        pruefer,
                        stakeholder_pruefer
                    )
                )

                #print(response_stakeholder_anlieger_pruefer)

                self.save_response_to_file(
                    str(response_stakeholder_anlieger_pruefer),
                    STAKEHOLDER_FEEDBACK_DIR / "Anliegen_zu_Stakholder.txt"
                )

                time.sleep(30)


        #print(response_stakeholder_anliegen)

        self.delete_saved_responses(
            STAKEHOLDER_FEEDBACK_DIR / "Anliegen_zu_Stakholder.txt"
        )


        # Anliegen zu Stakeholder zuordnen
        for i in range(3):

            # Stakeholder_Anliegen bewerten
            stakeholder_relevanzbewerter = (
                "Du bist ein KI-gestütztes Analysetool für Nachhaltigkeitsberichte."
                "Deine Aufgabe ist es, die Relevanz der identifizierten Stakeholder-Anliegen zu bewerten, basierend auf klar definierten Kriterien."
                "Dein Ziel ist es, jedem Anliegen eine Relevanzstufe (Hoch, Mittel, Gering) zuzuweisen und eine priorisierte Stakeholder-Matrix zu erstellen."
            )

            with open(
                STAKEHOLDER_PROMPTS_DIR / "Relevanzbewertung",
                "r",
                encoding="utf-8"
            ) as f:
                prompt = f.read()

                stakeholder_relevanzbewerter_prompt = prompt

                stakeholder_relevanzbewerter_prompt = stakeholder_relevanzbewerter_prompt.replace(
                    "<Anliegen>",
                    str(response_stakeholder_anliegen)
                    if str(response_stakeholder_anliegen)
                    else "Kein Stakeholder-Anliegen"
                )

                stakeholder_relevanzbewerter_prompt = stakeholder_relevanzbewerter_prompt.replace(
                    "<Daten>",
                    nutzerdaten
                    if nutzerdaten
                    else "Kein Nutzerdaten"
                )

                stakeholder_relevanzbewerter_prompt = stakeholder_relevanzbewerter_prompt.replace(
                    "<Muster>",
                    response_stakeholder_muster
                    if str(response_stakeholder_muster)
                    else "Kein Muster"
                )

                feedback = self.feedback_lesen(
                    "Anleigen bewerten"
                )

                stakeholder_relevanzbewerter_prompt = stakeholder_relevanzbewerter_prompt.replace(
                    "<Feedback>",
                    str(feedback)
                    if str(feedback)
                    else "Kein Feedback"
                )

                response_stakeholder_relevantz_bewertung = (
                    ai_helper.get_openai_response(
                        stakeholder_relevanzbewerter,
                        stakeholder_relevanzbewerter_prompt
                    )
                )


                pruefer = (
                    "Du bist ein Prüftool für Vollständigkeit und Qualität der LLM-Antworten. "
                    "du bist spezialist für die Nachhaltigkeitsberichterstattung nach LSME-ESRS."
                )

                with open(
                    COMPLETENESS_PROMPT_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:
                    stakeholder_pruefer = f.read()

                    stakeholder_pruefer = stakeholder_pruefer.replace(
                        "<IST>",
                        str(response_stakeholder_relevantz_bewertung)
                    )

                    stakeholder_pruefer = stakeholder_pruefer.replace(
                        "<SOLL>",
                        str(prompt)
                    )

                    stakeholder_pruefer = stakeholder_pruefer.replace(
                        "<Schrittname>",
                        "Stakeholder Anliegen bewerten"
                    )

                    response_stakeholder_identifiter_pruefer = (
                        ai_helper.get_openai_response(
                            pruefer,
                            stakeholder_pruefer
                        )
                    )

                    #print(response_stakeholder_identifiter_pruefer)

                    self.save_response_to_file(
                        str(response_stakeholder_identifiter_pruefer),
                        STAKEHOLDER_FEEDBACK_DIR / "Anleigen bewerten"
                    )

                    time.sleep(30)


        #print(response_stakeholder_relevantz_bewertung)

        self.delete_saved_responses(
            STAKEHOLDER_FEEDBACK_DIR / "Anleigen bewerten"
        )

        stakeholder_dict = (
            str(response_stakeholder_table)
            + str(response_stakeholder_anliegen)
            + str(response_stakeholder_relevantz_bewertung)
        )

        #print(stakeholder_dict)

        spaltennamen = (
            "Stakeholder-Gruppe,Intern/Extern,Kategorie Direkt/Indirekt"
            "Stakeholder-Gruppe,Anliegen,ESG-Thema,\tESG-Kategorie"
            "Anliegen,Fehlende Daten,Status"
            "Anliegen,Wahrscheinlichkeit und Schwere,Finanzielle Materialität,"
            "Stakeholder-Perspektiven,Strategische Relevanz,Gesamtbewertung von 3.0,"
            "Priorität"
        )

        all_table = self.cvs_maker(
            stakeholder_dict,
            4,
            spaltennamen
        )

        results = {}

        results["musters"] = response_stakeholder_muster
        results["Stakeholder-Table"] = all_table

        #print(all_table)

        return results


    def feedback_lesen(self, path):
        stakeholder_path = STAKEHOLDER_FEEDBACK_DIR / path

        with open(
            stakeholder_path,
            "r",
            encoding="utf-8"
        ) as x:
            feedback = x.read()

        return feedback


    def delete_saved_responses(self, file_path: str):
        try:
            # Datei im Schreibmodus öffnen (Überschreiben)
            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write("")

            print(
                f"✅ Der Inhalt der Datei {file_path} "
                f"wurde erfolgreich gelöscht."
            )

        except FileNotFoundError:
            print(
                f"⚠️ Datei {file_path} existiert nicht."
            )

        except Exception as e:
            print(
                f"⚠️ Fehler beim Löschen des Inhalts: {str(e)}"
            )


    def cvs_maker(self, tabellen, tabellenanzahl, spaltenname):
        ai_helper = OpenAIHelper()

        pruefer = (
            "Du bist ein KI-System, das Antworten von einem LLM filtert, "
            "um sie in ein maschinenlesbares CSV-Format zu konvertieren.  "
        )

        for i in range(2):

            with open(
                STAKEHOLDER_PROMPTS_DIR / "csv_maker",
                "r",
                encoding="utf-8"
            ) as f:

                csv_maker = f.read()

                csv_maker = csv_maker.replace(
                    "<List>",
                    str(tabellen)
                )

                #csv_maker = csv_maker.replace("<Anzahl>", str(tabellenanzahl))
                #csv_maker = csv_maker.replace("<Spaltentabellen>", str(spaltenname))

                feedback = self.feedback_lesen("csv")

                csv_maker = csv_maker.replace(
                    "<Feedback>",
                    str(feedback)
                )

                csv = csv_maker

                #print(csv)

                response_csv_maker = ai_helper.get_openai_response(
                    pruefer,
                    csv_maker
                )

                prufung = self.vollstaendigkeit(
                    csv,
                    response_csv_maker
                )

                respnse = self.save_response_to_file(
                    prufung,
                    STAKEHOLDER_FEEDBACK_DIR / "csv"
                )

        self.delete_saved_responses(
            STAKEHOLDER_FEEDBACK_DIR / "csv"
        )

        return response_csv_maker


    def vollstaendigkeit(self, soll, ist):
        ai_helper = OpenAIHelper()

        pruefer = (
            "Du bist ein Prüftool für Vollständigkeit und Qualität der LLM-Antworten. "
            "du bist spezialist für die Nachhaltigkeitsberichterstattung nach LSME-ESRS."
        )

        with open(
            COMPLETENESS_PROMPT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            stakeholder_pruefer = f.read()

            stakeholder_pruefer = stakeholder_pruefer.replace(
                "<IST>",
                str(ist)
            )

            stakeholder_pruefer = stakeholder_pruefer.replace(
                "<SOLL>",
                str(soll)
            )

            response_stakeholder_identifiter_pruefer = (
                ai_helper.get_openai_response(
                    pruefer,
                    stakeholder_pruefer
                )
            )

        return str(response_stakeholder_identifiter_pruefer)


    def nutzerdata_lesen(self, nutzerdaten, paths: List[str]):
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
                    "Du bist ein KI-System, das Unternehmen bei der "
                    "Nachhaltigkeitsberichterstellung unterstützt. "
                    "Deine Aufgabe ist es, die hochgeladenen Nutzerdaten "
                    "zu analysieren und relevante Informationen "
                    "direkt in das unten stehende Relevanz-Muster einzutragen. "
                    "Das Muster enthält Hinweise, was in jede Kategorie gehört. "
                    "Zusätzlich hast du Zugriff auf Tabellen, die dir für jede "
                    "Kategorie und jedes Unterthema präzise Anforderungen an "
                    "Vollständigkeit und Detaillierungsgrad liefern."
                )

                # Excel-Tabelle einlesen und konvertieren
                data = pd.read_excel(
                    Path(__file__).resolve().parent.parent.parent
                    / "LSME_Themen.xlsx"
                )

                csv_text = data.to_csv(index=False)
                data_str = data.to_string(index=False)

                with open(
                    RELEVANCE_TEMPLATES_DIR.parent / "relevanz_prompt",
                    "r"
                ) as f:

                    relevanz_prompt = f.read()

                    relevanz_prompt = relevanz_prompt.replace(
                        "<Tabelle>",
                        data_str
                    )

                    relevanz_prompt = relevanz_prompt.replace(
                        "<Daten>",
                        nutzerdaten
                    )


                for path in paths:

                    # stakeholder_muster einlesen
                    stakeholder_path = RELEVANCE_TEMPLATES_DIR / path

                    with open(
                        stakeholder_path,
                        "r",
                        encoding="utf-8"
                    ) as x:

                        stakeholder_muster = x.read()

                        # Platzhalter ersetzen
                        relevanz_prompt = relevanz_prompt.replace(
                            "<Muster>",
                            str(stakeholder_muster)
                        )

                        # AI-Antwort abrufen
                        response_stakeholder_muster = (
                            ai_helper.get_openai_response(
                                system_role_relevanz,
                                relevanz_prompt
                            )
                        )

                        all_muster = (
                            all_muster
                            + str(response_stakeholder_muster)
                        )


            except Exception as e:
                print(f"Fehler: {e}")

        return all_muster


    def save_response_to_file(self, response: str, file_path: str):
        try:
            # Vorhandenen Inhalt der Datei lesen
            try:
                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:
                    existing_content = file.read()

            except FileNotFoundError:
                existing_content = ""

            # Neuen Inhalt vorbereiten
            new_content = (
                f"{response}\n\n---\n"
                + existing_content
            )

            # Datei mit neuem Inhalt überschreiben
            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:
                file.write(new_content)

            print(
                f"✅ Antwort erfolgreich gespeichert in "
                f"{file_path} (am Anfang der Datei)"
            )

        except Exception as e:
            print(
                f"⚠️ Fehler beim Speichern der Antwort: {str(e)}"
            )


def main():
    with open(
        STAKEHOLDER_PROMPTS_DIR / "testdaten",
        "r"
    ) as f:

        data = f.read()

        s = Stakeholder()

        stakeholder_results = s.stakeholder_mapping(data)

        print(
            "stakeholder_results"
            + str(stakeholder_results)
        )

        """""
        # Ergebnisse extrahieren
        stakeholder_identifikation = stakeholder_results.get("Stakeholder_identifikation", "")
        print(stakeholder_identifikation)
        print("---------------------------------------------")
        stakeholder_anliegen = stakeholder_results.get("Stakeholder Anliegen", "")
        print(stakeholder_anliegen)
        print("---------------------------------------------")
        stakeholder_bewertung = stakeholder_results.get("Stakeholder Anliegen Bewertung", "")
        print(stakeholder_bewertung)
        print("---------------------------------------------")"""


if __name__ == "__main__":
    main()
