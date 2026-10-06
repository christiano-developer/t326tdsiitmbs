"""Rule-based sentiment: happy / sad / neutral via weighted keyword and phrase lexicons.

Scoring: +1 per happy cue, -1 per sad cue (phrases checked first, then single words; a negator just
before a word flips it). score > 0 -> happy, < 0 -> sad, else neutral (factual statements have no cues).
"""
import re

HAPPY_PHRASES = [
    "dream come true", "tears of joy", "cloud nine", "ear to ear", "jumping for joy", "can't stop smiling",
    "best day", "exceeded all my expectations", "exactly what i was hoping", "happiest moment",
    "bursting with excitement", "radiating with happiness", "changed my life", "went perfectly",
]
SAD_PHRASES = [
    "worst experience", "passed away", "falling apart", "heart is broken", "nobody showed up", "turns to failure",
    "lost everything", "empty inside", "worse than expected", "ended badly", "massive layoffs",
    "drowning in sorrow", "consumed by grief", "lost my",
]
HAPPY_WORDS = {
    "love", "loved", "lovely", "excited", "exciting", "excitement", "joy", "joyful", "thrilled", "best", "amazing",
    "grateful", "fantastic", "overjoyed", "wonderful", "proud", "happiest", "happy", "happiness", "delighted",
    "blessed", "bliss", "ecstatic", "beautiful", "smiling", "smile", "fortunate", "great", "awesome", "perfect",
    "perfectly", "excellent", "glad", "winning", "won", "celebrate", "enjoy", "enjoyed", "incredible", "brilliant",
    "promotion", "engagement", "grinning", "hoping", "accomplished", "surprise", "good", "nice", "pleased",
    "alive", "energized", "spectacular", "thrive", "thriving", "cheerful", "elated", "marvelous", "superb",
}
SAD_WORDS = {
    "worst", "heartbroken", "failed", "fail", "failure", "terrible", "rejected", "devastated", "regret", "layoffs",
    "disappointed", "disappointing", "diagnosis", "lonely", "abandoned", "depression", "depressed", "badly",
    "hopeless", "crying", "cry", "pain", "painful", "miserable", "exhausted", "traumatized", "accident", "defeated",
    "sorrow", "empty", "anxiety", "anxious", "fire", "grief", "sad", "sadness", "awful", "horrible", "hate",
    "broken", "lost", "suffering", "struggling", "unhappy", "upset", "angry", "bad", "poor", "worse", "tragic",
    "worried", "worry", "shattered", "betrayal", "betrayed", "crushed", "disappointment", "burdened", "problems",
    "grieving", "despair", "heartache", "ruined", "gloomy",
}
NEGATORS = {"not", "no", "never", "don't", "didn't", "isn't", "wasn't", "can't", "won't", "nothing"}


def classify(sentence: str) -> str:
    text = sentence.lower()
    score = 0
    for p in HAPPY_PHRASES:
        if p in text:
            score += 2
            text = text.replace(p, " ")
    for p in SAD_PHRASES:
        if p in text:
            score -= 2
            text = text.replace(p, " ")
    words = re.findall(r"[a-z']+", text)
    for i, w in enumerate(words):
        sign = 1 if w in HAPPY_WORDS else -1 if w in SAD_WORDS else 0
        if sign and i > 0 and words[i - 1] in NEGATORS:
            sign = -sign
        score += sign
    return "happy" if score > 0 else "sad" if score < 0 else "neutral"
