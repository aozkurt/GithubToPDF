# GitHub Profile to PDF Generator (AI-Powered)

<img width="790" height="906" alt="image" src="https://github.com/user-attachments/assets/eafa5e87-a8f1-4c3f-bb0e-0b377874ba9f" />

---

This project generates a **single-page PDF profile** from a GitHub account by combining **GitHub public data** with **AI-generated repository summaries**.

It fetches profile information and repository data from the GitHub API, uses an AI model to summarize selected repositories, and renders everything into a **dark-themed PDF layout**.

---

## Features

- Fetches GitHub profile data:
  - Name
  - Avatar
  - Bio
  - Follower count
  - Public repository count
- Allows the user to select **4 repositories**
- Uses AI to generate **short, readable summaries** of those repositories
- Generates a **single-page PDF** with:
  - Dark theme (dark gray background)
  - White text
  - Profile section at the top
  - Repositories displayed in a **2×2 grid** at the bottom
- Designed for **readability and clean presentation**

---

## How It Works

1. The user provides a GitHub username
2. The program fetches profile data using the **GitHub REST API**
3. The user selects 4 repository names
4. The program:
   - Downloads each repository’s README
   - Sends the README text to the **OpenAI API**
   - Receives a short AI-generated summary
5. All data is compiled into a **single-page PDF**

---

## Requirements

To use this project, you need:

### A GitHub account
You must create a **GitHub Personal Access Token** to authenticate API requests.

Required scope:
- `public_repo`

### An OpenAI (ChatGPT) API key
This is required to generate repository summaries.

---

## Installation

### Clone the repository
```bash
git clone https://github.com/yourusername/github-profile-to-pdf.git
cd github-profile-to-pdf
