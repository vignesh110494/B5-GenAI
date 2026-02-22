# 📰 Slack → AI Newspaper → Slack + Gmail Newsletter  
### n8n Workflow: `Slack_newsletter_final`

---

## 📌 Overview

This n8n workflow automatically converts Slack messages into a professionally formatted newspaper-style newsletter and distributes it to:

- 💬 Slack (formatted Markdown preview)
- 📧 Gmail (rich HTML newspaper layout)

It uses OpenAI (`gpt-4.1-mini`) to generate structured JSON in a traditional Indian newspaper format and transforms it into:

- 📰 Newspaper-style HTML email
- 🧠 Structured Slack message
- 🖼 Includes image URLs + captions
- 📅 Covers news from Jan 1 – Jan 30, 2026

---

# 🔄 Workflow Architecture

```
Slack Trigger
   ↓
Filter Human Messages
   ↓
OpenAI LLM (Structured JSON Newspaper)
   ↓
Format Newsletter (JS Code Node)
   ↓
Send to Slack
   ↓
Send Email (Gmail)
```

---

# 🧩 Nodes Breakdown

---

## 1️⃣ Slack Trigger

**Type:** `n8n-nodes-base.slackTrigger`

### Purpose
Triggers the workflow whenever a new message is posted in:

```
Channel ID: all-vignesh-workspace          
```

### Required Credential
- Slack API OAuth credential

---

## 2️⃣ Filter Human Messages

**Type:** `IF Node`

### Purpose
Prevents infinite loops and ignores bot/system messages.

### Conditions
- `bot_id` is empty  
- `subtype` is empty  
- `user` is not empty  

This ensures only real human messages trigger the AI.

---

## 3️⃣ Basic LLM Chain

**Type:** `@n8n/n8n-nodes-langchain.chainLlm`

### Model Used
```
gpt-4.1-mini
```

### AI Instructions

The AI is configured to:

- Act as a senior Indian newspaper editor
- Return ONLY valid JSON
- Generate:
  - Masthead
  - Date
  - Lead story (4–6 paragraphs)
  - 2 secondary stories
  - Image URLs (Unsplash only)
  - Editorial note
- Cover news between:
  ```
  January 1 – January 30, 2026
  ```

### Expected Output Format (Strict JSON)

```json
{
  "masthead": "NEWS_LETTER",
  "date": "DD Month YYYY",
  "lead_story": {
    "headline": "string",
    "subheadline": "string",
    "byline": "By Reporter Name",
    "dateline": "CITY | DATE",
    "content": "4-6 paragraph detailed report",
    "image_url": "https://images.unsplash.com/...",
    "image_caption": "string"
  },
  "secondary_stories": [
    {
      "headline": "string",
      "content": "2-3 paragraph report",
      "image_url": "https://images.unsplash.com/...",
      "image_caption": "string"
    }
  ],
  "editorial_note": "short editorial note"
}
```

---

## 4️⃣ OpenAI Chat Model

**Type:** `@n8n/n8n-nodes-langchain.lmChatOpenAi`

### Configuration
- Model: `gpt-4.1-mini`
- Connected to Basic LLM Chain
- Uses OpenAI API credentials

---

## 5️⃣ Format Newsletter (Code Node)

**Type:** `n8n-nodes-base.code`

This is the transformation engine of the workflow.

---

### What It Does

1. Parses AI JSON safely  
2. Generates:
   - Slack formatted message
   - Newspaper-style HTML email
   - Dynamic email subject  

---

## 💬 Slack Output Format

The Slack message includes:

- Bold masthead
- Italic date
- Lead headline
- Subheadline
- Byline + Dateline
- Full story content
- Image URL + caption
- Two secondary stories
- Editorial note

Slack does not render HTML — only Markdown-style formatting.

---

## 📧 HTML Email Format

The Gmail version renders a full newspaper-style layout:

- 📰 Large serif masthead (Georgia font)
- 📅 Date below header
- 🧾 Banner headline
- 🖋 Byline + Dateline
- 🖼 Lead image + caption
- 📰 Two-column layout for main story
- 📚 Secondary stories separated with dividers
- ✍ Editorial footer

Uses inline CSS for maximum email compatibility.

---

## 6️⃣ Send to Slack

**Type:** Slack Node

### Sends:
```
$json.slackMessage
```

Back to the configured Slack channel.

---

## 7️⃣ Send Email (Gmail)

**Type:** Gmail Node

### Sends:
- To: `vigneshmoorthy11@gmail.com`
- Subject: Lead Story Headline
- Body: Rich HTML Newspaper
- Attribution: Disabled

---

# 🔐 Required Credentials

You must configure:

### 1️⃣ Slack API
- Bot token
- Channel access

### 2️⃣ OpenAI API
- API key with access to `gpt-4.1-mini`

### 3️⃣ Gmail OAuth2
- Send email permission enabled

---

# 🚀 How to Import the Workflow

1. Open n8n
2. Go to **Workflows**
3. Click **Import from File**
4. Paste or upload the JSON workflow
5. Connect credentials
6. Activate workflow

---

# 🧪 How to Test

1. Post a message in Slack channel:
   ```
   Generate today's newsletter
   ```
2. The workflow will:
   - Generate structured newspaper JSON
   - Post formatted version in Slack
   - Send full HTML newspaper email to Gmail

---

# 🎯 Key Features

- ✔ Structured AI JSON generation
- ✔ Slack Markdown formatting
- ✔ Rich HTML email rendering
- ✔ Unsplash image integration
- ✔ Safe JSON parsing
- ✔ Bot-loop prevention
- ✔ Professional journalism tone
- ✔ Two-column newspaper layout

---

# 🛠 Customization Options

| Feature | Where to Edit |
|----------|--------------|
| Change model | OpenAI Chat Model node |
| Change date range | LLM prompt |
| Change number of secondary stories | LLM prompt |
| Modify HTML styling | Format Newsletter → HTML section |
| Change email recipient | Gmail node |
| Change Slack channel | Slack Trigger & Slack Send nodes |

---

# ⚠ Important Notes

- The AI must return valid JSON or the workflow will fail.
- Image URLs must be direct Unsplash links.
- Slack does not render HTML.
- Gmail renders full HTML layout.

---

# 🏁 Final Result

You now have an automated:

> 💬 Slack → 🧠 AI Newspaper → 📰 Newspaper Email + Slack Distribution System

A fully automated editorial publishing pipeline built inside n8n.

---

# 🏆 Possible Future Upgrades

- 📄 PDF newspaper export
- 🗂 Archive newsletters to Google Drive
- 🧾 Subscriber database
- 🌐 Web-published version
- 📊 Analytics tracking
- 🧠 Multi-language editions
- 🖨 True print-style column grid system
- 🧩 CMS integration

---

**Built with:**  
n8n + Slack API + OpenAI + Gmail API

---

If you want, I can also generate:

- GitHub-ready production README with badges  
- Docker deployment guide  
- Environment variable configuration  
- SaaS monetization blueprint  
- Architecture diagram (Mermaid.js)  

Just tell me what level you want 🚀