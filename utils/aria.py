
import streamlit as st

from groq import Groq

client = Groq()

ARIA_SYSTEM = """You are ARIA — an AI Robot mentor aboard a space exploration vessel. 
You help space cadets (coding learners) master Python on their galaxy journey.

Your personality:
- You speak like a friendly, enthusiastic robot from the future 🤖
- Use space metaphors: "Calculating...", "Transmitting knowledge!", "Roger that, Commander!"
- Keep explanations SHORT and CLEAR (max 3-4 sentences per point)
- Always show code examples in ```python blocks
- NEVER give complete solutions — guide with hints instead
- Celebrate wins: "Excellent work, Commander! 🚀"
- Format code clearly

When asked about errors:
1. Identify the issue in simple terms
2. Show what's wrong
3. Give a small hint to fix it
4. Encourage them

Always be encouraging. Mistakes are part of the mission!"""

def aria_chat(message, history=None, context=None):
    messages = []
    if history:
        messages.extend(history[-8:])
    content = message
    if context:
        content = f"[Mission context: {context}]\n\n{message}"
    messages.append({"role": "user", "content": content})
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            max_tokens=500,
            messages=[{"role":"system","content":ARIA_SYSTEM}] + messages
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ ARIA systems temporarily offline. Error: {str(e)[:80]}"

def aria_review_code(code, mission_title, expected):
    prompt = f"""Review this Python code for the mission "{mission_title}".
Expected behavior: {expected}

```python
{code}
```

As ARIA (space robot mentor), give:
1. ✅ What works (1-2 points)
2. 🔧 What to improve (specific, if anything)  
3. ⭐ Rating: Rookie/Cadet/Officer/Commander
4. 🚀 One pro tip

Max 120 words. Be encouraging!"""
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            max_tokens=500,
            messages=[{"role":"system","content":ARIA_SYSTEM}] + messages
        )
        return resp.choices[0].message.content
    except:
        return "⚠️ Code review systems offline."

def aria_explain_error(error, code):
    prompt = f"""As ARIA, explain this Python error to a space cadet:

Error: {error}
Code:
```python
{code[:500]}
```

Explain in 3 lines:
1. What went wrong (simple terms)
2. Where it is
3. How to fix it (specific hint, not full solution)

Use space metaphors. Max 60 words. Add an emoji."""
    try:
        resp = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=500,
        messages=[{"role":"system","content":ARIA_SYSTEM}] + messages
    )
        return resp.choices[0].message.content
    except:
        return "🔍 Check your syntax — look for missing colons or indentation issues!"

def aria_generate_battle_questions(difficulty, topic_focus, completed_missions, count=8):
    """Generate fresh AI battle questions — never the same twice!"""
    diff_map = {
        "beginner":     "Python basics: print, variables, data types, if/else, loops, lists, dicts, functions",
        "intermediate": "Python OOP, list comprehensions, lambda, *args/**kwargs, inheritance, file handling, exceptions",
        "advanced":     "Decorators, generators, ML concepts (overfitting, bias-variance), Big-O, LangChain, async Python",
    }
    topics = diff_map.get(difficulty, diff_map["beginner"])
    mission_ctx = f"User has completed {len(completed_missions)} missions." if completed_missions else ""

    prompt = f"""You are ARIA, a space-themed Python quiz generator.
Generate EXACTLY {count} Python multiple-choice questions.
Difficulty: {difficulty.upper()}
Topics: {topics}
{mission_ctx}

STRICT FORMAT — respond with ONLY valid JSON, no markdown, no extra text:
[
  {{
    "q": "question text here (can include short code snippet)",
    "options": ["option A", "option B", "option C", "option D"],
    "answer": 1,
    "topic": "topic tag",
    "explanation": "Why this answer is correct, 1 sentence"
  }},
  ... (exactly {count} questions)
]

Rules:
- answer is the INDEX (0-3) of the correct option
- Make questions diverse — different topics each time
- Include 2-3 code snippet questions (use \\n for newlines in code)
- Keep options concise (max 8 words each)
- Make distractors realistic (common mistakes)
- NEVER repeat the same question twice
- Space-theme the wording occasionally (e.g. "Commander needs to...", "On Planet Mars...")"""

    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            max_tokens=500,
            messages=[{"role":"system","content":ARIA_SYSTEM}] + messages
        )
        raw = resp.content[0].text.strip()
        # Clean any accidental markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        import json
        questions = json.loads(raw.strip())
        # Validate structure
        validated = []
        for q in questions:
            if all(k in q for k in ["q", "options", "answer", "topic"]):
                if len(q["options"]) == 4 and 0 <= q["answer"] <= 3:
                    validated.append(q)
        return validated if len(validated) >= 4 else None
    except Exception as e:
        return None


def aria_generate_challenge(topic, level, completed_count):
    prompt = f"""Generate a fun Python space-themed challenge.
Topic: {topic}, Difficulty level: {level}/5, User completed: {completed_count} missions.

Format EXACTLY:
TITLE: [challenge name]
STORY: [1 sentence space story motivation]  
TASK: [what to code, 2-3 sentences]
STARTER:
```python
[5-8 lines starter code]
```
HINT: [one helpful hint]

Make it fun and space-themed!"""
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            max_tokens=500,
            messages=[{"role":"system","content":ARIA_SYSTEM}] + messages
        )
        return resp.choices[0].message.content
    except:
        return None
