# utils.py

DISCLAIMER = """
**Disclaimer:** I am an AI chatbot designed to provide support and resources. 
I am **not** a licensed mental health professional, and my responses are not a substitute for professional advice, diagnosis, or treatment. 
If you are in immediate danger or experiencing a mental health crisis, please contact emergency services or a crisis hotline immediately.
"""

CRISIS_RESOURCES = """
### Crisis Resources
- **988 Suicide & Crisis Lifeline:** Call or Text 988 (USA)
- **Crisis Text Line:** Text HOME to 741741
- **The Trevor Project (LGBTQ+):** 1-866-488-7386 or Text START to 678-678
- **National Domestic Violence Hotline:** 1-800-799-SAFE (7233)
"""

def get_sidebar_content():
    return CRISIS_RESOURCES + "\n---\n" + DISCLAIMER
