from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

PROMPTS_DIR = BASE_DIR / "Prompts"
FEEDBACK_DIR = BASE_DIR / "Feedbacks"

STAKEHOLDER_PROMPTS_DIR = PROMPTS_DIR / "Stakeholder-Mapping"
VALUE_CHAIN_PROMPTS_DIR = PROMPTS_DIR / "Wertschöpfungskette"
MATERIALITY_PROMPTS_DIR = PROMPTS_DIR / "Matrialitätsbewrtung"
RELEVANCE_TEMPLATES_DIR = PROMPTS_DIR / "relevanzMusters"

STAKEHOLDER_FEEDBACK_DIR = FEEDBACK_DIR / "Stakeholder-Mapping"
VALUE_CHAIN_FEEDBACK_DIR = FEEDBACK_DIR / "wirschöpfungskette"
MATERIALITY_FEEDBACK_DIR = FEEDBACK_DIR / "materialität"

COMPLETENESS_PROMPT_FILE = PROMPTS_DIR / "vollständigkeitsprüfung.txt"
RELEVANCE_PROMPT_FILE = PROMPTS_DIR / "relevanz_prompt"

LSME_THEMEN_FILE = PROJECT_ROOT / "LSME_Themen.xlsx"
STAKEHOLDER_LISTE_FILE = PROJECT_ROOT / "Stakeholder_Liste.xlsx"
