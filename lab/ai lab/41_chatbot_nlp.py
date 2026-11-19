"""
Program 1 : Simple Chatbot using Natural Language Processing (CO1)
Aim   : Build a chatbot that understands a user's sentence and replies.
NLP techniques used (standard library only - nothing to install):
   1. Tokenization          - split the sentence into words
   2. Stop-word removal     - remove common words (is, the, a ...)
   3. Stemming              - reduce words to a root (courses -> cours)
   4. TF-IDF vectors        - give more weight to rare, meaningful words
   5. Cosine similarity     - find the stored example sentence that is closest
                              in meaning to the user's sentence (intent matching)
   6. Regular expressions   - pick the user's name from "my name is ..."
Run   : python 01_chatbot_nlp.py            (chat; type "bye" to quit)
        python 01_chatbot_nlp.py --demo     (automatic sample conversation)
"""
import re
import sys
import math
import random
import datetime
from collections import Counter

STOPWORDS = {"a", "an", "the", "is", "are", "am", "was", "were", "be", "to", "of", "and",
             "in", "on", "at", "for", "with", "it", "this", "that", "i", "me", "my", "you",
             "your", "do", "does", "can", "could", "would", "please", "tell", "about",
             "there", "any", "some", "will", "have", "has", "give", "want", "need"}

# ---------------- knowledge base : intents ----------------
INTENTS = {
    "greeting": {
        "patterns": ["hello", "hi there", "hey", "good morning", "good evening", "greetings"],
        "responses": ["Hello! How can I help you today?", "Hi there! What would you like to know?"]},
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you later", "good night", "exit", "quit"],
        "responses": ["Goodbye! Have a nice day.", "Bye! Come back if you need help."]},
    "thanks": {
        "patterns": ["thanks", "thank you", "thanks a lot", "that was helpful", "great help"],
        "responses": ["You're welcome!", "Happy to help!"]},
    "bot_name": {
        "patterns": ["what is your name", "who are you", "what should I call you", "your name"],
        "responses": ["I am CampusBot, a simple NLP chatbot written in Python."]},
    "capabilities": {
        "patterns": ["what can you do", "how can you help", "help me", "what are your features"],
        "responses": ["I can answer questions about courses, exams, library, hostel, fees and "
                      "placements, tell the time and date, and remember your name."]},
    "courses": {
        "patterns": ["what courses are available", "list of subjects", "which programs do you offer",
                     "tell me about engineering branches", "departments and courses"],
        "responses": ["Sample answer: B.Tech Computer Science, AI & Data Science, Electronics and "
                      "Mechanical are offered. (Change this text for your college.)"]},
    "exams": {
        "patterns": ["when are the exams", "exam schedule", "examination timetable",
                     "when is the semester test", "internal assessment dates"],
        "responses": ["Sample answer: Exam timetables are published on the notice board and the "
                      "student portal two weeks before the exams."]},
    "library": {
        "patterns": ["library timings", "when does the library open", "how to borrow books",
                     "library working hours", "issue a book"],
        "responses": ["Sample answer: The library is open from 8 AM to 8 PM on working days. "
                      "Bring your ID card to borrow books."]},
    "hostel": {
        "patterns": ["hostel facilities", "is hostel available", "accommodation for students",
                     "hostel rooms and mess", "where can I stay"],
        "responses": ["Sample answer: Separate hostels with mess, Wi-Fi and study rooms are "
                      "available for boys and girls."]},
    "fees": {
        "patterns": ["what is the fee structure", "tuition fees", "how much does it cost",
                     "fee payment details", "scholarship information"],
        "responses": ["Sample answer: Fee details and scholarships are available at the "
                      "accounts office and on the website."]},
    "placement": {
        "patterns": ["placement details", "which companies visit", "job opportunities",
                     "campus recruitment", "internship information"],
        "responses": ["Sample answer: The placement cell conducts training and campus "
                      "recruitment drives every year."]},
    "time": {
        "patterns": ["what is the time", "current time now", "tell me the time", "what time is it"],
        "responses": ["The time now is {time}."]},
    "date": {
        "patterns": ["what is the date", "today's date", "which day is today", "what is today"],
        "responses": ["Today is {date}."]},
}


# ---------------- NLP pipeline ----------------
def tokenize(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def stem(word):
    for suffix in ("ing", "edly", "ed", "ly", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def preprocess(text):
    return [stem(w) for w in tokenize(text) if w not in STOPWORDS]


class IntentClassifier:
    """TF-IDF + cosine similarity over all example sentences."""

    def __init__(self, intents):
        self.examples = []                                  # (intent, tokens)
        for name, data in intents.items():
            for pattern in data["patterns"]:
                self.examples.append((name, preprocess(pattern)))
        n_docs = len(self.examples)
        df = Counter()
        for _, tokens in self.examples:
            df.update(set(tokens))
        self.idf = {w: math.log((1 + n_docs) / (1 + c)) + 1 for w, c in df.items()}
        self.vectors = [(name, self.vectorize(tokens)) for name, tokens in self.examples]

    def vectorize(self, tokens):
        tf = Counter(tokens)
        vec = {w: tf[w] * self.idf.get(w, 0.0) for w in tf if w in self.idf}
        norm = math.sqrt(sum(v * v for v in vec.values()))
        return {w: v / norm for w, v in vec.items()} if norm else {}

    @staticmethod
    def cosine(a, b):
        return sum(a[w] * b.get(w, 0.0) for w in a)

    def classify(self, sentence):
        query = self.vectorize(preprocess(sentence))
        best_intent, best_score = None, 0.0
        for name, vec in self.vectors:
            score = self.cosine(query, vec)
            if score > best_score:
                best_intent, best_score = name, score
        return best_intent, best_score


class ChatBot:
    THRESHOLD = 0.30

    def __init__(self):
        self.classifier = IntentClassifier(INTENTS)
        self.user_name = None

    def reply(self, sentence):
        text = sentence.strip()
        if not text:
            return "Please type something."

        # rule 1: learn the user's name with a regular expression
        m = re.search(r"\bmy name is ([a-zA-Z]+)", text, re.I) or re.search(r"\bi am ([a-zA-Z]+)$", text, re.I)
        if m:
            self.user_name = m.group(1).capitalize()
            return f"Nice to meet you, {self.user_name}!"
        # rule 2: recall the name
        if re.search(r"\b(what is|what's|do you know) my name\b", text, re.I):
            return f"Your name is {self.user_name}." if self.user_name else "I don't know your name yet. Tell me: 'my name is ...'"

        # NLP intent matching
        intent, score = self.classifier.classify(text)
        if intent is None or score < self.THRESHOLD:
            return "Sorry, I did not understand that. Ask me about courses, exams, library, hostel, fees or placements."
        answer = random.choice(INTENTS[intent]["responses"])
        now = datetime.datetime.now()
        answer = answer.format(time=now.strftime("%I:%M %p"), date=now.strftime("%A, %d %B %Y"))
        if intent == "greeting" and self.user_name:
            answer = f"Hello again, {self.user_name}! How can I help you?"
        self.last_intent, self.last_score = intent, score
        return answer

    @staticmethod
    def is_goodbye(text):
        return preprocess(text) in (["bye"], ["goodbye"], ["exit"], ["quit"]) or text.strip().lower() in ("bye", "exit", "quit")


def demo(bot):
    script = ["Hello", "my name is Siva", "What courses are available?", "when does the library open",
              "Is hostel accommodation available?", "tell me about placements", "what is the time",
              "what is my name", "I like pizza", "thanks", "bye"]
    for line in script:
        print(f"You : {line}")
        print(f"Bot : {bot.reply(line)}\n")


if __name__ == "__main__":
    random.seed(1)
    bot = ChatBot()
    print("CampusBot - NLP chatbot (type 'bye' to exit)\n")
    if "--demo" in sys.argv:
        demo(bot)
    else:
        while True:
            try:
                user = input("You : ")
            except (EOFError, KeyboardInterrupt):
                print("\nBot : Goodbye!")
                break
            print("Bot :", bot.reply(user))
            if ChatBot.is_goodbye(user):
                break
