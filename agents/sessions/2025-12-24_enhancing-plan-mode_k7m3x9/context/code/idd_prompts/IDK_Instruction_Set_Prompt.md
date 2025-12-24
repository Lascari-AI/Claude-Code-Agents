# IDK Instruction Set Prompt
- I recently completed a course on AI coding and I'm trying to expand a concept I learned in the course
- The course was about using AI to write code
- The course introduced the concept of using Information Dense Keywords (IDKs) when writing prompts

# The Idea of IDKs (Information Dense Keywords)
- Words that have a clear, concise, and direct meaning to them in regards to the task at hand (in our case, writing code)
- Use the most valuable information rich words that best communicates what you want done to your AI coding assistant.
    - Prompts are made up of individual keywords
    - Some of these keywords contain more information than others (more meaning, more action)
- Using IDKs has shown to create more accurate and effective prompts.
    - This meaning is that the AI is more likely to understand the task at hand and write code that is more accurate
    - We measure accuracy here by passing tests and not needing to make changes to the code
- Therefore using IDKs means the code will be correct the first time.

# How I Would Like to Expand on This
- I would like to make this list of IDKs to operate almost as an instruction set for my AI coding assistant
## Thought Process
- In traditional programming, an instruction set is a suite of low-level operations the CPU can perform directly (e.g., ADD, JMP, INC). 
- For AI coding, our “CPU” is the large language model (LLM), which responds to natural language. 
- By consistently using Information Dense Keywords (IDKs), we reduce ambiguity and convey maximum meaning per word or phrase—like specialized opcodes telling the AI “this is exactly what I need you to do.” 
- This harnesses the AI’s pattern-recognition capabilities to produce more accurate code on the first try.
- I would like to build out this idea so that I have an exhaustive list of IDKs that I can use to write prompts for my AI coding assistant

# My Current List of IDKs
## CRUD
### CREATE
    - Initializes a brand-new entity (file, function, class, var, etc.). Tells the AI "make something new."

### UPDATE
    - Modifies an existing entity. Tells the AI "edit or enhance what's already there."

### DELETE
    - Removes or eliminates an existing entity. Tells the AI "completely remove this."

## Actions
### ADD
- Attaches or supplements an existing entity with new content. Tells the AI "append, attach, or expand."

### REMOVE
- Opposite of ADD—take something out from an existing entity.

### MOVE
- Relocates code/entities from one place to another. Tells the AI "cut-paste from Location A to Location B."

### REPLACE
- Substitutes one piece of content for another. Tells the AI "swap the old content for the new."

### SAVE
- Instructs the AI to persist or finalize the code changes somewhere (less common in day-to-day prompts—useful when clarifying final output or storing a code snippet in a separate location).

### MIRROR
- Tells the AI to replicate or copy the logic/pattern from an existing place and re-use it. This is a powerful concept in code (e.g., "mirror create_bar_chart but for create_line_chart").

### MAKE
- A somewhat more commanding version of "update" or "create." Often used with a direct imperative (e.g., "MAKE top quartile green, bottom red, rest blue" in a chart) to unify creation + transformation.

### USE
- Tells the AI to rely on or incorporate external code snippets/doc references as a guide. E.g., "USE snippet X as reference; replicate that pattern."

### APPEND
- Similar to ADD but more specific: Tells the AI to add something "to the end" or "attach in a final position." Minimizes confusion about location.

## Coding/Language Specific
### VAR
- Refers to a variable. Tells the AI "this is a named variable you need to manipulate."

### FUNCTION
- Explicitly denotes a function definition (def block).

### CLASS 
- Denotes a class definition.

### TYPE
- Denotes a type definition (e.g., a Pydantic model, a TypeScript interface).

### FILE
- Denotes an entire file. Often used with CREATE file.py, UPDATE file.py.

### DEFAULT
- Ties a value or parameter to a default. E.g., "DEFAULT 10." This is more specific than just "=10."

## Location
### BEFORE
- Tells the AI to insert or adjust code ahead of something else. E.g., "Insert logic before line 20."

### AFTER
- Tells the AI to insert or adjust code after a specific block or line.


# Current State
- I have a list of these IDKs but I do believe I am missing both some sections and some IDKs

# End Goal State
- I want to have a comprehensive list of IDKs that I can use to write prompts for my AI coding assistant

# What to Do
- Create a more detailed understand of IDKs function and the thought process behind them
- Create any missing sections that I am missing
- Create any missing IDKs that I am missing

# Key Considerations
- IDKs should be almost self explanatory in their meaning
    - I.E. I should know what it means and what it does without needing to be explicitly briefed on what it is
        - E.X. "CREATE" is very clearly means to make something new

# Output Format
## IDK Type
- This is a section that designates what type of IDK it is

# Attached Context
- Transcripts from lessons of the course for reference and deeper understanding of IDKs
- Spec prompts that contain examples of IDKs being used within the low level prompts section
    - Spec prompts explain what needs to get done, then contain "Low Level Prompt" which are commands for the AI to follow
    - Each low level prompt uses IDKs to tell the AI what to do
- Notes I have taken from the course for reference