import os
import nbformat
from nbconvert import PythonExporter

def convert_notebooks_in_folder(folder_path):
  # Create output folder
  output_folder = os.path.join(folder_path, "converted_py")
  os.makedirs(output_folder, exist_ok=True)
  
  # Loop through all .ipynb files
  for filename in os.listdir(folder_path):
    if filename.endswith(".ipynb"):
      notebook_path = os.path.join(folder_path, filename)
      print(f"Converting: {notebook_path}")
      
      # Load notebook
      with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
      
      # Convert to Python script
      exporter = PythonExporter()
      script_body, _ = exporter.from_notebook_node(notebook)
      
      # Save .py file
      py_filename = filename.replace(".ipynb", ".py")
      py_path = os.path.join(output_folder, py_filename)
      with open(py_path, 'w', encoding='utf-8') as f:
        f.write(script_body)
      
      print(f"Saved to: {py_path}")
            
if __name__ == "__main__":
  # Change this to your target folder
  target_folder = "/path/to/your/notebooks"
  convert_notebooks_in_folder(target_folder)

