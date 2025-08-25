# Healthcare Diagnoses System
# Scenario

A healthcare client wants a secure AI assistant for doctors that:
Summarizes patient history from EHR notes.
Suggests possible diagnoses based on symptoms.
Must comply with HIPAA and store no PHI outside their cloud.

# Tasks

Draw a high-level architecture diagram (components, data flow, and security layers).
Recommend a technology stack (LLM, RAG framework, cloud infrastructure, etc.).
Describe three key trade-offs in your design (e.g., accuracy vs. latency, open-source vs.
closed-source models).

# Deliverable

Architecture diagram.
Tech stack description.
Trade-off analysis.

## Architecture Diagram

![Architecture Diagram](./architecture-diagram.png)

## Technology  Stack 

- **AWS Cloud Infrastructure**
    - **Amazon Elastic Kubernetes Service (EKS):** Orchestrates containerized microservices for scalability, high availability, and secure workload isolation. Hosts backend APIs, LLM inference, and retrieval services.
    - **Amazon API Gateway:** Provides a secure, scalable entry point for all API requests from the frontend, enabling authentication, throttling, and monitoring.
    - **Istio Service Mesh:** Manages secure service-to-service communication, enforces policies, and provides observability for microservices within the Kubernetes cluster.
- **Frontend & Backend**
    - **ReactJS Frontend:** Delivers a responsive, user-friendly interface for doctors to interact with the assistant, view patient summaries, and input symptoms.
    - **FastAPI Backend:** Handles business logic, orchestrates calls to the retriever, LLM, and prompt builder, and enforces security and compliance checks.
- **Vector Database**
    - **Pinecone:** Stores and indexes EHR notes and diagnostic data as vector embeddings for fast, semantic search and retrieval. Ensures data is encrypted and remains within the client’s cloud environment.
- **Prompt Builder Service**
    - **Prompt Builder API:** Dynamically constructs prompts for the LLM by combining retrieved EHR data, predefined system instructions, and user input, ensuring contextually relevant and compliant queries.
- **Large Language Model (LLM)**
    - **Local LLM (Fine-tuned on Medical Data):** Runs within the client’s secure cloud, trained on de-identified medical datasets to generate accurate, domain-specific summaries and diagnostic suggestions. No PHI leaves the environment.
- **Retriever Service**
    - **Medical Retriever:** Searches EHR notes and medical literature for relevant information. Integrates:
        - **Guardrails to filter out PHI:** Ensures no protected health information is exposed to the LLM or external systems.
        - **Guardrails for HIPAA compliance:** Enforces data handling and access policies to meet regulatory requirements.
        - **Metadata Handling:** Attaches provenance and context to retrieved data for traceability.
        - **Rerank for Large Data:** Prioritizes the most relevant results when dealing with extensive patient histories or literature.
- **Monitoring & Observability**
    - **Prometheus:** Collects and visualizes metrics from all system components for real-time health monitoring and alerting.
    - **CloudTrail:** Logs all API calls and user actions for auditability and compliance tracking.
    - **GuardDuty:** Continuously monitors for security threats and anomalous activity within the AWS environment.
    - **Langsmith:** Tracks LLM performance, prompt effectiveness, and error rates to support ongoing model improvement and compliance reporting.

## Trade-Off Analysis

- **Accuracy vs. Latency:**  
    Achieving high diagnostic accuracy often requires retrieving and processing more data, which can increase response times. However, clinicians need timely feedback, especially in urgent scenarios. To balance this, the system can route simple cases to lightweight, faster LLMs for immediate answers, while reserving more comprehensive retrieval and analysis for complex cases where accuracy is paramount.

- **Privacy vs. Innovation:**  
    Strict privacy requirements (e.g., HIPAA) are essential in healthcare but can slow down the adoption of new technologies. Every new model or integration must undergo rigorous privacy and security assessments, which can limit experimentation and rapid iteration. While this ensures patient data is protected, it may delay or restrict the use of cutting-edge LLMs or external services.

- **Open-Source vs. Closed-Source Models:**  
    Open-source models offer transparency and the ability to customize or fine-tune for specific medical domains, which is valuable if in-house expertise is available. However, they require more maintenance and security vetting. Closed-source models, while less transparent, are typically easier to deploy, come with vendor support, and may offer better performance out-of-the-box, but limit customization and insight into model behavior.

- **Fine-Tuning vs. Retrieval-Augmented Generation (RAG):**  
    Fine-tuning an LLM on medical data can improve accuracy for specific tasks but requires access to high-quality, de-identified datasets and ongoing maintenance. RAG leverages external knowledge bases (like EHRs or medical literature) at inference time, reducing the need for frequent retraining and enabling up-to-date information retrieval. However, RAG systems add complexity and may introduce latency or retrieval errors.

- **Vector Database Selection (Pinecone vs. Weaviate):**  
    Pinecone is a fully managed service, making it easy to deploy and scale for real-time semantic search, but offers less flexibility for custom queries. Weaviate provides more control, including GraphQL support for hybrid search and advanced filtering, which can be advantageous for complex medical data scenarios, but may require more operational overhead to manage and secure.