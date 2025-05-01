#python -m llama_cpp.server --model models\Mistral-7B-Instruct-v0.3.Q4_K_M.gguf --n_gpu_layers -1
# to split the model across multiple GPUs, set the environment variable CUDA_VISIBLE_DEVICES to the GPU IDs you want to use, separated by commas. For example, to use GPUs 0 and 1, set it like this
$Env:CUDA_VISIBLE_DEVICES="0,1"
python -m llama_cpp.server --model .\models\DeepSeek-R1-Distill-Qwen-14B-Q8_0.gguf --n_gpu_layers -1 --tensor_split 2 1
Pause
