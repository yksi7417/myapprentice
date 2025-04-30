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

After I install a new GPU card (now I have RTX 2060 SUPER + RTX3060 , i need to recompile again)

$env:FORCE_CMAKE = "1"
$env:CMAKE_ARGS  = "-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=75;86"
$env:CUDACXX      = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.1\bin\nvcc.exe"

pip install llama-cpp-python[server] --upgrade --force-reinstall --no-cache-dir

Mon Apr 28 20:42:49 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.94                 Driver Version: 560.94         CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3060      WDDM  |   00000000:05:00.0 Off |                  N/A |
|  0%   34C    P8              8W /  170W |       0MiB /  12288MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   1  NVIDIA GeForce RTX 2060 ...  WDDM  |   00000000:06:00.0  On |                  N/A |
| 55%   44C    P8             11W /  175W |     814MiB /   8192MiB |     10%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
```

### Use llama_cpp.server , see if it's using CUDA or not 

```
$Env:CUDA_VISIBLE_DEVICES="0,1"; python -m llama_cpp.server --model models\Mistral-7B-Instruct-v0.3.Q4_K_M.gguf --n_gpu_layers -1 --tensor_split 1 1
```

### to test if Server is giving you correct response

```
curl -X POST http://localhost:8000/v1/chat/completions -H "Content-Type: application/json" -d "{\"model\": \"local-llama\", \"messages\": [{\"role\": \"user\", \"content\": \"Tell me a joke about cats.\"}], \"temperature\": 0.7}"
```

### CrewAI showing error:   

```
    from litellm.types.utils import ChatCompletionDeltaToolCall
ModuleNotFoundError: No module named 'litellm.types.utils'
```

Solution:  hack the file under D:\conda\envs\speech_env\Lib\site-packages\litellm\utils.py
change the block from

```
try:
    # Python 3.9+
    with resources.files("litellm.litellm_core_utils.tokenizers").joinpath(
        "anthropic_tokenizer.json"
    ).open("r") as f:
        json_data = json.load(f)
except (ImportError, AttributeError, TypeError):
    with resources.open_text(
        "litellm.litellm_core_utils.tokenizers", "anthropic_tokenizer.json"
    ) as f:
        json_data = json.load(f)
```

to 

```
try:
    # Python 3.9+
    with resources.files("litellm.litellm_core_utils.tokenizers").joinpath(
        "anthropic_tokenizer.json"
    ).open("r", encoding="utf-8") as f:  ## Hardcode encoding to utf-8 for Windows
        json_data = json.load(f)
except (ImportError, AttributeError, TypeError):
    with resources.open_text(
        "litellm.litellm_core_utils.tokenizers", "anthropic_tokenizer.json"
    ) as f:
        json_data = json.load(f)
```


### Ollama - end up not using because it cannot split models like llama.cpp 

it is possible to create your own model file 

```
# Modelfile
FROM ./DeepSeek-R1-Distill-Qwen-14B-Q4_K_M.gguf

PARAMETER temperature 0.7
PARAMETER top_p 0.95
PARAMETER stop "<|endoftext|>"
```

```
PS D:\dvlp\myapprentice\models> ollama create deepseek-qwen-14b-q4km -f Modelfile
gathering model components
copying file sha256:67a7933cf2ad596a393c8e13b30bc4da2d50b283e250b78554aed18817eca31c 100%
parsing GGUF
using existing layer sha256:67a7933cf2ad596a393c8e13b30bc4da2d50b283e250b78554aed18817eca31c
creating new layer sha256:0439aa4ff272f2884b931c3e0f88b55d1dab33b35742ebbc407541802b389be9
writing manifest
success
PS D:\dvlp\myapprentice\models> ollama list
NAME                             ID              SIZE      MODIFIED
deepseek-qwen-14b-q4km:latest    8f5bae63627a    9.0 GB    13 seconds ago
```
