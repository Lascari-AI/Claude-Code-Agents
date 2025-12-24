# Information-Dense Keywords (IDKs) for AI Coding

## Introduction

Modern AI coding assistants can generate and edit code faster than ever. 

However, there’s a key bottleneck: we need to communicate our intentions clearly. 

Traditional programming relies on precise syntaxes, while AI coding uses natural language instructions—leaving more room for ambiguity. 

That’s where Information-Dense Keywords (IDKs) come in.

## What Are IDKs?

Information-Dense Keywords (IDKs) are single words or short phrases that pack a high level of meaning relevant to coding tasks. 

They work similarly to a CPU’s instruction set, but for AI coding:
- Each IDK tells the AI exactly what operation to perform (CREATE, MOVE, ADD, REFACTOR, etc.).
- By bundling clear, immediate meaning into concise terms, IDKs help reduce misunderstandings and misinterpretations.
- Using IDKs consistently can boost accuracy and reduce the back-and-forth needed to get your code done “right the first time.”

## Why Use IDKs?

1.	Precision & Clarity
    - Common English words can be vague: “improve” or “enhance” might mean many different things. 
    - IDKs, on the other hand, are domain-specific instructions for code-based tasks, minimizing ambiguity.

2.	Faster Development Cycles
    - When an AI coding assistant has to infer your intent from ambiguous language, it may produce incorrect or partial results. 
    - With IDKs, you speak its “native” language for instructions—leading to fewer corrections, fewer wasted tokens, and time saved.

3.	Reusable Prompt Patterns
    - Over time, you’ll build a consistent “vocabulary” of IDKs. By reusing these same words, your prompts become more standardized, and the AI becomes more predictable.

4.	Scalable Collaboration
    - If your whole team uses IDKs in prompts, everyone shares a common “instruction set.” 
    - This yields consistent code updates, even when multiple people (and multiple AI coding assistants) are involved.

## The “Instruction Set” Mentality

In CPU architecture, an “instruction set” defines the lowest-level operations (like MOV, ADD, JMP) that a processor can perform. 

For AI coding:
- CPU ↔ AI Model
    - The CPU is replaced by the AI/LLM, which consumes your text-based instructions.
- Opcodes ↔ IDKs
    - Our IDKs are the “opcodes” that encode precisely what the AI should do to your code.
- Assembly ↔ Prompt
    - Instead of writing assembly instructions, you write prompt lines using IDKs to convey meaning quickly.

By thinking of IDKs as “opcodes”, you leverage the AI’s pattern recognition capabilities. 

You effectively give the model short, direct instructions on how to transform the code—like a specialized, mini-language of your own design.

## About This Document

This README introduces the core concept of IDKs. 

Immediately following, you’ll find an IDK Instruction Set reference that defines each keyword, explains its meaning, and illustrates how to use it in prompts.

1.	Intro – You’re here!
    - A high-level overview of why IDKs matter and how they fit into AI coding.

2.	IDK Instruction Set – The heart of it all:
    - Categories (CRUD, Actions, Refactoring, Testing, etc.)
    - Detailed Definitions for each keyword (e.g. CREATE, UPDATE, MIRROR, APPEND)
    - Examples of usage in real prompts

3.	Usage Tips
    - Quick best practices on combining IDKs with references to files, function names, variables, or line numbers to eliminate ambiguity in prompts.

How to Get Started
- Skim the IDK list. Notice how each word has a concise meaning.
- Choose relevant IDKs for the tasks you typically do (e.g., CREATE file, MOVE function, REFACTOR loop).
- Practice writing prompts that combine these IDKs with details like filenames, function names, or even lines of code. For instance:

```aider
CREATE file data_transformer.py:
    CREATE FUNCTION def transform_data(data: List[Dict]) -> List[Dict]:
        # ...
```

- Refine your prompts. After each run, see if the AI meets your expectations. If not, check if you can clarify with a more direct IDK or more context.