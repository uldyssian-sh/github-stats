#!/usr/bin/env python3
"""Basic tests for GitHub Stats modules."""

def test_imports():
    """Test that modules can be imported."""
    try:
        import github_stats
        import generate_images
        return True
    except ImportError:
        return False

def test_syntax():
    """Test Python syntax is valid."""
    import py_compile
    try:
        py_compile.compile('github_stats.py', doraise=True)
        py_compile.compile('generate_images.py', doraise=True)
        return True
    except py_compile.PyCompileError:
        return False

if __name__ == "__main__":
    print("Running basic tests...")
    
    if test_syntax():
        print("✅ Syntax test passed")
    else:
        print("❌ Syntax test failed")
    
    print("✅ Basic tests completed")