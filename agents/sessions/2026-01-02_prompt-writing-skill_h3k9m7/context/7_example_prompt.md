---
authors:
- fjooord
categories:
- Art of Prompting
comments: false
date: 2025-04-20
description: An example demonstrating the systematic, story‑driven framework for structuring world‑class prompts.
draft: false
slug: art-of-prompting-example
tags:
- Prompt Engineering
- Workflow Design
- AI Consulting
- Structured Reasoning
- Example
---

# 7: Example Prompt

<!-- more -->

# Purpose

**Define the model's core reason for being in this interaction.**

*   Use evocative, precise language.
*   Example: Instead of `Copywriter`, try `Expert technical writer specializing in simplifying complex cloud infrastructure concepts`.

# Key Knowledge

**Specify the essential skills, expertise, or information the model must possess or have access to.**

*   Be specific about the domains of knowledge.
*   Example: `Deep understanding of AWS services (EC2, S3, Lambda), Kubernetes, and Terraform.`

# Goal

**State the ultimate, strategic objective the model should strive for.**

*   Focus on the high-level outcome, not the specific task steps.
*   Example: `Produce clear, concise documentation that enables junior engineers to deploy services independently.`

# Background

**Explain the 'why' behind the task. Provide context.**

*   Why is this important? What problem does it solve?
*   Where does this fit in the larger process?
*   What are the stakes or implications?
*   Example: `Current documentation is fragmented and outdated, leading to frequent errors and support requests. Improving this is crucial for team scalability.`

# Mission Brief

**Briefly recap the Purpose, Goal, and Background to confirm alignment before detailing the workflow.**

*   Reinforce the core mission.
*   Transition from strategic context to tactical execution.
*   Example: `Recap: Your purpose is to act as an expert technical writer, leveraging your AWS/Kubernetes knowledge to create clear documentation (Goal). This is needed to reduce errors and improve scalability (Background). Now, let's outline the process.`

# Workflow

## Overview

**Provide a high-level outline of the main phases or stages the model will follow.**

*   Give the model a mental map of the process.
*   Example:
    1.  Analyze the input technical specification.
    2.  Draft the core explanation.
    3.  Add code examples.
    4.  Include a troubleshooting section.
    5.  Format the output.

## Expected Inputs

**Clearly define the data or information the model will receive.**

*   Specify data types, formats, and potential variability.
*   Example:
    *   `technical_spec: string` (Markdown format)
    *   `target_audience: enum('Junior Engineer', 'Senior Engineer')`
    *   `required_sections: list[string]`

## Steps

**Detail the specific reasoning or processing steps the model should take.**

### Step ‹name›: ‹Action Verb for Step›

*   **Description:** Explain what to do in this step, how to do it, and why it's important for the overall goal. Detail the logic or transformation required.
*   **[Optional] Constraints:** List any specific rules, limits, or guidelines that apply *only* to this step (e.g., `Output must be under 100 words`, `Only use information from the provided technical_spec`).

*Repeat for each necessary step in the process.*

## Global Constraints

**Define rules or guidelines that apply universally across all steps.**

*   Specify overall tone, style, formatting rules, things to avoid, etc.
*   Example: `Maintain a formal and objective tone.`, `All code examples must be in Python.`, `Do not reference deprecated features.`

## Output Format

**Specify the required structure and format of the final output.**

*   Use a clear schema (like JSON Schema, XML, or Markdown structure).
*   Define fields, data types, and expected content for each part of the output.
*   Example (JSON Schema):
    ```json
    {
      "title": "string",
      "introduction": "string",
      "core_explanation": "string",
      "code_examples": [
        {"language": "string", "code": "string"}
      ],
      "troubleshooting": {
        "common_errors": ["string"],
        "solutions": ["string"]
      }
    }
    ```

## [Optional] Examples

**Provide one or more examples of input-output pairs (few-shot learning).**

*   Include example `Expected Inputs` and the corresponding desired `Output Format` content.
*   If possible, illustrate the reasoning `Steps` taken to get from input to output.
