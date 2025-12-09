---
hide:
  - toc
---

# Instructions

- Before the README sections 'Setup' and 'Usage' are completed, you must first download two files from the shared CEN Google Drive: the [FAQ](#faq-enter-herecsv) and [Other.txt](#othertxt)
- Optionally, adding links to these files in the [config file](#configtoml) will streamline direct access in the future
- Additionally, the UI features several [status indicators](#status-indicators) for identifying common issues

## `FAQ - Enter Here.csv`

This file contains a list of topics/people and common questions that may be asked about it/them

### Retrieval

- This file is from the Google Sheet named 'FAQ' in `CEN/AI/Chatbot/`
- Open the Sheet, then download the tab named 'Enter Here' as a `.csv` file (Comma Separated Values)

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
      | Instructional | How do I teach?  |
      |               |                  |

## `Other.txt`

This file contains a list of our teams, employees and their roles, phrases to find and substitutes to replace them with (in the LLM-generated output), and answers for each of the CEN/Team questions

### Retrieval

- Download the text file named `Other.txt` in `CEN/AI/Chatbot/`

### Format

- Each section is separated by a newline
- The second section requires that each entry contains parts 1-3, separated by a colon (like `part 1:part 2:part 3`)
- The third and fourth sections require that each entry contains parts 1-2, separated by a colon (like `part 1:part 2`)
- Do not use unnecessary quotes or spaces
- Each section accepts 1+ entries
- Example

      ```text
      Team Name

      Employee Name:Employee Title:Employee Pronoun

      Phrase to replace:Phrase to replace it with

      Phrase before 'CEN' or 'Collegiate Edu-Nation':Phrase after 'CEN' or 'Collegiate Edu-Nation'

      Answer to Team Question
      ```

### Update

Since this file contains employee info, it will need to be manually kept in sync with our current employees, roles, and teams. As long as the current version is always in `CEN/AI/Chatbot/`, we can be sure there are at least two copies of this file at all times (with the other being on the Chatbot maintainer's local computer)

The recommended process for updating this file is to

- Unlock the previous `Other.txt`
- Rename it to `Other.txt.backup`
- Upload the updated `Other.txt`
- Lock the updated file
- Delete `Other.txt.backup` once you're certain the new file is correct

## `Permutated.csv`

This file is the output of successfully running `Generate` on the above files

### Retrieval and Usage

- This file will be stored locally in `~/.chatbot-util/`
- Log in to Google Cloud Console and navigate to the `Chatbot` project
- Click the hamburger menu on the top left and navigate to `Cloud Storage/Buckets/cen-chatbot-docs-062524/FAQ/`
- Once there, upload `Permutated.csv`, making sure to select the 'Overwrite object' option

This updated the FAQ in the bucket referenced by the agent's data store, but it didn't actually update the data store itself. This will also need to be updated for the changes to propagate to the agent

- Search for 'AI Applications'
- Once there, press 'view' under 'Connected data stores' for the CEN Chatbot app
- Press on 'faq-7.2', then select this file after clicking '+ IMPORT DATA' and selecting the 'Full' option

The changes should propagate after a short period of time (~15 minutes)

### Format

- Each row contains exactly one question and answer, which are comma-separated
- Every question and answer must be enclosed in quotes

      ```text
      "question","answer"
      "What is CEN?","CEN is a non-profit organization engaging whole communities to reinvigorate education, revitalize local economies, and reimagine what's possible for rural America. We're preparing rural communities to connect and thrive in a fast-moving future."
      ```

## `config.toml`

This basic (and optional) TOML configuration file contains links to `FAQ - Enter Here.csv` and `Other.txt` that enables convenient access via buttons in the `Generate` card on the UI

### Format

- The first row is an indicator for the `[links]` section
- The second and third rows contain direct links (enclosed in quotes) to the `faq` and `other` files

      ```text
      [links]
      faq = "https://docs.google.com/spreadsheets/d/identifier/edit?usp=drive_link"
      other = "https://drive.google.com/file/d/identifier/view?usp=drive_link"
      ```

### Update

If the direct links to the files change (which happens often with `Other.txt`), simply update the links in this file. Any changes will be automatically reflected on the UI within a short period of time

## Status Indicators

The [Overall Status](#overall-status-check-icon) gives an overview of whether you can/should proceed with generation, with additional indicators in its' associated popover providing insight into specific issues

### Overall Status (Check Icon)

| Color                                     | Meaning                                                                                                                                     |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| <span style="color:green;">&#9679</span>  | All systems are operational, so generation may proceed                                                                                      |
| <span style="color:yellow;">&#9679</span> | [Verified Status](#verified-status-file-icon) is red, but all systems are operational, so generation may proceed with caution               |
| <span style="color:red;">&#9679</span>    | The [Ollama Status](#ollama-status-brain-icon) and/or the [Folder Status](#folder-status-folder-icon) are red, so generation cannot proceed |

### Ollama Status (Brain Icon)

| Color                                    | Meaning                                                                  |
| ---------------------------------------- | ------------------------------------------------------------------------ |
| <span style="color:green;">&#9679</span> | Ollama and `mistral` are installed on your device                        |
| <span style="color:red;">&#9679</span>   | Ollama and/or `mistral` are NOT installed on your device. See the README |

### Folder Status (Folder Icon)

| Color                                    | Meaning                                                                                         |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------- |
| <span style="color:green;">&#9679</span> | The [FAQ](#faq-enter-herecsv) and [Other.txt](#othertxt) are present in `~/.chatbot-util/`      |
| <span style="color:red;">&#9679</span>   | The [FAQ](#faq-enter-herecsv) and/or [Other.txt](#othertxt) are missing from `~/.chatbot-util/` |

### Verified Status (File Icon)

| Color                                    | Meaning                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span style="color:green;">&#9679</span> | No entries are modified or missing in the newly generated [Permutated.csv](#permutatedcsv)                                                                                                                                                                                                                                                                     |
| <span style="color:grey;">&#9679</span>  | No new files have been generated in this session                                                                                                                                                                                                                                                                                                               |
| <span style="color:red;">&#9679</span>   | Some entries are modified and/or missing in the newly generated [Permutated.csv](#permutatedcsv). You should review before generating as this will overwrite `Permutated.csv.backup`, potentially resulting in data loss. Clicking `Okay` on the associated toast will reset this status indicator, which can be retriggered at any time by clicking this icon |
