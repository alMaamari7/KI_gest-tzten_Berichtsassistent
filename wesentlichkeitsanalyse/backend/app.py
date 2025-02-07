import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
from docx import Document
from DoupleMateriality import DoupleMateriality
import time

# 🔹 Initialisierung von Session-State
def init_session_state():
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "combined_data" not in st.session_state:
        st.session_state.combined_data = ""
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "step_1" not in st.session_state:
        st.session_state.step_1 = False
    if "step_2" not in st.session_state:
        st.session_state.step_2 = False
    if "step_3" not in st.session_state:
        st.session_state.step_3 = False


        # 🔹 Extraktion von Text aus Dateien
def extract_text(file):
    file_extension = file.name.split(".")[-1].lower()
    if file_extension == "pdf":
        import PyPDF2
        reader = PyPDF2.PdfReader(BytesIO(file.read()))
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_extension == "docx":
        doc = Document(BytesIO(file.read()))
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_extension in ["txt", "csv"]:
        return file.getvalue().decode("utf-8")
    elif file_extension in ["xlsx", "xls"]:
        df = pd.read_excel(file)
        return df.to_csv(index=False)
    else:
        return None

def parse_csv_string(csv_string: str):
        """Parst einen CSV-String und gibt eine Liste von DataFrames zurück"""
        tables = csv_string.strip().split("CSV")
        dataframes = []

        for table in tables:
            lines = [line.strip() for line in table.strip().split("\n") if line.strip()]
            if lines:
                try:
                    df = pd.DataFrame([line.split(",") for line in lines[1:]], columns=lines[0].split(","))
                    dataframes.append(df)
                except Exception as e:
                    st.error(f"⚠️ Fehler beim Verarbeiten einer Tabelle: {str(e)}")
                    st.text("\n".join(lines))  # Debugging: Zeigt die fehlerhaften Daten an

        return dataframes
def preprocess_llm_csv(raw_table):
    """
    Bereinigt die LLM-Antwort, um sie in ein valides CSV-Format für `split_csv_tables()` zu überführen.
    """
    # 1️⃣ Entferne Markdown-Codeblöcke (` ``` `)
    cleaned_table = raw_table.replace("```", "").strip()

    # 2️⃣ Füge ein künstliches "CSV"-Trennzeichen ein, um die Split-Funktion zu unterstützen
    if "Stakeholder-Gruppe" in cleaned_table:  # Falls es die Tabelle ist
        cleaned_table = "CSV\n" + cleaned_table

    # 3️⃣ Entferne doppelte oder überflüssige Leerzeilen
    cleaned_table = "\n".join([line.strip() for line in cleaned_table.split("\n") if line.strip()])

    return cleaned_table
# 🔹 Verarbeitung der Daten für Schritt 1
def process_step_1():
    doupleMateriality = DoupleMateriality()

    if not st.session_state.get("combined_data"):
        st.error("⚠️ Keine Daten vorhanden. Bitte laden Sie zuerst eine Datei hoch.")
        return

    if not st.session_state.get("results"):  # Falls results nicht existiert, erstelle es
        st.session_state.results = {}

    if not st.session_state.get("step_1", False):  # Falls step_1 nicht gesetzt ist
        if st.button("🔍 Starte Stakeholder-Analyse"):
            with st.spinner("🔄 Verarbeitung läuft..."):
                result = doupleMateriality.step_1(st.session_state.combined_data)
                 # Wartezeit für LLM-Prozesse

                # 🔹 Ergebnisse trennen
                muster_1 = result.get("musters")
                tabelle_1 = result.get("Stakeholder-Table")
                #tabelle_1 = preprocess_llm_csv(tabelle_1)
                # 🔹 Tabellen parsen
                stakeholder_viewe = parse_csv_string(tabelle_1) if tabelle_1 else {}
                if not stakeholder_viewe:
                    print("❌ Fehler: `split_csv_tables()` hat keine Tabellen zurückgegeben! LLM-Antwort prüfen:",
                          tabelle_1)

                # 🔹 Ergebnisse speichern
                #st.session_state.results["step_1"] = result
                st.session_state.results["step_1_tables"] = stakeholder_viewe
                st.session_state.results["muster_1"] = muster_1
                st.session_state.step_1 = True  # Markiere Schritt 1 als abgeschlossen

            st.rerun()


def process_step_2():
    doupleMateriality = DoupleMateriality()

    # Schritt 2 darf nur starten, wenn Schritt 1 abgeschlossen ist
    if not st.session_state.step_1:
        st.warning("⚠️ Bitte zuerst die Stakeholder-Analyse (Schritt 1) abschließen.")
        return

    if not st.session_state.step_2:
        if st.button("🔍 Starte Wertschöpfungskettenanalyse"):
            with st.spinner("🔄 Verarbeitung läuft..."):
                value_chain = doupleMateriality.step_2(
                    str(st.session_state["results"].get("Stakeholder-Table")),
                    st.session_state.combined_data,
                    str(st.session_state.get("muster_1"))
                )


                # 🔹 Ergebnisse trennen
                muster_2 = value_chain.get("musters")
                tabelle_2 = value_chain.get("ValueChain-Table")

                # 🔹 Tabellen parsen
                value_chain_viewe = parse_csv_string(tabelle_2) if tabelle_2 else {}

                # 🔹 Ergebnisse speichern
                #st.session_state.results["step_2"] = value_chain
                st.session_state.results["step_2_tables"] = value_chain_viewe
                st.session_state.results["muster_2"] = muster_2
                st.session_state.step_2 = True

            st.rerun()


def process_step_3():
    doupleMateriality = DoupleMateriality()

    if not st.session_state.get("step_2"):
        st.warning("⚠️ Bitte zuerst die Wertschöpfungskettenanalyse (Schritt 2) abschließen.")
        return

    if not st.session_state.get("step_3", False):
        if st.button("🔍 Starte Materialitätsanalyse"):
            with st.spinner("🔄 Verarbeitung läuft..."):
                result = doupleMateriality.step_3(
                    st.session_state.combined_data,
                    str(st.session_state["results"].get("Stakeholder-Table")),
                    str(st.session_state["results"].get("ValueChain-Table")),
                    str(st.session_state.get("muster_2"))
                )


                # 🔹 Ergebnisse trennen
                muster_3 = result.get("musters")
                tabelle_3 = result.get("Stakeholder-Table")

                # 🔹 Tabellen parsen
                materiality_viewe = parse_csv_string(tabelle_3) if tabelle_3 else {}

                # 🔹 Ergebnisse speichern
                st.session_state.results["step_3"] = result
                st.session_state.results["step_3_tables"] = materiality_viewe
                st.session_state.results["muster_3"] = muster_3
                st.session_state.step_3 = True

            st.rerun()





def display_results():
    if "results" not in st.session_state:
        st.warning("⚠️ Keine Ergebnisse vorhanden. Bitte führen Sie die Analysen zuerst durch.")
        return

    step_names = {
        "step_1_tables": ["Stakeholder-Gruppe", "Stakeholder-Anliegen", "Anliegen ohne Stakeholder", "Stakeholder-Anliegen-Bewertung"],
        "step_2_tables": ["Bereich_Prozess/Aktivität", "ESG-Risiko und Chancen", "Themen mit Fehlenden Daten"],
        "step_3_tables": ["Impact-Wesentlichkeit", "Finanzielle Wesentlichkeit", "Doppelte Wesentlichkeitsanalyse"]
    }

    # 🔹 **Schritt 1**
    if "step_1_tables" in st.session_state.results:
        st.success("✅ Stakeholder-Analyse erfolgreich abgeschlossen!")
        tables = st.session_state.results.get("step_1_tables", [])

        if not tables:
            st.warning("⚠️ Keine Tabellen gefunden.")
        else:
            for name, df in zip(step_names["step_1_tables"], tables):
                st.write(f"📊 **{name}**")
                st.dataframe(df)

    # 🔹 **Schritt 2**
    if "step_2_tables" in st.session_state.results:
        st.success("✅ Wertschöpfungskettenanalyse erfolgreich abgeschlossen!")
        tables = st.session_state.results.get("step_2_tables", [])

        if not tables:
            st.warning("⚠️ Keine Tabellen gefunden.")
        else:
            for name, df in zip(step_names["step_2_tables"], tables):
                st.write(f"📊 **{name}**")
                st.dataframe(df)

    # 🔹 **Schritt 3**
    if "step_3_tables" in st.session_state.results:
        st.success("✅ Materialitätsanalyse erfolgreich abgeschlossen!")
        tables = st.session_state.results.get("step_3_tables", [])

        if not tables:
            st.warning("⚠️ Keine Tabellen gefunden.")
        else:
            for name, df in zip(step_names["step_3_tables"], tables):
                st.write(f"📊 **{name}**")
                st.dataframe(df)


# 🔹 Hauptfunktion für das UI
def main():
    st.title("📊 Doppelte Materialitätsanalyse")
    init_session_state()

    # Datei-Upload
    uploaded_files = st.file_uploader(
        "📂 Dateien hochladen", type=["pdf", "docx", "txt", "csv", "xlsx"], accept_multiple_files=True
    )

    # Verarbeitung der hochgeladenen Dateien
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in [f.name for f in st.session_state.uploaded_files]:
                text = extract_text(file)
                if text:
                    st.session_state.combined_data += "\n" + text
                    st.session_state.uploaded_files.append(file)
                    st.success(f"✅ {file.name} erfolgreich hochgeladen und verarbeitet.")

    # Gespeicherte Daten anzeigen
    if st.session_state.combined_data:
        with st.expander("🔍 Gespeicherte Daten anzeigen"):
            st.text_area("Daten", st.session_state.combined_data, height=150)

    # Verarbeitung von Schritt 1 starten
        # Nur Button anzeigen, wenn Daten vorhanden sind
        if st.session_state.combined_data:
            process_step_1()

        # Schritt 2 nur anzeigen, wenn Schritt 1 abgeschlossen wurde
        if st.session_state.step_1:
            process_step_2()

        if st.session_state.step_2:
            process_step_3()

    # Ergebnisse anzeigen
    display_results()


if __name__ == "__main__":
    main()


