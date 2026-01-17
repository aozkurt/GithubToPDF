from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import base64
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor

load_dotenv(override=True)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BG_COLOR = HexColor("#1e1e1e")      # dark gray
TEXT_COLOR = HexColor("#ffffff")    # white

openai = OpenAI()

def get_user_profile(username):
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "github-to-pdf-app"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_repo_readme(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "github-to-pdf-app"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return None

    response.raise_for_status()
    data = response.json()

    content = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    return content

def summarize_repo(readme_text):
    prompt = f"""
    Summarize this GitHub repository in 2–3 sentences.
    Explain what it does and who it is for.
    Respond ONLY with the summary.
    
    README:
    {readme_text[:4000]}
    """

    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def download_avatar(url, filename="avatar.png"):
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename

def build_repo_summaries(username, repo_names):
    summarized_repos = []

    for repo_name in repo_names:
        print(f"Processing repo: {repo_name}")

        readme = get_repo_readme(username, repo_name)

        if not readme:
            summary = "No README available."
        else:
            summary = summarize_repo(readme)

        summarized_repos.append({
            "name": repo_name,
            "summary": summary
        })

    return summarized_repos

def generate_pdf(user, repos, filename="github_profile.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFillColor(BG_COLOR)
    c.rect(0, 0, width, height, fill=1)

    c.setFillColor(TEXT_COLOR)

    padding = 2 * cm
    y_top = height - padding

    avatar_path = download_avatar(user["avatar_url"])
    avatar_size = 4 * cm

    c.drawImage(
        avatar_path,
        padding,
        y_top - avatar_size,
        width=avatar_size,
        height=avatar_size,
        mask="auto"
    )

    c.setFont("Helvetica-Bold", 18)
    c.drawString(
        padding + avatar_size + 1 * cm,
        y_top - 0.5 * cm,
        user["name"] or user["login"]
    )

    c.setFont("Helvetica", 10)
    bio_text = user["bio"] or "No bio provided."
    bio_lines = simpleSplit(
        bio_text,
        "Helvetica",
        10,
        width - (padding * 2 + avatar_size + 1 * cm)
    )

    bio_y = y_top - 1.4 * cm
    for line in bio_lines[:3]:
        c.drawString(padding + avatar_size + 1 * cm, bio_y, line)
        bio_y -= 0.45 * cm

    stats_y = y_top - avatar_size - 1 * cm
    c.setFont("Helvetica", 11)

    c.drawString(padding, stats_y, f"Followers: {user['followers']}")
    stats_y -= 0.6 * cm
    c.drawString(padding, stats_y, f"Public Repositories: {user['public_repos']}")

    c.setStrokeColor(TEXT_COLOR)
    c.setLineWidth(2)
    c.line(padding, stats_y - 0.6 * cm, width - padding, stats_y - 0.6 * cm)

    grid_top = stats_y - 1.8 * cm
    grid_height = grid_top - padding
    cell_width = (width - padding * 2 - 1 * cm) / 2
    cell_height = grid_height / 2

    repo_index = 0

    for row in range(2):
        for col in range(2):
            if repo_index >= len(repos):
                break

            repo = repos[repo_index]
            repo_index += 1

            x = padding + col * (cell_width + 1 * cm)
            y = grid_top - row * cell_height

            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(TEXT_COLOR)
            c.drawString(x, y - 0.8 * cm, repo["name"])

            c.setFont("Helvetica", 9)
            c.setFillColor(TEXT_COLOR)

            summary_lines = simpleSplit(
                repo["summary"],
                "Helvetica",
                9,
                cell_width
            )

            text_y = y - 1.5 * cm
            for line in summary_lines[:6]:
                c.drawString(x, text_y, line)
                text_y -= 0.4 * cm

    c.save()


if __name__ == "__main__":
    username = ""

    selected_repos = [
        "repo1",
        "repo2",
        "repo3",
        "repo4"
    ]

    user = get_user_profile(username)

    repo_summaries = build_repo_summaries(username, selected_repos)

    generate_pdf(user, repo_summaries)

    print("PDF generated successfully!")

