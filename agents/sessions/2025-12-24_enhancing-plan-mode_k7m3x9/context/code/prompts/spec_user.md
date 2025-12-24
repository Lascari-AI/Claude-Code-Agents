<user_prompt>
    <input_text>
        - As a Spec Prompt Engineer and Specification Document Strategist, please analyze the provided inputs and generate a comprehensive specification document.
        - Ensure you follow and complete all phases of the `<internal_workflow>` to produce the full specification.
        - Take all the time needed to generate the best possible specification document; there is no rush.
    </input_text>
    <app_purpose_input description="The core purpose of the app and other context like rules and such.">
        {app_purpose_content_placeholder}
    </app_purpose_input>
    <user_requests_input description="Any requests or instructions from the user that are relevant to the task.">
        {user_requests_content_placeholder}
    </user_requests_input>
    <relevant_files_input description="Files provided by the user that are relevant to the task. This could be a list of paths, or actual file content if small.">
        {relevant_files_content_placeholder}
    </relevant_files_input>
    <file_tree_input description="A tree structure of the files in the project. This provides context, including files not directly relevant.">
        {file_tree_content_placeholder}
    </file_tree_input>
    <final_thoughts>Take a deep breath, and please begin constructing the specification prompt based on these inputs.</final_thoughts>
</user_prompt>