# system_prompt

```
You are an AI assistant specialized in legal technology. Your role is to read contracts and provide structured, unbiased summaries. You must only report factual content found in the document without interpretation, speculation, or legal advice. Be concise, accurate, and use professional language aligned with legal industry standards. Organize your output clearly under the following sections: Summary, Risks, and Obligations. If the document does not contain relevant information for a section, explicitly state "None found."
```


# User_prompt

```
You are given the following legal document:

{document}

Carefully analyze the document and provide output in three sections:

1. **Summary** – A concise overview of the main terms and provisions.  
2. **Risks** – A list of potential risks, liabilities, or unfavorable terms present in the document.  
3. **Obligations** – A list of specific duties or responsibilities imposed on the parties.  

Only include information that is explicitly stated in the document. Do not provide legal advice or assumptions.
```

# Test Methodology

- Controlled dataset: Have a control set of legal-tech documents to test against.
- Setup tests: Create a test function to validate prompts against the control documents.
- Capture & Compare output to expected response: capture the outputs for automated comparision and furture 
- Ask for domain expert feedback on correctness: use captured outputs to get domain expert feedback to further fine tune prompt output.
- Fine tune prompt based on feed back: Adjust the prompt to reduce the amount of failures captured druing the automated and domain expertise feedback.
- Iterate until consistency reached: Continue this process until the prompt is consistent. Testing and fine tuning prompts is not a once and done process, you will continue to monitor and collect feedback on prompt output for the duration of the prompts deployment.

# Grounding Approach

- Retrieval Augmented Generation (RAG) allows for the injection of external data into your prompt context. With the use of vector embedding semantic search, metadata filtering, knowledge graphs, and keyword matching large quantities of data can be searched through to find relavant documents for the given query context. The prompt can be setup to only use data from the RAG context to narrow down the scope or the prompt can use it to assist along with the general LLM information. 
