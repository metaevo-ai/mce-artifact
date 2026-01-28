"""Validation script for base agent implementation."""
import ast
import inspect
import sys
from pathlib import Path


def validate_retrieval_function(working_dir: Path):
    """Validate retrieve_context.py has correct function signature."""
    script_path = working_dir / "retrieve_context.py"
    
    if not script_path.exists():
        print("❌ File not found: retrieve_context.py")
        return False
    
    try:
        with open(script_path, 'r') as f:
            content = f.read()
        tree = ast.parse(content)
    except Exception as e:
        print(f"❌ Error parsing file: {e}")
        return False
    
    # Find retrieval_function
    func_node = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "retrieval_function":
            func_node = node
            break
    
    if not func_node:
        print("❌ Function 'retrieval_function' not found")
        return False
    
    # Check signature
    args = func_node.args
    if len(args.args) != 1 or args.args[0].arg != "question":
        print("❌ Function signature incorrect. Expected: def retrieval_function(question: str) -> str:")
        return False
    
    if not any(isinstance(n, ast.Return) for n in ast.walk(func_node)):
        print("❌ Function has no return statement")
        return False
    
    # Test import and execution
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("retrieve_context", script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules['retrieve_context'] = module
        spec.loader.exec_module(module)
        
        func = getattr(module, 'retrieval_function')
        result = func("What is the debt amount?")
        
        if not isinstance(result, str):
            print(f"❌ Function should return string, got {type(result).__name__}")
            return False
        
        if not result:
            print("❌ Function returned empty string")
            return False
        
        del sys.modules['retrieve_context']
        print(f"✅ Retrieval function validated ({len(result)} chars returned)")
        return True
        
    except Exception as e:
        print(f"❌ Error testing function: {e}")
        return False


def validate_context_files(working_dir: Path):
    """Validate context/ directory has markdown files."""
    context_dir = working_dir / "context"
    
    if not context_dir.exists():
        print("❌ Context directory not found")
        return False
    
    if not context_dir.is_dir():
        print("❌ 'context' is not a directory")
        return False
    
    md_files = list(context_dir.glob("*.md"))
    
    if not md_files:
        print("❌ No markdown files found in context/")
        return False
    
    empty_files = [f.name for f in md_files if f.stat().st_size == 0]
    if empty_files:
        print(f"❌ Empty files: {', '.join(empty_files)}")
        return False
    
    print(f"✅ Found {len(md_files)} markdown file(s) with content")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run python utils/validate_base.py <iter_dir>")
        sys.exit(1)
    
    working_dir = Path(sys.argv[1])
    
    print("\n=== Base Agent Implementation Validation ===\n")
    
    valid_func = validate_retrieval_function(working_dir)
    valid_context = validate_context_files(working_dir)
    
    if valid_func and valid_context:
        print("\n✅ All validations passed!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed")
        sys.exit(1)

