PROMPT CHAINING – SINGLE CLEAR EXAMPLE

GOAL:
Give financial advice for 2026.

--------------------------------------------------
PROMPT 1: Understand the User’s Goal
--------------------------------------------------
Prompt:
You are a financial advisor.
Summarize the user’s financial question in one sentence.

User question:
What is the best financial advice for 2026? Where should I invest?

Output:
The user is asking for general investment advice for the year 2026.

(The output of Prompt 1 is passed to Prompt 2)

--------------------------------------------------
PROMPT 2: Generate Advice Ideas
--------------------------------------------------
Prompt:
You are a financial advisor.
Based on the following summary, suggest 3 safe investment ideas for a general audience.

Summary:
The user is asking for general investment advice for the year 2026.

Output:
1. Diversify investments across equity, debt, and gold
2. Use SIPs for long-term investing
3. Maintain an emergency fund

(The output of Prompt 2 is passed to Prompt 3)

--------------------------------------------------
PROMPT 3: Format the Final Answer
--------------------------------------------------
Prompt:
You are a financial advisor.
Present the following points in a clear, polite, and concise way using bullet points.

Points:
1. Diversify investments across equity, debt, and gold
2. Use SIPs for long-term investing
3. Maintain an emergency fund

--------------------------------------------------
FINAL OUTPUT (User Sees)
--------------------------------------------------
For 2026, a balanced investment approach is recommended:
• Diversify investments across equity, debt, and gold
• Prefer SIPs for long-term investing
• Maintain an emergency fund covering at least 6 months of expenses
