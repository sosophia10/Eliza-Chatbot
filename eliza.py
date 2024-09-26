"""
Eliza Psychotherapist Chatbot
Author: Sophia Herman
Date: May 26, 2024

Introduction:
This program simulates a conversation with a psychotherapist named Eliza. It recognizes certain keywords
and responds based on their presence in the user's input. The program also transforms simple statements
into questions, creating a self-reflective dialogue.

Examples of program input and output:
Eliza: Hi, I'm a psychotherapist. Why don't we start by telling me your name?
User: My name is | Sophia.
Eliza: Hi Sophia. How can I help you today? Feel free to tell me anything, these sessions are completely confidential.
Sophia: I am poor.
Eliza: Do you enjoy feeling poor?

Usage Instructions:
1. Run the program.
2. Enter your responses after the prompt.
3. To exit the conversation, type "quit".
4. If you press ENTER without typing anything, Eliza will prompt you to elaborate.

Algorithm:
1. Greet the user and ask for their name.
2. Continuously prompt the user for input until they type "quit".
3. Transform pronouns and verbs in the user's input to maintain context in Eliza's responses.
4. Handle contractions to ensure proper formatting.
5. Simplify the user's input to remove unnecessary descriptors.
6. Handle grammar to determine if the first word after "I am/I'm" is a verb, noun, adjective, etc.
7. Generate responses based on keyword recognition and transformation of statements into questions.
8. Personalize the dialogue by using the user's name in responses.
9. Handle empty input by prompting the user to elaborate.
10. End the conversation when the user types "quit" with a goodbye message.

"""

import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Ensure that the necessary nltk data is downloaded
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


def greet_user():
    """
    Greet the user.
    ---
    Initiate the conversation by asking for the user's name and greeting them.
    """
    print(
        "-> [eliza] Hi, I'm a psychotherapist. Why don't we start by telling me your name?"
    )
    user_name = input("=> [user] My name is ").strip()
    print(
        f"-> [eliza] Hi {user_name}. How can I help you today? Feel free to tell me anything, these sessions are completely confidential."
    )
    return user_name


def transform_pronouns(input_string):
    """
    Transform pronouns and verb forms in the user's input to match the context of Eliza's responses.
    ---
    In the get_response function, the user's input is transformed using transform_pronouns before generating a response.

    """
    pronoun_mapping = {
        "i": "you",
        "me": "you",
        "my": "your",
        "mine": "yours",
        "am": "are",
        "i'm": "you're",
        "i'd": "you'd",
        "i've": "you've",
        "i'll": "you'll",
        "you": "I",
        "your": "my",
        "yours": "mine",
        "you're": "I'm",
        "you'd": "I'd",
        "you've": "I've",
        "you'll": "I'll",
        "myself": "yourself",
        "yourself": "myself",
        "we": "you",
        "us": "you",
        "our": "your",
        "ours": "yours",
    }

    verb_mapping = {
        "is": {
            "i": "am",
            "you": "are",
            "he": "is",
            "she": "is",
            "it": "is",
            "we": "are",
            "they": "are",
        },
        "was": {
            "i": "was",
            "you": "were",
            "he": "was",
            "she": "was",
            "it": "was",
            "we": "were",
            "they": "were",
        },
        "has": {
            "i": "have",
            "you": "have",
            "he": "has",
            "she": "has",
            "it": "has",
            "we": "have",
            "they": "have",
        },
        "wasn't": {
            "i": "wasn't",
            "you": "weren't",
            "he": "wasn't",
            "she": "wasn't",
            "it": "wasn't",
            "we": "weren't",
            "they": "weren't",
        },
        "isn't": {
            "i": "am not",
            "you": "aren't",
            "he": "isn't",
            "she": "isn't",
            "it": "isn't",
            "we": "aren't",
            "they": "aren't",
        },
        "hasn't": {
            "i": "haven't",
            "you": "haven't",
            "he": "hasn't",
            "she": "hasn't",
            "it": "hasn't",
            "we": "haven't",
            "they": "haven't",
        },
    }
    words = input_string.lower().split()
    transformed_words = []
    for i, word in enumerate(words):
        # Map pronouns first
        if word in pronoun_mapping:
            transformed_words.append(pronoun_mapping[word])
        # Then map verbs according to the transformed pronoun
        elif i > 0 and words[i - 1].lower() in pronoun_mapping:
            prev_word = transformed_words[-1].lower()
            if word in verb_mapping and prev_word in verb_mapping[word]:
                transformed_words.append(verb_mapping[word][prev_word])
            else:
                transformed_words.append(word)
        else:
            transformed_words.append(word)

    # Join the words to a string
    transformed_string = " ".join(transformed_words)
    # print(f"Debug: After pronoun transformation: {transformed_string}")

    return handle_contractions(transformed_string)


def handle_contractions(input_string):
    """
    Ensure that contractions in the string are properly formatted without spaces.
    ---
    Sort of works.
    """
    contractions = {
        "n't": "n't",
        "'ll": "'ll",
        "'ve": "'ve",
        "'re": "'re",
        "'d": "'d",
        "'m": "'m",
    }

    for contraction, correct_form in contractions.items():
        input_string = re.sub(
            rf"\b(\w+)\s{contraction}\b", rf"\1{correct_form}", input_string
        )

    # print(f"Debug: After handling contractions: {input_string}")

    return input_string


def simplify_response(response):
    """
    Simplify the response to remove unnecessary descriptors after the first noun or stopping punctuation.
    ---
    In the get_response function, the transformation is applied to ensure phrases are optimally handled in the responses.
    """
    tokens = word_tokenize(response)
    simplified = []
    for word in tokens:
        if word in [".", "!", "?", ","]:
            break
        simplified.append(word)
        if pos_tag([word])[0][1].startswith("NN"):
            break
    simplified_string = " ".join(simplified)
    # Remove any spaces before apostrophes
    simplified_string is re.sub(r"\s'(\w+)", r"'\1", simplified_string)
    simplified_string = re.sub(
        r"\s+", " ", simplified_string
    )  # Remove any additional spaces
    # print(f"Debug: After simplification: {simplified_string}")

    return handle_contractions(simplified_string)


def handle_grammar(input_string):
    """
    Handle grammar by determining whether the beginning word of the user input is a verb, noun, or an adjective.
    ---
    Applies only when the input string starts with 'I am' or 'I'm'.
    Example: If the first word after "I am/I'm" is an adjective/noun (requires "being") or a verb in the continuous form (no "being").
    """
    # print(f"Debug: Before handling grammar: {input_string}")
    tokens = word_tokenize(input_string)
    tagged = pos_tag(tokens)

    # print(f"Debug: Tokenized input: {tokens}")
    # print(f"Debug: POS tags: {tagged}")

    # Check if the input starts with "I am" or "I'm"
    if len(tagged) > 1 and (
        tagged[0][0].lower() == "i" and tagged[1][0].lower() in ["am", "'m"]
    ):
        # Remove 'I am' or 'I'm' for grammar processing
        relevant_input = " ".join(tokens[2:])
        relevant_tagged = tagged[2:]
        first_word_tag = relevant_tagged[0][1] if len(relevant_tagged) > 0 else ""

        # print(f"Debug: Relevant input: {relevant_input}")
        # print(f"Debug: Relevant POS tags: {relevant_tagged}")

        # Handle different cases based on the tag
        if first_word_tag in [
            "JJ",
            "JJR",
            "JJS",
            "RB",
            "RBR",
            "RBS",
        ]:  # Adjective or Adverb
            # print(f"Debug: After handling grammar: feeling {relevant_input}")
            return "feeling " + relevant_input
        elif first_word_tag.startswith("VB"):  # Verb
            if first_word_tag == "VBG":
                # print(f"Debug: After handling grammar: {relevant_input}")
                return relevant_input  # No 'being' for verbs in continuous form
            else:
                # print(f"Debug: After handling grammar: being {relevant_input}")
                return "being " + relevant_input
        elif first_word_tag.startswith("NN") or first_word_tag in [
            "PRP",
            "PRP$",
            "RP",
            "IN",
            "DT",
            "PDT",
            "WDT",
            "CD",
            "LS",
            "SYM",
            "WDT",
            "WP",
            "WRB",
        ]:  # Noun, Pronoun, Determiner, Cardinal number, List item marker, Symbol
            if first_word_tag == "NN":
                # print(f"Debug: After handling grammar: being a {relevant_input}")
                return "being a " + relevant_input
            else:
                # print(f"Debug: After handling grammar: being {relevant_input}")
                return "being " + relevant_input
        elif first_word_tag in ["TO"]:  # Preposition or Particle
            # print(f"Debug: After handling grammar: {relevant_input}")
            return "trying " + relevant_input
        elif first_word_tag in [
            "CC",
            "EX",
            "FW",
            "UH",
            "POS",
        ]:  # Coordinating conjunction, Existential there, Foreign word, Interjection, Possessive ending
            # print(f"Debug: After handling grammar: about {relevant_input}")
            return "whatever " + relevant_input + " means"
        else:
            # print(f"Debug: Unrecognized first word tag {first_word_tag}")
            return relevant_input
    # print(f"Debug: After handling grammar: {input_string}")
    return input_string


def get_response(user_input, user_name):
    """
    Generate a response based on the user's input using regular expressions to spot keywords and transform sentences.
    ---
    # It uses regular expressions to identify patterns and keywords in the input and selects an appropriate response from predefined sets.
    """
    responses = {
        "I'm afraid of (.*)": [
            "Why are you afraid of {0}?",
            "What about {0} scares you?",
            "How do you usually cope with this fear?",
        ],
        "I'm worried about (.*)": [
            "Why are you worried about {0}?",
            "What do you think might happen with {0}?",
            "How do you usually deal with worries like this?",
        ],
        "I remember (.*)": [
            "What does {0} make you think of?",
            "How does that memory make you feel?",
            "Why is {0} significant to you?",
        ],
        "I feel like (.*)": [
            "Why do you feel like {0}?",
            "What makes you feel like {0}?",
            "How does it affect you to feel like {0}?",
        ],
        "I wish I could (.*)": [
            "What stops you from {0}?",
            "How do you think you could start {0}?",
            "What would change for you if you could {0}?",
        ],
        "People (.*)": [
            "Why do you think people {0}?",
            "What kind of people {0}?",
            "How do you feel about people {0}?",
        ],
        "My job (.*)": [
            "Tell me more about your job.",
            "What do you like or dislike about your job?",
            "How does your job make you feel?",
        ],
        "My friends (.*)": [
            "Tell me more about your friends.",
            "What do you enjoy about your friends?",
            "How do your friends affect your life?",
        ],
        "I don't understand (.*)": [
            "Why do you think you don't understand {0}?",
            "What could help you understand {0} better?",
            "How does not understanding {0} make you feel?",
        ],
        "I feel overwhelmed (.*)": [
            "What is overwhelming you?",
            "How do you usually cope with feeling overwhelmed?",
            "What can you do to reduce this feeling?",
        ],
        "I feel stuck (.*)": [
            "Why do you feel stuck {0}?",
            "What can you do to move forward?",
            "How long have you felt stuck?",
        ],
        "My childhood (.*)": [
            "Tell me more about your childhood.",
            "What are your most vivid childhood memories?",
            "How do you feel about your childhood?",
        ],
        "I don't like (.*)": [
            "Why don't you like {0}?",
            "What about {0} bothers you?",
            "How do you usually deal with things you don't like?",
        ],
        "I hate (.*)": [
            "Why do you hate {0}?",
            "What about {0} makes you feel this way?",
            "How do you usually express this feeling?",
        ],
        "I enjoy (.*)": [
            "What do you enjoy about {0}?",
            "How often do you engage in {0}?",
            "How does {0} make you feel?",
        ],
        "I prefer (.*)": [
            "Why do you prefer {0}?",
            "What makes {0} better for you?",
            "How does preferring {0} affect your choices?",
        ],
        "I dislike (.*)": [
            "Why do you dislike {0}?",
            "What about {0} makes you feel this way?",
            "How do you usually handle things you dislike?",
        ],
        "I'm unsure about (.*)": [
            "Why are you unsure about {0}?",
            "What would help you feel more certain about {0}?",
            "How does being unsure about {0} affect you?",
        ],
        "(.*)\?": [
            "Why do you ask that?",
            "What do you think?",
            "How would an answer to that help you?",
        ],
        "(.*) problem(.*)": [
            "Tell me more about that problem.",
            "How do you usually deal with problems like that?",
            "What do you think is causing this problem?",
        ],
        "(.*) happy(.*)": [
            "What makes you feel happy?",
            "Tell me more about what's making you happy.",
            "How long have you felt this way?",
        ],
        "(.*) sad(.*)": [
            "Why do you feel sad?",
            "What usually helps you feel better when you're sad?",
            "How long have you been feeling this way?",
        ],
        "(.*) angry(.*)": [
            "What makes you feel angry?",
            "How do you usually express your anger?",
            "What do you think can help you calm down?",
        ],
        "(.*) worried(.*)": [
            "Why do you feel worried?",
            "What do you think is the cause of your worry?",
            "How do you usually cope with worry?",
        ],
        "(.*) excited(.*)": [
            "What are you excited about?",
            "How long have you been feeling this way?",
            "What usually makes you excited?",
        ],
        "(.*) confused(.*)": [
            "What is confusing you?",
            "How do you usually deal with confusion?",
            "What do you think could help you understand better?",
        ],
        "(.*) love(.*)": [
            "Tell me more about this feeling of love.",
            "Who do you feel this way about?",
            "How long have you felt this way?",
        ],
        "(.*) afraid(.*)": [
            "Why do you feel afraid?",
            "What do you think is causing this fear?",
            "How do you usually deal with fear?",
        ],
        "(.*) dreams(.*)": [
            "What kind of dreams have you been having?",
            "Do you remember any specific dreams?",
            "How do these dreams make you feel?",
        ],
        "(.*) past(.*)": [
            "Do you often think about the past?",
            "What specifically from the past are you thinking about?",
            "How does thinking about the past make you feel?",
        ],
        "(.*) future(.*)": [
            "What are your thoughts about the future?",
            "Does thinking about the future make you anxious?",
            "What are you looking forward to?",
        ],
        "(.*) work(.*)": [
            "Tell me more about your work.",
            "Do you enjoy your work?",
            "What do you find most challenging about your work?",
        ],
        "(.*) family(.*)": [
            "Tell me more about your family.",
            "How do you feel about your family?",
            "What is your relationship with your family like?",
        ],
        "(.*) relationships(.*)": [
            "How do you feel about your relationships?",
            "What is the most important thing to you in a relationship?",
            "Have you had any significant relationships recently?",
        ],
        "(.*) school(.*)": [
            "Tell me more about your school experience.",
            "Do you enjoy school?",
            "What do you find most challenging about school?",
        ],
        "(.*) health(.*)": [
            "How is your health?",
            "Are you concerned about any health issues?",
            "What do you do to maintain your health?",
        ],
        "(.*) hobbies(.*)": [
            "What hobbies do you enjoy?",
            "How often do you engage in your hobbies?",
            "How do your hobbies make you feel?",
        ],
        "(.*) travel(.*)": [
            "Do you like to travel?",
            "Tell me about a recent trip you've taken.",
            "What places would you like to visit?",
        ],
        "(.*) stress(.*)": [
            "What is causing you stress?",
            "How do you usually handle stress?",
            "What can you do to reduce your stress?",
        ],
        "(.*) goals(.*)": [
            "What are your current goals?",
            "How do you plan to achieve your goals?",
            "What motivates you to pursue your goals?",
        ],
        "(.*) changes(.*)": [
            "What changes are you experiencing?",
            "How do you feel about these changes?",
            "What can you do to adapt to these changes?",
        ],
        "I want (.*)": [
            "Why do you want {0}?",
            "How would it feel if you got {0}?",
            "What would you do if you got {0}?",
            "I see. And what does that tell you?",
        ],
        "I need (.*)": [
            "Why do you need {0}?",
            "Would it really help you to get {0}?",
            "Are you sure you need {0}?",
        ],
        "Why don't you (.*)": [
            "Do you really think I don't {0}?",
            "Perhaps eventually I will {0}.",
            "Do you really want me to {0}?",
        ],
        "Why can't I (.*)": [
            "Do you think you should be able to {0}?",
            "If you could {0}, what would you do?",
            "I don't know -- why can't you {0}?",
        ],
        "I can't (.*)": [
            "How do you know you can't {0}?",
            "Perhaps you could {0} if you tried.",
            "What would it take for you to {0}?",
        ],
        "I am (.*)": [
            "How long have you been {0}?",
            "How do you feel about {0}?",
            "Do you enjoy {0}?",
        ],
        "I'm (.*)": [
            "How does {0} make you feel?",
            "Do you enjoy {0}?",
            "Why do you tell me you're {0}?",
        ],
        "Are you (.*)": [
            "Why does it matter whether I am {0}?",
            "Would you prefer if I were not {0}?",
            "Perhaps you believe I am {0}.",
        ],
        "What (.*)": [
            "Why do you ask?",
            "How would an answer to that help you?",
            "What do you think?",
        ],
        "How (.*)": [
            "How do you suppose?",
            "Perhaps you can answer your own question.",
            "What is it you're really asking?",
        ],
        "Because (.*)": [
            "Is that the real reason?",
            "What other reasons come to mind?",
            "Does that reason apply to anything else?",
            "If {0}, what else must be true?",
        ],
        "(.*) sorry (.*)": [
            "There are many times when no apology is needed.",
            "What feelings do you have when you apologize?",
        ],
        "Hello(.*)": [
            "Hello, I'm glad you could drop by today.",
            "Hi there, how are you today?",
            "Hello, how are you feeling today?",
        ],
        "I think (.*)": [
            "Do you doubt {0}?",
            "Do you really think so?",
            "But you're not sure {0}?",
        ],
        "(.*) friend (.*)": [
            "Tell me more about your friends.",
            "When you think of a friend, what comes to mind?",
            "Why don't you tell me about a childhood friend?",
            "How do you feel when you say that?",
        ],
        "Yes (.*)": ["You seem quite sure.", "OK, but can you elaborate a bit?"],
        "(.*) computer(.*)": [
            "Are you really talking about me?",
            "Does it seem strange to talk to a computer?",
            "How do computers make you feel?",
            "Do you feel threatened by computers?",
        ],
        "Is it (.*)": [
            "Do you think it is {0}?",
            "Perhaps it's {0} -- what do you think?",
            "If it were {0}, what would you do?",
        ],
        "It is (.*)": [
            "You seem very certain.",
            "If I told you that it probably isn't {0}, what would you feel?",
        ],
        "Can you (.*)": [
            "What makes you think I can't {0}?",
            "If I could {0}, then what?",
            "Why do you ask if I can {0}?",
        ],
        "Can I (.*)": [
            "Perhaps you don't want to {0}.",
            "Do you want to be able to {0}?",
            "If you could {0}, would you?",
        ],
        "You are (.*)": [
            "Why do you think I am {0}?",
            "Does it please you to think that I'm {0}?",
            "Perhaps you would like me to be {0}?",
        ],
        "You're (.*)": [
            "Why do you say I am {0}?",
            "Why do you think I am {0}?",
            "Are we talking about you, or me?",
            "How does that make you feel?",
        ],
        "(.*) me (.*)": [
            "Why do you say that {0} you?",
            "Why do you think that {0} you?",
            "What do you mean by {0} you?",
        ],
        "Why (.*)": [
            "What would you do if you had the answer to that question?",
            "I don't have all the answers, yet I wish I knew everything. Why {0}?",
            "I don't know, {0}?",
        ],
        "I want (.*)": [
            "What would it mean if you got {0}?",
            "Why do you want {0}?",
            "What would you do if you got {0}?",
        ],
        "(.*) mother(.*)": [
            "Tell me more about your mother.",
            "What was your relationship with your mother like?",
            "How do you feel about your mother?",
        ],
        "(.*) father(.*)": [
            "Tell me more about your father.",
            "How did your father make you feel?",
            "How do you feel about your father?",
        ],
        "(.*) child(.*)": [
            "Did you have close friends as a child?",
            "What is your favorite childhood memory?",
            "Please tell me more.",
            "Can you elaborate on that?",
            "Do you remember any dreams or nightmares from childhood?",
        ],
        "I feel (.*)": [
            "Why do you feel {0}?",
            "What makes you feel {0}?",
            "How long have you felt {0}?",
        ],
        "It seems (.*)": [
            "Why does it seem {0}?",
            "What makes it seem {0}?",
            "How does it affect you that it seems {0}?",
        ],
        "Sometimes (.*)": [
            "Can you tell me more about those times?",
            "Why sometimes and not always?",
            "What happens when {0}?",
        ],
        "If only (.*)": [
            "What do you think would change if {0}?",
            "Why do you say 'if only {0}'?",
            "What stops you from making {0} happen?",
        ],
        "I regret (.*)": [
            "Why do you regret {0}?",
            "What could you do differently now?",
            "How does regretting {0} affect you?",
        ],
        "I hope (.*)": [
            "Why do you hope {0}?",
            "What makes you hope {0}?",
            "How would you feel if {0}?",
        ],
        "I wish (.*)": [
            "Why do you wish {0}?",
            "What makes you wish {0}?",
            "What would you do if {0}?",
        ],
        "I miss (.*)": [
            "Why do you miss {0}?",
            "What do you miss most about {0}?",
            "How often do you think about {0}?",
        ],
        "default": [
            "Why do you say {0}?",
            "{0}?",
        ],
    }

    for pattern, resps in responses.items():
        match = re.match(pattern, user_input, re.IGNORECASE)
        if match:
            resp = random.choice(resps)
            try:
                transformed_input = transform_pronouns(match.group(1))
                # print(f"Debug: Before handling grammar: {transformed_input}")
                if pattern in ["I am (.*)", "I'm (.*)"]:
                    transformed_input = handle_grammar(f"I am {transformed_input}")
                # print(f"Debug: After handling grammar: {transformed_input}")
                transformed_input = handle_contractions(transformed_input)
                simplified_input = simplify_response(transformed_input)
                return resp.format(simplified_input)
            except IndexError:
                return "I'm not sure I understand. Can you elaborate?"
    transformed_default = transform_pronouns(user_input)
    # print(f"Debug: Before handling grammar (default): {transformed_default}")
    if re.match(r"^I am|^I'm", user_input, re.IGNORECASE):
        transformed_default = handle_grammar(transformed_default)
    # print(f"Debug: After handling grammar (default): {transformed_default}")
    transformed_default = handle_contractions(transformed_default)
    simplified_default = simplify_response(transformed_default)
    return random.choice(responses["default"]).format(simplified_default)


def eliza_chat():
    """
    Main function to handle the conversation loop with the user.
    ---
    Handles the main conversation loop, continuing until the user types "quit".
    It interacts with the user, gets their input, and generates responses using the get_response function.
    Includes a list of predefined quit responses. When the user inputs "quit," one of these responses is chosen randomly and printed.
    """
    user_name = greet_user()
    while True:
        user_input = input(f"=> [{user_name}] ").strip()
        if user_input.lower() == "quit":
            quit_responses = [
                "Thank you for talking with me.",
                "Good-bye, for now.",
                "Thank you, that will be $150. Have a good day!",
            ]
            print(f"-> [eliza] {random.choice(quit_responses)}")
            break
        elif user_input == "":
            print(
                "-> [eliza] I'm sorry, I didn't catch that. Can you please elaborate?"
            )
            continue
        response = get_response(user_input, user_name)
        print(f"-> [eliza] {response}")


if __name__ == "__main__":
    eliza_chat()
