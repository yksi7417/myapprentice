# My Apprentice

# Installation 

```
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

## After installing new library via pip, please also run the followings to keep dependency up to date 
```
pip-chill > requirements.in
pip-compile requirements.in --output-file requirements.txt
```

# Run 

```
streamlit run src/home.py
```

# Download Models 

```
pip install huggingface-hub
huggingface-cli login      
huggingface-cli download google/gemma-3-4b-it-qat-q4_0-gguf  --local-dir ./models
```

# Problems 

## CUDA not being used:

### Hard Way, works, build it yourself using CMake:
```
​The error message you're encountering:​

CMake Error at CMakeDetermineCompilerId.cmake:491 (message):
  No CUDA toolset found.
indicates that while the CUDA Toolkit is installed, CMake cannot locate the necessary CUDA build customizations for Visual Studio. This is a common issue when integrating CUDA with Visual Studio on Windows.​

Solution:

You need to manually copy the CUDA Visual Studio integration files to the appropriate Visual Studio directory. Here's how:​

Locate the CUDA MSBuild Extensions:

Navigate to the following directory (adjust the version number if necessary):​

makefile

C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\extras\visual_studio_integration\MSBuildExtensions

Copy the Build Customization Files:

Copy all the .props and .targets files from the above directory.​
Nvda.Build.CudaTasks.v12.1.dll
CUDA 12.1.xml
CUDA 12.1.props
CUDA 12.1.targets

Paste into Visual Studio's BuildCustomizations Directory:

Determine your Visual Studio version and locate the corresponding BuildCustomizations directory. For Visual Studio 2019, it would typically be:​

C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Microsoft\VC\v160\BuildCustomizations
Paste the copied files into this directory.​

This process integrates the necessary CUDA build customizations into Visual Studio, allowing CMake to detect and utilize the CUDA toolset during the build process. This solution has been discussed and validated in the llama-cpp-python GitHub repository.​

Additional Tips:

Verify CUDA Installation:

Ensure that the CUDA Toolkit is correctly installed and that the nvcc compiler is accessible via the command line. You can check this by running:​

nvcc --version
Set Environment Variables:

Before building llama-cpp-python, set the necessary environment variables to enable CUDA support:​

set CMAKE_ARGS=-DLLAMA_CUBLAS=on
set FORCE_CMAKE=1
Reinstall llama-cpp-python:

After setting the environment variables, reinstall the package to ensure it builds with CUDA support:​

pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir
By following these steps, you should be able to resolve the "No CUDA toolset found" error and enable GPU support for your llama-cpp-python project on Windows.

it end up telling me it's version 11.8 though.
025-04-19 22:18:55,684 - root - INFO - CUDA? True,version:11.8
Why? 

```

### Use llama_cpp.server , see if it's using CUDA or not 

```
python -m llama_cpp.server --model models\mistral-7b-instruct-v0.3.Q4_K_M.gguf --n_gpu_layers -1
```