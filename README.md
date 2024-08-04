# `Inquisitive` Generative-AI Powered Quiz Generator

<!-- <hr> -->

This repository contains the content of <u>Inquisitive:</u> generative intelligence powered quiz generator.

## Description
&nbsp; &nbsp; &nbsp;
The project is AI-driven multilingual question generator which creates quizzes from any text/news articles in any language.  
&nbsp; &nbsp; &nbsp;
The project incorporates language detection, machine translation, and a large language model (LLM) for accurate and contextually relevant quiz generation.  
&nbsp; &nbsp; &nbsp;
It utilizes the Gemini-API to create quizzes based on the given text context. In cases where the user inputs a topic instead of a large text, a paragraph is first provided for user comprehension, and then the quiz is generated based on it.  
&nbsp; &nbsp; &nbsp;
Users' submissions are recorded, and results are generated. A detailed analysis section allows users to review their performance and submissions. The sleek and user-friendly interface, is made with Streamlit which ensures a smooth and engaging user-experience.

&nbsp; &nbsp; &nbsp;


## Table of Contents

- [`Inquisitive` Generative-AI Powered Quiz Generator](#inquisitive-generative-ai-powered-quiz-generator)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Problem Statement](#problem-statement)
  - [Project Overview](#project-overview)
  - [Tech-Stack 💻](#tech-stack-)
  - [Links](#links)
  - [Installation](#installation)
  - [Contributions](#contributions)
    - [Contact](#contact)


## Problem Statement
&nbsp; &nbsp; &nbsp;
Our client, NewsSphere, is a leading news organization dedicated to expanding its global reach and enhancing audience engagement. With a vast amount of content published daily in multiple languages, the organization faces the considerable challenge of manually creating quizzes and
assessments for each article. This process is not only time-consuming but also prone to inconsistencies across different languages and cultural contexts.

<img align="center" src="./assets/FlowChart.png">


## Project Overview

1. **`User Input:`** User submits a news article in any language.

1. **`Language Detection:`** The app utilizes the Translation API to detect the language of the submitted content.

1. **`Translation to English:`** If the content is not in English, the app translates it into English using the Translation API.

1. **`Question Generation:`** The app calls the Gemini API to generate diverse and contextually relevant questions based on the input.
  
1. **`Translation Back:`** The generated questions are translated back into the original language of the news article using the Translation API.

1. **`Output:`** The app presents the questions in the original language to the user.
   
1. **`Quiz:`** User can now answer the various types of the questions generated.

1. **`Result:`** Once submitted ✅, results are visible on the screen.


## Tech-Stack 💻
   - Python
   - Streamlit (Python)
   - Langdetect (python)
   - Gemini API
   

## Links

1. Visit the deployed project on Streamlit Community Cloud:  
    [Deployment Link](https://ai-quiz-generator-bbs.streamlit.app/)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Bbs1412/Inquisitive_GenAI_quiz

    cd Inquisitive_GenAI_quiz
    ```

2. **Create and activate python environment:**  
    ```bash
    python -m venv env

    .\env\Scripts\activate
    ```

3. **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Generate Gemini-API key.**
   
   <img align="center" src="./assets/API.png">  
     
  
5. **Create a file *'api.env'* in current directory and save the API-key in it:**
    ```python
    API="your_key"
    ```

6. Run the app:
   ```bash
   streamlit run app.py
   ```

<!-- 3. Video demonstration of project implementation:
   [Redirect to LinkedIn](https://--------) 
   future_work_here
   update the numbers as well
   -->

   
## Contributions  

   Any contributions or suggestions are welcome! 


### Contact

   - **Email** - [bhushanbsongire@gmail.com](bhushanbsongire@gmail.com)
   - **Git** - [Bbs1412](https://github.com/Bbs1412/)


<!-- ## Acknowledgments -->
   <!-- - Thanks to .. for ... -->
