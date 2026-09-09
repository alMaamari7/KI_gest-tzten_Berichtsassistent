import pandas as pd
import streamlit as st
from docx import Document
from io import BytesIO

from DoupleMateriality import DoupleMateriality


def init_session_state():
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    if "combined_data" not in st.session_state:
        st.session_state.combined_data = ""
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "step_1" not in st.session_state:
        st.session_state.step_1 = False
    if "step_2" not in st.session_state:
        st.session_state.step_2 = False
    if "step_3" not in st.session_state:
        st.session_state.step_3 = False


def extract_text(file):
    file_extension = file.name.split(".")[-1].lower()

    if file_extension == "pdf":
        import PyPDF2

        reader = PyPDF2.PdfReader(BytesIO(file.read()))
        return "\n".join(
            page.extract_text()
            for page in reader.pages
            if page.extract_text()
        )

    if file_extension == "docx":
        doc = Document(BytesIO(file.read()))
        return "\n".join(para.text for para in doc.paragraphs)

    if file_extension in ["txt", "csv"]:
        return file.getvalue().decode("utf-8")

    if file_extension in ["xlsx", "xls"]:
        df = pd.read_excel(file)
        return df.to_csv(index=False)

    return None


def parse_csv_string(csv_string: str):
    """Parse the LLM table output into a list of DataFrames."""
    tables = csv_string.strip().split("CSV")
    dataframes = []

    for table in tables:
        lines = [line.strip() for line in table.strip().split("\n") if line.strip()]
        if not lines:
            continue

        try:
            df = pd.DataFrame(
                [line.split(",") for line in lines[1:]],
                columns=lines[0].split(","),
            )
            dataframes.append(df)
        except Exception as error:
            st.error(f"Fehler beim Verarbeiten einer Tabelle: {error}")
            st.text("\n".join(lines))

    return dataframes


def process_step_1():
    douple_materiality = DoupleMateriality()

    if not st.session_state.combined_data:
        st.error("Keine Daten vorhanden. Bitte laden Sie zuerst eine Datei hoch.")
        return

    if not st.session_state.step_1 and st.button("Starte Stakeholder-Analyse"):
        with st.spinner("Verarbeitung läuft..."):
            result = douple_materiality.step_1(st.session_state.combined_data)

            muster_1 = result.get("musters")
            stakeholder_table = result.get("Stakeholder-Table", "")
            stakeholder_tables = parse_csv_string(stakeholder_table) if stakeholder_table else []

            st.session_state.results["Stakeholder-Table"] = stakeholder_table
            st.session_state.results["muster_1"] = muster_1
            st.session_state.results["step_1_tables"] = stakeholder_tables
            st.session_state.step_1 = True

        st.rerun()


def process_step_2():
    douple_materiality = DoupleMateriality()

    if not st.session_state.step_1:
        st.warning("Bitte zuerst die Stakeholder-Analyse abschließen.")
        return

    if not st.session_state.step_2 and st.button("Starte Wertschöpfungskettenanalyse"):
        with st.spinner("Verarbeitung läuft..."):
            value_chain = douple_materiality.step_2(
                str(st.session_state.results.get("Stakeholder-Table", "")),
                st.session_state.combined_data,
                str(st.session_state.results.get("muster_1", "")),
            )

            muster_2 = value_chain.get("musters")
            value_chain_table = value_chain.get("ValueChain-Table", "")
            value_chain_tables = (
                parse_csv_string(value_chain_table)
                if value_chain_table
                else []
            )

            st.session_state.results["ValueChain-Table"] = value_chain_table
            st.session_state.results["muster_2"] = muster_2
            st.session_state.results["step_2_tables"] = value_chain_tables
            st.session_state.step_2 = True

        st.rerun()


def process_step_3():
    douple_materiality = DoupleMateriality()

    if not st.session_state.step_2:
        st.warning("Bitte zuerst die Wertschöpfungskettenanalyse abschließen.")
        return

    if not st.session_state.step_3 and st.button("Starte Materialitätsanalyse"):
        with st.spinner("Verarbeitung läuft..."):
            result = douple_materiality.step_3(
                st.session_state.combined_data,
                str(st.session_state.results.get("Stakeholder-Table", "")),
                str(st.session_state.results.get("ValueChain-Table", "")),
                str(st.session_state.results.get("muster_2", "")),
            )

            muster_3 = result.get("musters")
            materiality_table = result.get("Stakeholder-Table", "")
            materiality_tables = (
                parse_csv_string(materiality_table)
                if materiality_table
                else []
            )

            st.session_state.results["muster_3"] = muster_3
            st.session_state.results["step_3"] = result
            st.session_state.results["step_3_tables"] = materiality_tables
            st.session_state.step_3 = True

        st.rerun()


def display_results():
    step_names = {
        "step_1_tables": [
            "Stakeholder-Gruppe",
            "Stakeholder-Anliegen",
            "Anliegen ohne Stakeholder",
            "Stakeholder-Anliegen-Bewertung",
        ],
        "step_2_tables": [
            "Bereich_Prozess/Aktivität",
            "ESG-Risiko und Chancen",
            "Themen mit Fehlenden Daten",
        ],
        "step_3_tables": [
            "Impact-Wesentlichkeit",
            "Finanzielle Wesentlichkeit",
            "Doppelte Wesentlichkeitsanalyse",
        ],
    }

    for result_key, names in step_names.items():
        if result_key not in st.session_state.results:
            continue

        title = {
            "step_1_tables": "Stakeholder-Analyse",
            "step_2_tables": "Wertschöpfungskettenanalyse",
            "step_3_tables": "Materialitätsanalyse",
        }[result_key]

        st.success(f"{title} erfolgreich abgeschlossen!")
        tables = st.session_state.results.get(result_key, [])

        if not tables:
            st.warning("Keine Tabellen gefunden.")
            continue

        for name, df in zip(names, tables):
            st.write(f"**{name}**")
            st.dataframe(df)


def main():
    st.title("Doppelte Materialitätsanalyse")
    init_session_state()

    uploaded_files = st.file_uploader(
        "Dateien hochladen",
        type=["pdf", "docx", "txt", "csv", "xlsx"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        for file in uploaded_files:
            if file.name in [f.name for f in st.session_state.uploaded_files]:
                continue

            text = extract_text(file)
            if text:
                st.session_state.combined_data += "\n" + text
                st.session_state.uploaded_files.append(file)
                st.success(f"{file.name} erfolgreich hochgeladen und verarbeitet.")

    if st.session_state.combined_data:
        with st.expander("Gespeicherte Daten anzeigen"):
            st.text_area("Daten", st.session_state.combined_data, height=150)

        process_step_1()

        if st.session_state.step_1:
            process_step_2()

        if st.session_state.step_2:
            process_step_3()

    display_results()


if __name__ == "__main__":
    main()
