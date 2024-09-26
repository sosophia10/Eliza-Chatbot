# Eliza Chatbot: A Psychotherapist Simulation

## Overview
This project implements a Python-based version of the famous **ELIZA** chatbot, simulating conversations with a Rogerian psychotherapist. The chatbot uses **regular expressions** for word spotting and transforms user statements into relevant questions. The chatbot engages the user in a dialogue by mimicking a therapeutic session where it responds based on keywords in the input.

## Features
- **Natural Language Processing**: Processes user inputs using regular expressions to identify keywords.
- **Word Spotting**: Detects specific words and generates appropriate responses.
- **Sentence Transformation**: Converts user statements into questions to keep the conversation flowing.
- **User Name**: The chatbot asks for and uses the user's name in responses.

## Technologies Used
- **Python**: Programming language for building the chatbot.
- **Regular Expressions (re library)**: To identify keywords and process the user's input.
- **Text Processing**: Uses basic string manipulation for pronoun swapping and sentence transformation.

## Setup and Installation

### Prerequisites
- **Python 3.x** installed on your system.

### Installation Steps
1. Clone the repository:
   ```
   git clone https://github.com/sosophia10/Eliza-Chatbot.git
   ```

2. Navigate to the project directory:
   ```
   cd Eliza-Chatbot
   ```

3. Clone the repository:
   ```
   python eliza.py
   ```

## Usage
Once the program is run, the chatbot will start a conversation by asking for your name. Based on your inputs, it will continue the conversation by asking follow-up questions, transforming your statements, or prompting you to elaborate further.

### Example Interaction:
  ```
  [eliza] Hi, I'm a psychotherapist. What is your name?
[user] My name is Alex.
[eliza] Hi Alex. How can I help you today?
[user] I am feeling stressed.
[eliza] Alex, why do you feel stressed?
  ```

## Additional Resources
Learn more about ELIZA from [Joseph Weizenbaum's Paper](https://en.wikipedia.org/wiki/ELIZA).

Explore the online version of [Eliza](http://www.masswerk.at/elizabot/).
