import inspect
import importlib
import os
from pathlib import Path


class Help:
    def __init__(self):
        self.cli_path = Path(__file__).parent
        self.commands = self._discover_commands()

    def _discover_commands(self):
        """Dynamically discover all CLI command modules and their methods"""
        commands = {}
        
        # Get all Python files in the CLI directory except __init__.py and help.py
        for file in self.cli_path.glob("*.py"):
            if file.name in ["__init__.py", "help.py"]:
                continue
            
            module_name = file.stem
            try:
                # Import the module dynamically
                module = importlib.import_module(f"tubearchivist_cli.cli.{module_name}")
                
                # Find the main class (should be capitalized version of module name)
                class_name = module_name.capitalize()
                if hasattr(module, class_name):
                    cls = getattr(module, class_name)
                    
                    # Get public methods (not starting with _)
                    methods = []
                    for method_name in dir(cls):
                        if not method_name.startswith('_') and callable(getattr(cls, method_name)):
                            method = getattr(cls, method_name)
                            # Only include methods with docstrings
                            description = self._get_method_description(method)
                            if description:  # Only add if we have a description
                                methods.append({
                                    'name': method_name,
                                    'description': description
                                })
                    
                    if methods:
                        # Get class docstring for command description
                        class_description = self._get_class_description(cls)
                        if class_description:  # Only add if we have a description
                            commands[module_name] = {
                                'description': class_description,
                                'methods': methods
                            }
            except ImportError:
                continue
        
        return commands

    def _get_class_description(self, cls):
        """Get class description from docstring only"""
        if cls.__doc__:
            return cls.__doc__.strip().split('\n')[0]
        return None

    def _get_method_description(self, method):
        """Get method description from docstring only"""
        if method.__doc__:
            return method.__doc__.strip().split('\n')[0]
        return None

    def show(self):
        """Display comprehensive help information"""
        print("TubeArchivist CLI - Available Commands:")
        print("=" * 50)
        
        if not self.commands:
            print("No documented commands found.")
            return
        
        for command_name, command_info in sorted(self.commands.items()):
            print(f"\n{command_name.upper()}:")
            print(f"  {command_info['description']}")
            
            for method in command_info['methods']:
                print(f"  {command_name} {method['name']:<12} - {method['description']}")
        
        print(f"\nUsage: python tube.py <command> <action>")
        print(f"Example: python tube.py config set")

    def show_command(self, command_name):
        """Display help for a specific command"""
        if command_name not in self.commands:
            print(f"Unknown command: {command_name}")
            print("Use 'help' to see all available commands.")
            return
        
        command_info = self.commands[command_name]
        print(f"{command_name.upper()} - {command_info['description']}")
        print("=" * 50)
        
        for method in command_info['methods']:
            print(f"  {command_name} {method['name']:<12} - {method['description']}")
        
        print(f"\nUsage: python tube.py {command_name} <action>")
        
        command_info = self.commands[command_name]
        print(f"{command_name.upper()} - {command_info['description']}")
        print("=" * 50)
        
        for method in command_info['methods']:
            print(f"  {command_name} {method['name']:<12} - {method['description']}")
        
        print(f"\nUsage: python tube.py {command_name} <action>")
