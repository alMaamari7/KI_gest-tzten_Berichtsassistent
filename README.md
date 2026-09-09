# KI-gestützter Berichtsassistent

LLM-basierter Prototyp zur Unterstützung der Nachhaltigkeitsberichterstattung und der Analyse der doppelten Wesentlichkeit.

Dieses Projekt entstand im Rahmen meiner Bachelorarbeit im Studiengang Wirtschaftsinformatik an der HTW Berlin. Ziel war die Entwicklung und Evaluation eines AI-gestützten Prototyps, der unstrukturierte Unternehmens- und Stakeholderinformationen verarbeitet und zentrale Schritte der ESG-Analyse unterstützt.

## Projektüberblick

Der Berichtsassistent verarbeitet unterschiedliche Informationsquellen und führt darauf aufbauend mehrere spezialisierte LLM-Analysen durch.

### Analysepipeline

```text
Unternehmens- und Stakeholderdaten
            │
            ▼
     Dokumentenverarbeitung
            │
            ▼
      Stakeholderanalyse
            │
            ▼
  Wertschöpfungskettenanalyse
            │
            ▼
    Wesentlichkeitsanalyse
            │
            ▼
      Strukturierte Ergebnisse
```

Der Prototyp unterstützt damit mehrere aufeinander aufbauende Schritte der ESG-Analyse und der Vorbereitung einer Analyse der doppelten Wesentlichkeit.

## Zentrale Funktionen

- Verarbeitung von PDF-, DOCX-, TXT-, CSV- und XLSX-Dateien
- LLM-basierte Stakeholderanalyse
- Analyse der Wertschöpfungskette
- Identifikation und Zuordnung relevanter ESG-Themen
- Analyse der Impact Materiality
- Analyse der Financial Materiality
- Unterstützung der Analyse der doppelten Wesentlichkeit
- Strukturierte Verarbeitung der LLM-Ergebnisse
- Iterative Feedback- und Vollständigkeitsprüfungen
- Darstellung der Ergebnisse als strukturierte Tabellen

## LLM-basierte Analysepipeline

Das Projekt verwendet das LLM nicht lediglich als einfachen Chatbot.

Die fachliche Analyse ist in mehrere spezialisierte Verarbeitungsschritte aufgeteilt. Ergebnisse vorheriger Analyseschritte werden für nachfolgende Verarbeitungsschritte verwendet.

Vereinfacht:

```text
Dokumente / Unternehmensdaten
            │
            ▼
    Datenaufbereitung
            │
            ▼
    Stakeholderanalyse
            │
            ▼
 Wertschöpfungskettenanalyse
            │
            ▼
 Wesentlichkeitsanalyse
            │
            ▼
    strukturierte Ergebnisse
```

Für die einzelnen Analyseaufgaben werden spezialisierte Prompts eingesetzt.

## Iterative Qualitätsprüfung

Ein Bestandteil des Prototyps ist die iterative Überprüfung der generierten Ergebnisse.

Dabei werden unter anderem:

- Ergebnisse auf Vollständigkeit geprüft,
- qualitative Rückmeldungen erzeugt,
- weitere Analyseiterationen durchgeführt,
- vorherige Ergebnisse und Feedbackinformationen in nachfolgende Verarbeitungsschritte einbezogen,
- optimierte Ergebnisse anschließend strukturiert weiterverarbeitet.

Der Ansatz dient dazu, die Qualität und Vollständigkeit der LLM-Ergebnisse innerhalb der jeweiligen Analyseaufgaben zu verbessern.

## Dokumentenverarbeitung

Der Prototyp kann verschiedene Dateiformate verarbeiten:

```text
PDF
DOCX
TXT
CSV
XLSX
```

Die Inhalte werden zunächst extrahiert und für die nachfolgenden LLM-Analysen aufbereitet.

Strukturierte Daten werden unter anderem mit Pandas verarbeitet und anschließend für die weiteren Analyseschritte verwendet.

## ESG-Analysen

### Stakeholderanalyse

Die Stakeholderanalyse unterstützt unter anderem:

- Identifikation relevanter Stakeholder
- Zuordnung von Stakeholdergruppen
- Analyse von Stakeholderinteressen und -anliegen
- Bewertung der Relevanz von Stakeholderinformationen

### Wertschöpfungskettenanalyse

Die Wertschöpfungskettenanalyse verarbeitet Informationen zur Wertschöpfungskette und unterstützt deren strukturierte Zuordnung für die weitere ESG-Analyse.

### Wesentlichkeitsanalyse

Auf Grundlage der vorherigen Analyseschritte werden relevante ESG-Themen weiter untersucht.

Der Prototyp unterstützt dabei insbesondere:

- Impact Materiality
- Financial Materiality
- Double Materiality

Die Ergebnisse werden strukturiert aufbereitet und als Tabellen dargestellt.

## Technology Stack

| Bereich | Technologie |
|---|---|
| Programming | Python |
| LLM | OpenAI GPT-3.5-Turbo |
| AI | Large Language Models |
| Prompting | Prompt Engineering |
| UI | Streamlit |
| Data Processing | Pandas |
| PDF Processing | PyPDF2 |
| DOCX Processing | python-docx |
| Excel Processing | OpenPyXL |
| Configuration | Environment Variables |

## Projektstruktur

```text
KI_gest-tzten_Berichtsassistent/
│
├── LSME_Themen.xlsx
├── Stakeholder_Liste.xlsx
├── .env.example
│
└── wesentlichkeitsanalyse/
    │
    ├── Feedbacks/
    ├── Prompts/
    ├── requirements.txt
    │
    └── backend/
        ├── app.py
        ├── OpenAIHelper.py
        ├── Stakeholder.py
        ├── WertschöpfungsketteAnlayser.py
        ├── MaterialitätAnalyser.py
        ├── DoupleMateriality.py
        └── paths.py
```

### Komponenten

| Komponente | Aufgabe |
|---|---|
| `app.py` | Streamlit-Oberfläche und Ablaufsteuerung |
| `OpenAIHelper.py` | Kommunikation mit der OpenAI API |
| `Stakeholder.py` | Stakeholderanalyse |
| `WertschöpfungsketteAnlayser.py` | Wertschöpfungskettenanalyse |
| `MaterialitätAnalyser.py` | Wesentlichkeitsanalyse |
| `DoupleMateriality.py` | Orchestrierung der Analyseschritte |
| `paths.py` | Zentrale Verwaltung der Projektpfade |
| `Prompts/` | Prompts und Vorlagen für die Analysen |
| `Feedbacks/` | Temporäre bzw. gespeicherte Feedbackinformationen |

## Installation

Repository klonen:

```bash
git clone https://github.com/alMaamari7/KI_gest-tzten_Berichtsassistent.git
cd KI_gest-tzten_Berichtsassistent
```

Virtuelle Umgebung erstellen:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Abhängigkeiten installieren:

```bash
pip install -r wesentlichkeitsanalyse/requirements.txt
```

## API-Konfiguration

Eine `.env`-Datei im Projektverzeichnis anlegen:

```text
OPENAI_API_KEY=your_api_key_here
```

Eine Vorlage befindet sich in:

```text
.env.example
```

Der API-Key wird über die Umgebungsvariable `OPENAI_API_KEY` geladen und nicht im Repository gespeichert.

## Anwendung starten

Die Benutzeroberfläche basiert auf Streamlit.

```bash
streamlit run wesentlichkeitsanalyse/backend/app.py
```

Danach kann die Anwendung über die von Streamlit angezeigte lokale Adresse geöffnet werden.

## Evaluation

Der Prototyp wurde im Rahmen der Bachelorarbeit hinsichtlich Genauigkeit, Konsistenz und Effizienz evaluiert.

Ausgewählte Ergebnisse:

| Kennzahl | Ergebnis |
|---|---:|
| Zeitersparnis gegenüber manueller Analyse | 91–93 % |
| Durchschnittliche Konsistenz | 54,81 % |
| Gesamte Abweichungsrate | 31,55 % |
| Stakeholder-Klassifikation | 91,36 % |
| ESG-Themen-Mapping | 79,17 % |

Die Evaluation zeigt insbesondere ein deutliches Potenzial zur Reduzierung des manuellen Analyseaufwands.

Gleichzeitig zeigen die Ergebnisse bei verschiedenen fachlichen Analysen eine begrenzte Konsistenz und Genauigkeit. Die Resultate des Prototyps sollten daher weiterhin durch eine menschliche Prüfung kontrolliert werden.

## Vergleich mit manueller Analyse

Für die untersuchten Testfälle wurde ein erheblicher Unterschied beim Analyseaufwand festgestellt:

```text
Manuelle Analyse
≈ 3,5–4,5 Stunden

Prototyp
≈ 21 Minuten
```

Dies entspricht einer Zeitersparnis von ungefähr 91–93 % für den untersuchten Analyseprozess.

## Bachelorarbeit

**Titel:**  
*Nutzung von LLMs bei der Beratung zur Erstellung von Nachhaltigkeitsberichten*

**Studiengang:** Wirtschaftsinformatik  
**Hochschule:** HTW Berlin  
**Abgabe:** 07.02.2025

Die Bachelorarbeit untersucht den Einsatz von Large Language Models zur Unterstützung von Aufgaben im Kontext der Nachhaltigkeitsberichterstattung.

Der entwickelte Prototyp dient dabei als praktische Grundlage für die Untersuchung der Effizienz, Konsistenz und Qualität LLM-basierter ESG-Analysen.

## Erkenntnisse

Das Projekt zeigt zwei wesentliche Aspekte des Einsatzes von LLMs für strukturierte Fachanalysen:

### Effizienz

LLMs können insbesondere bei der Verarbeitung großer Mengen unstrukturierter Informationen erhebliche Zeitersparnisse ermöglichen.

### Qualitätssicherung

Die Qualität der Ergebnisse hängt stark von der jeweiligen Analyseaufgabe ab. Deshalb sind strukturierte Prompts, Zwischenprüfungen, iterative Verarbeitung und menschliche Kontrolle wichtige Bestandteile eines solchen Systems.

## Projektstatus

Dieses Repository enthält den im Rahmen der Bachelorarbeit entwickelten Prototypen.

Der Schwerpunkt liegt auf der Untersuchung und Evaluation des Einsatzes von LLMs für strukturierte ESG-Analysen und nicht auf einer produktionsreifen Enterprise-Anwendung.

## Disclaimer

Die im Projekt dargestellten AI-Ergebnisse sind prototypische Analyseergebnisse und ersetzen keine fachliche oder rechtliche Prüfung von Nachhaltigkeitsberichten.

---

## Author

**Asaad Al-Maamari**

B.Sc. Wirtschaftsinformatik · HTW Berlin

**Focus:**

```text
AI Engineering
Large Language Models
Prompt Engineering
AI Evaluation
Python
Data Processing
```
