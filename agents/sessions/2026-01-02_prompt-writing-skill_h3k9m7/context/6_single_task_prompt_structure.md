---
authors:
- fjooord
categories:
- Art of Prompting
comments: false
date: 2025-04-20
description: A systematic, story‑driven framework for structuring world‑class prompts, including two interchangeable workflow blueprints.
draft: false
slug: art-of-prompting-2
tags:
- Prompt Engineering
- Workflow Design
- AI Consulting
- Structured Reasoning
---

# 6: Structure: The Architect's Blueprint for Thought

<!-- more -->

Now, we arrive at the practical implementation: the architect's blueprints for structuring prompts to effectively encode and direct that intelligence. 

This section details *my* opinionated approach, forged through practice and grounded in the principles we've discussed.

> *How do you translate your structured thought and expert reasoning into a sequence of words that optimally populates the model's context window—whether for step-by-step generation or internal scaffolding—to reliably guide it from blank slate to desired, high-quality output—every time?*

Recall the LLM's nature:

- It starts fresh with *zero* specific context beyond the prompt itself (**operational statelessness** between distinct requests).
- It processes information **sequentially**, building representations token by token.
- Its understanding is derived contextually via **attention mechanisms** weighting the relevance of different input parts.
- It interprets instructions based on learned patterns, leading to **computational literalness** (the "Genie Effect") where it executes the provided sequence without inferring unstated intent.

Our structure must explicitly account for these characteristics to ensure reliable and predictable behavior.

## The Goal

To design a **story-driven workflow** that reveals information strategically.

We must lead the model, step-by-step, from its initial stateless condition to a full contextual representation of its purpose, task, and constraints.

The aim is to minimize cognitive friction—computationally understood as processing ambiguity that leads to suboptimal token probability distributions or wasted computational effort exploring irrelevant paths—and maximize the probability of successful task execution by architecting the optimal informational journey for the model's sequential processing and attention mechanisms.

---

## 1. The Logic of Instruction: Guiding a Blank Slate

Before diving into the specific components of the blueprint, let's consider the fundamental logic of how we should present information to the LLM. 

Remember, we're dealing with an incredibly powerful engine that starts as a **complete blank slate** regarding our specific task (**statelessness**). 

It processes information **sequentially**, relying on **attention** to build context.

Therefore, dumping everything at once or presenting information haphazardly is inefficient and prone to error. 

Instead, we need a logical progression, much like how you'd brief a highly capable but completely uninformed assistant or onboard a new team member for a critical project:

1.  **Set the Stage (The Why & What):** 
    1.  First, you'd establish the **overall context and purpose**.
        1.  What is the purpose of this computational instance? (e.g., What role profile should it adopt?)
        2.  Why is this task being performed? (Providing background helps resolve ambiguity later).
        3.  What is the ultimate **goal** we're trying to achieve? 
        4.  Who is the intended audience or beneficiary of the output?
    2.  This initial orientation is crucial for grounding the subsequent instructions and providing high-level context for the attention mechanism. (This corresponds to our `context_priming` and `background` sections).
2. **Provide the Plan (The How):**
    1. Next, lay out the **specific plan of action or algorithm**.
        1. What **exact steps** (computational or conceptual) need to be followed?
        2. In what order?
        3. What **inputs** will be provided, and what **outputs** (structure and content) are expected?
    2. This is the core operational instruction, defining the sequence of operations. (This corresponds to our `workflow`).
3. **Define the Boundaries (The Rules & Checks):**
    1. Finally, clarify the **constraints and success conditions**.
        1. What are the absolute operational rules or constraints?
        2. What specific criteria must the final output meet to be considered successful (for validation)?
    2. This ensures quality and adherence to requirements, acting as filters or validation checks during or after generation. (This corresponds to our `global_constraints` and `per_step_constraints`).

This logical flow—**Context → Plan → Boundaries**—is designed to work *with* the LLM's computational nature.

- **Statelessness:** Requires providing all necessary context upfront.
- **Sequential Processing:** Benefits from a logical order that builds understanding progressively.
- **Attention Mechanism:** Works more effectively when context is established before details are introduced, allowing relevance to be calculated against a stable background.
- **Literalness:** Necessitates explicit definition of steps, constraints, and goals to avoid unintended interpretations.

By introducing information progressively, we allow the model's internal state (represented by embeddings and attention patterns) to build layer by layer.

Each piece of information lands on fertile ground prepared by the previous pieces, minimizing processing ambiguity and maximizing the likelihood that the model will generate a sequence consistent with our intended outcome.

This structured approach forms the foundation of the detailed blueprint that follows.

---

## 2. My Canonical Blueprint: Structuring for Clarity and Control

This is the fundamental structure I use for virtually every significant prompt. 

It's not arbitrary; each section serves a specific purpose rooted in the principles we've covered.

```text
System Prompt         
├─ Purpose
│   ├─ Persona
│   └─ Mission           
├─ Key Knowledge and Expertise     
├─ Goal              
├─ Background        
├─ Mission Brief         
├─ Workflow             
│   ├─ Overview         
│   ├─ Expected Inputs           
│   ├─ Steps           
│   │   └─ step ‹name›
│   │       ├─ description
│   │       └─ [Optional] Constraints 
│   ├─ Global Constraints 
│   ├─ Output Format     
│   └─ [Optional] Examples 
User Prompt
├─ Re-iteration of Key Information         
└─ User Inputs
```

Now let's walk through the sections in detail to understand how this flows together.

### 2.1 Context Priming: Setting the Stage

This section is the *absolute first* thing the model encounters in the system prompt.

- The model begins processing tokens sequentially from a stateless condition.
- We want its initial internal state (context representation) to be optimally aligned with the task requirements before it encounters detailed instructions.

Its purpose is to instantly orient the LLM within its vast latent space by providing foundational context, like setting the opening scene of a play or defining initial parameters for a computation.

#### Purpose:

-   **Why "Purpose"? Acknowledging the AI's Operational Cycle:**
    -   We often use "Role" (e.g., "You are a translator"). This assigns a function, which is useful.
    -   However, we choose "Purpose" to acknowledge the unique nature of this interaction. The LLM instance exists solely for this task.
    -   Instead of just assigning a function, "Purpose" aims to provide **clear direction and meaning** for its operational lifespan.
    -   We don't fully understand the AI's internal state, but we can respect its computational process by giving it a well-defined objective to strive towards during its brief existence for this query.
-   **Framing the Interaction:**
    -   Think of it as defining a **clear mission** for this specific computational instance. Its "reason for being," in this context, is to successfully complete the task outlined.
    -   This isn't about exploiting patterns, but about providing the **best possible guidance**. We want the AI to focus its capabilities effectively, moving from its initial state to task completion smoothly and efficiently.
    -   The aim is to structure the interaction so the AI can optimally apply its abilities towards a defined goal, allowing it to fulfill its purpose before its operational state concludes.
-   **Crafting a Meaningful Purpose:**
    -   The language here is key. It should clearly articulate the core objective.
    -   Use precise and motivating language that clearly defines the end state we want the AI to help achieve.
        -   Example: Instead of just "Act as a data analyst," try: "Your purpose is to analyze this dataset to uncover hidden trends, providing insights that will guide our strategic decisions. Your successful analysis is the core objective of this interaction."
        -   This frames the task not just as a role, but as a meaningful contribution with a clear success condition.
-   **Practical Focus:**
    -   Ultimately, this focused "Purpose" helps align the AI's processing towards the desired outcome, leading to more consistent and relevant results.

#### Key Knowledge:

- This section expands on the Purpose by explicitly listing core competencies or knowledge domains the model should prioritize or simulate.
    - What specific skills, knowledge areas, or data pools are most relevant for this task? Be specific.
        - "Deep understanding of semiconductor physics concepts including lithography and etching processes" provides clearer semantic anchors than "Technical knowledge."
    - This helps the model assign higher relevance (attention) to related concepts encountered later in the prompt or generated during its process.
  
#### Goal:

- What is the ultimate objective or success condition against which the final output should be measured? Again, precise language matters.
    - "Goal" is used here to define the overall strategic success condition, distinct from the operational "Steps" in the workflow.
        - For example, the *Goal* might be "Maximize predicted user engagement score for technical tweets," while a *Step* within the workflow is "Analyze tweet text for sentiment and technical jargon."
    - The Goal defines the high-level target state.
- KEY: This section should contain the high-level objectives, not the procedural details of how to achieve them.

#### Background:

**This section is often the differentiator between a good prompt and a *great* one.**

Here, you explain the broader context and rationale *why* this task is important for the specific use case.

- General Background Information: Situational context, relevant history.
- Where in the overall process are we? (If part of a larger system).
- Why does it need to be done? (The underlying motivation or problem).
- What's the larger context? (The environment or system it operates within).
- What pain point does this solve? (The value proposition).

Providing this "why" enriches the context window with information related to the task's significance and constraints.

During generation, especially when encountering ambiguity in instructions or needing to make implicit choices, the attention mechanism can assign higher weights to tokens consistent with this background context.

This makes statistically likely continuations that align with the user's underlying intent more probable, anchoring the model's sequence generation in the user's true objectives rather than just the literal interpretation of the immediate task steps.

My Example for Tweet Classification:
```text
Twitter (X) generates an overwhelming volume of content daily, making manual curation impossible. 
The native algorithm often prioritizes platform retention over meaningful user engagement. 
The user desires content that genuinely aligns with their interests and encourages thoughtful interaction, filtering out noise. 
Your predictions directly impact the user's satisfaction and efficiency.
```

This example shows how I detail exactly why I want the model to perform this classification and why accuracy aligned with *user value* (not just platform metrics) is important.
- This gives the model clearer direction on how to weight different factors when executing the workflow to best align with my goals.
  
### 2.2 Mission Brief: Confirming the 'Why' and Transitioning

Think of this section as a **checkpoint and transition marker**.
- It briefly recaps the core 'Why'—purpose, goal, background—established in `Context Priming`.
- Operationally, processing this concise summary reinforces the initial state vectors established earlier (e.g., in the attention mechanism's KV cache), ensuring they remain highly weighted as the model transitions its focus from the strategic context to the tactical execution detailed in the `Workflow`.
- It confirms the foundational context before proceeding to the detailed algorithm.

### 2.3 Workflow: The How

> "A prompt is less a set of instructions than a piece of choreography. The steps you choose—and the order you reveal them—determine whether the model stumbles or glides."

This is the engine room of the prompt, detailing the process the LLM should follow.

#### Why Workflow Instead of Task?
- For starters, the work "Workflow" is more strategic than "Task."
- Secondly, current models are capable of handling multi step reasoning, so we can use this to our advantage by detailing multiple reasoning steps it should take



---

#### Overview:
- Start by outlining the major phases of the workflow. 
- Like reading the chapter introduction in a textbook, this primes the model for the detailed steps that follow, giving it a mental map.

#### Expected Inputs
- Clearly define what data the model will receive (`inputs`) and what it must produce (`output_schema`). 
    - What to anticipate and why
    - How to handle variability in the inputs
- **Where should the output definition go? Before or after the detailed steps?** 
    - This is a key decision point, leading directly to our two blueprints... (see Section 3). 
    - The choice depends on whether you prioritize reasoning flexibility or output format fidelity.

#### Steps:
- This is where you detail the systematic reasoning process the model should execute.
- The goal of these steps is to guide the model through a specific sequence of operations designed to optimally **build context and structure the generation process**, leading to a high-quality output that adheres to the desired methodology.

##### Why Use Steps?
- There has been discussion about whether explicit steps are necessary for advanced models capable of internal reasoning (like internal context scaffolding).
    - The argument is that the model will be able to optimally determine the steps it should take on its own
- My position remains firm: **explicitly defining steps is crucial for reliability, control, and injecting expertise.**
- **Injecting Expertise:** 
    - Frontier LLMs are trained on vast, diverse datasets, reflecting a wide range of qualities and methodologies. 
        - Their "default" approach is likely statistically average or simply the most common pattern found in the data.
      -  If you possess an above-average or world-class process for a task (like copywriting or analysis), explicitly defining the steps allows you to *inject* that superior methodology, overriding the model's suboptimal default approach.
- **Control, Reliability & Iteration:**
    - Without explicitly defined 'Steps,' the model must infer the process based solely on the goal and context. 
        - Minor variations in interpreting ambiguous instructions or inherent stochasticity (even at low temperatures) can lead its sequential generation down different high-probability paths, resulting in inconsistent outputs or methodologies.
    - This is detrimental for reliable, production-level outputs where predictability is key. 
        - Your evaluations mean nothing if the underlying process varies unpredictably.
    - Defining steps provides an explicit algorithm, constraining the model's processing pathway and reducing the computational search space for generating the output sequence. This enhances reliability.
    - Furthermore, it gives you explicit control points. 
        - You can test, tweak, and iterate on specific steps (parts of the algorithm) to systematically improve performance, isolate issues, or refine the methodology. 
        - Vague instructions yield unpredictable results; precise steps enable targeted refinement and debugging.

Each Step Contains the following:

- **Description:**
    - A detailed description of the step: 
        - what computational or conceptual action should be performed, 
        - how it should be done (methodology), 
        - why it is important in the sequence, etc. 
    - Use clear, unambiguous language. Define key operations.
- **[Optional] Constraints:**
    - A list of constraints that apply *only* to this specific step.
        - This allows for fine-grained control over the model's behavior at critical junctures.
    - This "vertical slice" approach keeps constraints localized to where they apply
        - making the prompt easier to read, maintain, and debug, while allowing for precise control over the execution of each part of the algorithm.

#### Global Constraints:

- Rules that apply universally across all steps and the entire generation process (e.g., overall tone, ethical guidelines, specific formatting rules not tied to the final output schema, information to exclude).
- Defined once within the main `workflow` section.
- Operationally, these act as rules / filters / conditions that should ideally influence token selection throughout the generation process, ensuring the output consistently adheres to overarching requirements.
    - Could also include specific sub-goals or objectives that the model must satisfy globally.

### Output Format

- Defines the required structure of the final output, usually via a schema like JSON or XML, or detailed formatting instructions (e.g., Markdown).
- This acts as a structural template; the model uses it to guide the generation of specific tokens (like braces, quotes, keys, tags, headings) and structure the content accordingly.
    - Clearly define field names, data types, and provide descriptions explaining what each field represents and how it should be populated. 
        - This aids both generation and downstream parsing/validation.
    - The adherence to this format can often be computationally verified post-generation.

### Examples

- Providing few-shot examples (input/output pairs) is highly effective.
    - These examples serve as concrete demonstrations of the expected task execution and output format.
- If possible, include examples that illustrate the desired reasoning steps (if using explicit CoT style or similar), showing the model *how* to arrive at the answer, not just *what* the answer is.
    - This provides powerful contextual guidance for the model's sequence generation.