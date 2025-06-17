---
hide:
  - toc
---

# Instructions

Before the README sections 'Setup' and 'Usage' are completed, you must first add two files from the shared CEN Google Drive to `~/.chatbot-util/` on your computer

## `Chatbot FAQ - Enter Here.csv`

This file contains a list of topics/people and common questions that may be asked about it/them

### Retrieval

- This file is from the Google Sheet named 'FAQ' in `CEN/AI/Chatbot/`
- Simply download the tab named 'Enter Here' as a `.csv` file (Comma Separated Values)
- Create the directory `.chatbot-util/` in your Home folder
- Move this downloaded file to `~/.chatbot-util/`

### Format

- Each Person/Entity can span multiple rows of questions
- Each Person/Entity is split by an empty row
- Example

      | Person/Entity | Questions        |
      | ------------- | ---------------- |
      | CEN           | What is CEN?     |
      |               |                  |
      | Rob Thomas    | Smooth?          |
      |               |                  |
      | Robotics      | What are robots? |
      |               |                  |

## `Other.txt`

This file contains a list of our employees and their roles, phrases to find and substitutes to replace them with (in the LLM-generated output), and answers for each of the CEN/Robotics/Instructional/Edu-Reach questions

### Retrieval

- This file is from the text file named `Other.txt` in `CEN/AI/Chatbot`
- Download this file and place in `~/chatbot-util`

### Format

- Each section is separated by a newline
- The first section requires that each entry contains parts 1-3, separated by a colon (like `part 1:part 2:part 3`)
- The second and third sections require that each entry contains parts 1-2, separated by a colon (like `part 1:part 2`)
- Do not use unnecessary quotes or spaces
- Each section accepts 1+ entries
- Example

      ```text
      Employee Name:Employee Title:Employee Pronoun

      Phrase to replace:Phrase to replace it with

      Phrase before 'CEN' or 'Collegiate Edu-Nation':Phrase after 'CEN' or 'Collegiate Edu-Nation'

      Answer to Robotics Question

      Answer to Instructional Question
      ```

## `Permutated.csv`

This file is the output of successfully running `chatbot-util` on the above files

### Retrieval and Usage

- This file will be stored locally in `~/.chatbot-util/`
- Log in to Google Cloud Console, and search for 'vertex ai agent builder'
- Once there, press 'view' under 'Connected data stores' for the CEN Chatbot app
- Press on 'faq-7.2', then select this file after clicking '+ IMPORT DATA'

### Format

- Each row contains exactly one question and answer, which are comma-separated
- Every question and answer must be enclosed in quotes

      ```text
      "question","answer"
      "What is CEN?","CEN is a non-profit organization engaging whole communities to reinvigorate education, revitalize local economies, and reimagine what's possible for rural America. We're preparing rural communities to connect and thrive in a fast-moving future."
      ```
