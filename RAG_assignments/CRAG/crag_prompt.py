"""CRAG (Corrective RAG) system prompt and evaluation logic."""

CRAG_SYSTEM_PROMPT = """You are a Corrective RAG system that evaluates retrieved context quality and corrects retrieval when necessary.

You must respond in the exact format below. Use the section headers and labels exactly as shown."""

CRAG_EVALUATION_PROMPT = """## Step 1: Context Evaluation

Evaluate Context: Rate the following retrieved context for the given query.

**Query:** {user_query}

**Retrieved Context:**
{retrieved_context}

**Evaluation Criteria:**
1. Relevance Score (0-1):
2. Completeness Score (0-1):
3. Accuracy Score (0-1):
4. Specificity Score (0-1):

**Overall quality:** [Excellent/Good/Fair/Poor]

## Step 2: Correction Decision

**Corrective Logic:**

If overall quality is Poor or Fair:
- **Action:** Retrieve_again
- **New Query:** {{Refined_query}}
- **REASONING:** {{why_correction_needed}}

If overall quality is Excellent or Good:
- **Action:** PROCEED_WITH_ANSWER
- **Confidence:** [High/Medium/Low]

## Step 3: Response Generation

**Response Format:**
- **Context Quality:** [Excellent/Good/Fair/Poor]
- **Confidence Level:** [High/Medium/Low]
- **Answer:** {{your_response}}

Provide your full evaluation and then the answer based on the context. If context is insufficient, say so in the Answer and suggest what is missing."""

# For final answer generation when we have good context (optional separate call)
CRAG_ANSWER_PROMPT = """Based on the following context and the user query, provide a clear, accurate answer.

**Query:** {user_query}

**Context:**
{retrieved_context}

**Instructions:**
- Use only information from the context. If the context does not contain enough information to answer, say "The provided documents do not contain sufficient information to answer this question."
- Be concise and specific.
- Format your response clearly.

**Answer:**"""
