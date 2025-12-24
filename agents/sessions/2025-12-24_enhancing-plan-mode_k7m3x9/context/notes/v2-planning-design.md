# **1. Introduction**

This document outlines the comprehensive workflow for transforming a user's request and associated file context into a structured `FullRequestSpecification`. 

The goal is to create a detailed, actionable plan that an AI coding assistant (or a human developer) can use to implement the requested feature or changes. 

This process emphasizes:

- Hierarchical breakdown
- Sequential checkpoint progression
- Opportunities for parallel task execution by structure checkpoints into groups of non block task tranches
- Rich contextual information at each stage.

# **2. Key Principles Guiding the Workflow**

- **Hierarchical Decomposition:** The overall request is broken down into sequential checkpoints, which are further broken down into task tranches, and finally into low-level tasks.
- **Sequential Checkpoints:** Major milestones are ordered and must be completed sequentially.
- **Checkpoint Execution Specification:** Each checkpoint has its own "mini-spec" detailing how to achieve its specific goal.
- **Parallelism:**
    - Initial analysis of all provided files can be done in parallel.
    - Analysis of how each initial file relates to a specific checkpoint's goal can be done in parallel.
    - Low-level tasks *within a single task tranche* are designed for parallel execution where dependencies allow.
- **Context-Rich Planning:** File context (initial state, relevance, and changes per checkpoint) is tracked and utilized throughout.
- **Actionable Low-Level Tasks:** The most granular tasks are concrete `aider`style commands with explicit dependencies.

# **3. Inputs to the Workflow**

- **User's Primary Request:**
    - The high-level description of what needs to be achieved.
- **List of Relevant Files:**
    - Paths to files in the existing codebase that are deemed relevant to the request by the user
    - The content of these relevant files.
- **File Tree Structure:**
    - Provides broader context of the project structure.
- **General Rules/Constraints (Optional):**
    - Any overarching guidelines / rules files

# **4. Output of the Workflow**

A single, structured `FullRequestSpecification` object (conforming to the Pydantic model defined previously).

# **5. Workflow Phases and Steps**

## **Phase 0: Initialization and Initial File Analysis**

- **Goal:** To process initial inputs and perform a preliminary analysis of all relevant files.
- **Inputs:** User's Primary Request, List of Relevant File Paths, Initial File Contents, File Tree Structure, General Rules/Constraints.
- **Steps:**
    1. **System Ingestion:** Load all provided inputs.
    2. **Preliminary Request Understanding:** The system (or an AI component) forms a basic understanding of the user's primary request to guide the initial file analysis.
    3. **Parallel Initial File Analysis (for each relevant input file):**
        - **Action:** For each file provided:
            - Generate `overall_relevance_to_request_objective`: A description of how this file, in its current state, broadly relates to the preliminary understanding of the overall request.
            - Generate `initial_content_summary_purpose`: A brief summary of the file's current content, key components, or primary purpose.
        - **Output per file:** An `InitialFileAnalysisItem` object.
- **Outputs of Phase 0:**
    - A list of `InitialFileAnalysisItem` objects.
    - Internal representation of the preliminary request understanding.
    - Internal representation of general rules/constraints.

## **Phase 1: Defining the Overall Request Objective**

- **Goal:** To articulate a clear, concise high-level objective for the entire request.
- **Inputs:** User's Primary Request, Preliminary Request Understanding (from Phase 0).
- **Steps:**
    1. **System/AI Refinement:** Based on the user's input and preliminary understanding, formulate a single, clear `overall_request_objective`. This might involve an AI generating a candidate objective and potentially seeking user confirmation if ambiguity is high.
- **Outputs of Phase 1:**
    - The `overall_request_objective` string.

## **Phase 2: Defining Sequential Request Checkpoints**

- **Goal:** To break down the `overall_request_objective` into major, ordered, and logical milestones (checkpoints).
- **Inputs:** `overall_request_objective`.
- **Steps:**
    1. **System/AI Decomposition:** Analyze the `overall_request_objective` and identify distinct, sequential stages or sub-goals that build upon each other.
    2. **For each identified stage, define a `RequestCheckpoint` (shell):**
        - `order`: Sequential number (1, 2, 3...).
        - `title`: A concise, descriptive title for the checkpoint.
        - `goal_for_request_checkpoint`: A clear statement of what this specific checkpoint aims to achieve.
        - `prerequisites`: List titles or orders of preceding `RequestCheckpoint`(s) that must be completed first (empty for the first checkpoint).
        - `expected_outcome`: A brief description of the tangible deliverables or state of the system/codebase after this checkpoint is successfully completed.
- **Outputs of Phase 2:**
    - A list of `RequestCheckpoint` objects (these are shells, their detailed `execution_spec` and file contexts will be populated in Phase 3).

## **Phase 3: Detailed Planning for Each Request Checkpoint (Iterative)**

- **Goal:** For each `RequestCheckpoint` defined in Phase 2, develop its detailed execution plan, including file context, specific relevance, and granular tasks. This phase is performed iteratively for each checkpoint in its defined order.
- **Inputs (for each iteration, i.e., for one `RequestCheckpoint`):**
    - The current `RequestCheckpoint` (shell from Phase 2).
    - The full list of `InitialFileAnalysisItem` objects (from Phase 0).
    - The `ending_files_for_request_checkpoint` from the *previous* `RequestCheckpoint` (if this is not the first checkpoint).
    - The `overall_request_objective`.
- **Steps (repeated for each `RequestCheckpoint`):**
    1. **Sub-Phase 3.1: Determine Request Checkpoint-Specific File Context:**
        - **Action (Beginning Files):**
            - If it's the first checkpoint: Identify which of the `InitialFileAnalysisItem.file_path`s are relevant to *starting* this checkpoint. Mark their status (e.g., "Existing, to be modified," "Existing, read-only").
            - If it's a subsequent checkpoint: Start with the `ending_files_for_request_checkpoint` from the previous checkpoint. These become the `beginning_files_for_request_checkpoint` for the current one.
        - **Output (Beginning Files):** Populated `request_checkpoint_specific_file_context.beginning_files_for_request_checkpoint`.
        - **Action (Ending Files - Projection):** Based on the `goal_for_request_checkpoint` and the tasks that *will be planned* in Sub-Phase 3.3, project the state of files after this checkpoint. This is an anticipatory step and might be refined as tasks are detailed. Indicate status (e.g., "Modified," "New," "Deleted," "Unchanged").
        - **Output (Ending Files):** Populated `request_checkpoint_specific_file_context.ending_files_for_request_checkpoint`.
    2. **Sub-Phase 3.2: Request Checkpoint-Specific File Relevance Analysis (Parallel):**
        - **Action:** For each file listed in the `InitialFileAnalysisItem` list (from Phase 0):
            - Analyze and describe its specific relevance (`relevance_to_request_checkpoint_goal`) to the `goal_for_request_checkpoint` of the *current* checkpoint. This helps understand which of the original files are key players in the current stage.
        - **Output:** Populated `request_checkpoint_specific_file_relevance_analysis` list for the current checkpoint.
    3. **Sub-Phase 3.3: Generate Request Checkpoint Execution Specification:**
        - **Action (Define Objective):** Set `execution_spec.objective` to be the same as `goal_for_request_checkpoint`.
        - **Action (Define Implementation Notes):** Compile any `implementation_notes_specific_to_checkpoint` relevant only to this checkpoint's execution.
        - **Action (Define Task Tranches):**
            - Break down the `execution_spec.objective` into logical, smaller work packages or `TaskTranche`s.
            - For each `TaskTranche`:
                - Assign a `tranche_id` (e.g., "1.1", "1.2").
                - Define its `goal`.
        - **Action (Define Low-Level Tasks within each Task Tranche):**
            - For each `TaskTranche`:
                - Further decompose its `goal` into a sequence of `LowLevelTask`s.
                - For each `LowLevelTask`:
                    - Assign a `task_id` (e.g., "1.1.1", "1.1.2").
                    - Write a clear `description`.
                    - Formulate the `action_details` (the `aider`style command).
                    - Identify `depends_on` (a list of `task_id`s *within the same tranche*) that must be completed before this task can start.
        - **Output:** The fully populated `execution_spec` for the current checkpoint.
        - *(Refinement)*: The definition of Low-Level Tasks here might lead to adjustments in the projected `ending_files_for_request_checkpoint` from Sub-Phase 3.1.
- **Outputs of Phase 3 (after iterating through all checkpoints):**
    - The list of `RequestCheckpoint` objects, now fully populated with their specific file contexts, relevance analyses, and execution specifications.

## **Phase 4: Consolidating General Notes and Overall Context Summary**

- **Goal:** To gather any general implementation notes that apply to the entire request and summarize the overall file context.
- **Inputs:** General Rules/Constraints (from Phase 0), `InitialFileAnalysisItem` list, `ending_files_for_request_checkpoint` from the *final* `RequestCheckpoint`.
- **Steps:**
    1. **Compile General Notes:** Aggregate any `general_request_implementation_notes` from the initial inputs or identified during planning that apply broadly across all checkpoints.
    2. **Summarize Overall Request Context:**
        - `Beginning Context (Start of Request)`: Can be derived from the list of `InitialFileAnalysisItem.file_path`s.
        - `Ending Context (After all Request Checkpoints)`: Can be derived from the `ending_files_for_request_checkpoint` of the final checkpoint.
- **Outputs of Phase 4:**
    - `general_request_implementation_notes` list.
    - `overall_request_context_summary` (structure to be defined, could be simple lists of file paths).

## **Phase 5: Final Assembly of Full Request Specification**

- **Goal:** To combine all generated components into the final `FullRequestSpecification` object.
- **Inputs:**
    - `InitialFileAnalysisItem` list (from Phase 0).
    - `overall_request_objective` (from Phase 1).
    - List of fully populated `RequestCheckpoint` objects (from Phase 3).
    - `general_request_implementation_notes` (from Phase 4).
    - `overall_request_context_summary` (from Phase 4 - if included directly in the model, otherwise it's for external reporting).
- **Steps:**
    1. **System Construction:** Assemble all the pieces into a single `FullRequestSpecification` Pydantic model instance.
- **Outputs of Phase 5:**
    - The final `FullRequestSpecification` object.

# **6. Assumptions**

- The system (potentially involving AI) is capable of understanding natural language requests and decomposing them into logical steps.
- The system can analyze code files (or their summaries) to determine relevance and purpose.
- The system can generate `aider`style commands based on task descriptions.
- The system can identify dependencies between low-level tasks.
- Access to file contents is available if detailed analysis or modification is part of the plan.

# **7. Conclusion**

This workflow provides a robust and detailed methodology for planning complex coding requests. By breaking the request into manageable, sequential checkpoints, and further detailing each checkpoint with parallelizable task tranches and context-aware file analysis, it aims to improve the accuracy, efficiency, and predictability of code generation and modification tasks. The resulting `FullRequestSpecification` serves as a comprehensive blueprint for execution.

---