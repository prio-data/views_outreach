from codebook_generator__json_to_md import markdown_content, codebook_path

def markdown_to_latex(markdown_content):
    """
    Convert Markdown content to LaTeX format.

    Args:
        markdown_content (str): The Markdown content to be converted to LaTeX format.

    Returns:
        latex_content (str): LaTeX content generated from the Markdown content.

    Note:
        The function replaces the Markdown syntax with LaTeX syntax.
        Specifically, 
        - '**' is replaced with '\textbf{' and '}'. 
        - '*' is replaced with '\textit{' and '}'.
        - '`' is replaced with '\texttt{' and '}'.
        - '~~' is replaced with '\sout{' and '}'.
        - '```' is replaced with '\begin{verbatim}' and '\end{verbatim}'.

    Minimal Example:
    ```python
    markdown_content = "This is a **bold** text."
    latex_content = markdown_to_latex(markdown_content)
    print(latex_content)
    ```

    """
    latex_content = markdown_content.replace("**", "\\textbf{").replace("**", "}").replace("*", "\\textit{").replace("*", "}").replace("`", "\\texttt{").replace("`", "}").replace("~~", "\\sout{").replace("~~", "}").replace("```", "\\begin{verbatim}").replace("```", "\\end{verbatim}")
    return latex_content

def save_latex_content(latex_content, codebook_path):
    """
    Save the LaTeX content to a file in codebook path

    Parameters:
        latex_content (str): The LaTeX content to be saved to a file.
    """
    with open(codebook_path, "w") as file:
        file.write(latex_content)

if __name__ == "__main__":
    markdown_content = markdown_content
    latex_content = markdown_to_latex()
    save_latex_content(latex_content, codebook_path)

    