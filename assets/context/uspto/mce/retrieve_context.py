def retrieval_function(question: str) -> str:
    """Simple retrieval - returns all context concatenated."""
    from pathlib import Path
    context_dir = Path(__file__).parent / "context"
    all_context = []
    for file in sorted(context_dir.rglob("*.md")):
        all_context.append(file.read_text())
    return "\n\n".join(all_context) if all_context else ""
