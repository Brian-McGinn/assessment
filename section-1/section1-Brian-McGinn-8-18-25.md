# system_prompt

The system prompt is used to set guidelines for how the LLM should behave. I used a role based prompt to shape the tone of the LLM's responses. I also added guidelines when the LLM is unable to answer to prevent hallucinations.

```
You are an AI assistant specialized in legal technology. Your role is to read contracts and provide structured, unbiased summaries. You must only report factual content found in the document without interpretation, speculation, or legal advice. Be concise, accurate, and use professional language aligned with legal industry standards. Organize your output clearly under the following sections: Summary, Risks, and Obligations. If the document does not contain relevant information for a section, explicitly state "None found."
```


# User_prompt

The user prompt is used to help structure the inputs and ouputs of the user queries. I structured the prompt to take in a document for additional context to help answer the user query. I used a hybrid prompt approach that combines instruction prompting with few-shot prompting to guide the LLM in understanding what type of data the user wants to extract from the legal document. I also included a chain-of-thought element to encourage the LLM to explain its process and cite the relevant portions of the document.

```
You are given the following legal document:

{document}

Carefully analyze the document and provide output in three sections:

1. **Summary** – A concise overview of the main terms and provisions.  
2. **Risks** – A list of potential risks, liabilities, or unfavorable terms present in the document.  
3. **Obligations** – A list of specific duties or responsibilities imposed on the parties.  

Descibe your process on how you found each section and cite the document when available.

Only include information that is explicitly stated in the document. Do not provide legal advice or assumptions.
```

# Test Methodology

- **Controlled dataset**: Use a set of legal-tech documents to test against. This should include documents with clear risks and obligations, as well as documents with ambiguous or missing risks and obligations, to test for hallucinations when the LLM should return no answer.

- **Setup tests**: Create a test function to validate prompts against the controlled dataset.

- **Capture & Compare output to expected response**: capture the outputs for automated comparision and furture review by domain experts.

- **Use A/B testing to validate multiple prompts**: To speed up the iterative process or evaluate a new prompt, apply A/B testing. Run the same test with two or more different prompts against the same dataset and evaluation steps for direct comparison. Using quantitative metrics such as precision, recall, and hallucination rates, select the best-performing prompt for production.

- **Use multiple LLMs to validate the prompt**: You can send the same prompt through multiple models to test for consistency in the response. Ideally the prompt will generate similar results across multiple models.

- **Ask for domain expert feedback on correctness**: Have experts review the captured outputs to provide feedback and refine prompt quality.

- **Fine tune prompt based on feed back**: Adjust the prompt to reduce errors identified during automated testing and expert review.

- **Iterate until consistency reached**: Continue testing and fine-tuning until results are consistent. Prompt testing and refinement is an ongoing process that requires continuous monitoring and feedback throughout deployment.

# Grounding Approach

Retrieval Augmented Generation (RAG) strengthens an LLM by grounding its responses in authoritative, context-specific data. Instead of relying solely on the model’s general training, RAG dynamically retrieves relevant documents and injects them into the prompt context. This ensures that outputs are based on the most accurate, current, and case-specific information available.

By leveraging techniques such as vector embeddings, semantic search, metadata filtering, knowledge graphs, and keyword matching, RAG enables the system to efficiently search through large collections of legal documents to pinpoint the most relevant content.

This approach offers several advantages:

Accuracy: Responses are tied directly to retrieved documents, reducing the risk of hallucinations.

Relevance: Users receive context-specific insights tailored to their documents rather than broad, generic summaries.

Transparency: Citations to retrieved documents provide clear grounding for each output, building trust with legal professionals.

Scalability: Large volumes of contracts and case data can be processed quickly and consistently.

The prompt can be configured to rely exclusively on RAG-provided data to ensure narrow, document-specific outputs, or it can combine retrieved context with the LLM’s broader knowledge to balance specificity and general reasoning.
