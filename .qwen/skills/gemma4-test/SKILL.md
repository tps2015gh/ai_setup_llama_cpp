# SKILL: gemma4-test

## Description
Test and verify Gemma 4 E2B model functionality with llama.cpp.

## Model Info

### Specifications
- **Model:** Gemma 4 E2B (Expert 2B)
- **Quantization:** Q4_K_M
- **File:** `google_gemma-4-E2B-it-Q4_K_M.gguf`
- **Size:** 3.46GB
- **Location:** `llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf`

### System Requirements
- **Minimum RAM:** 8GB
- **Disk Space:** ~4GB free
- **CPU:** x64 with AVX support

## Test Procedures

### 1. Basic Load Test
```bash
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -p "Hello" -n 50
```

### 2. Chat Mode Test
```bash
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -p "You are a helpful assistant."
```

### 3. Low-RAM Test (8GB systems)
```bash
llama-cpp\llama-cli.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf -cnv -c 2048 -p "Test"
```

### 4. Benchmark
```bash
llama-cpp\llama-bench.exe -m llama-cpp\models\google_gemma-4-E2B-it-Q4_K_M.gguf
```

## Expected Behavior
- Model loads within 10-30 seconds
- First token generated within 5-15 seconds (CPU)
- Token speed: 5-15 tokens/sec (depends on CPU)

## Common Issues

### Issue: Out of Memory
**Solution:** Reduce context size: `-c 1024`

### Issue: Slow Response
**Solution:** 
- Close other applications
- Reduce context: `-c 2048`
- Set threads: `-t 4` (or your CPU core count)

### Issue: Gibberish Output
**Solution:** Model may be corrupted, verify file size is ~3.46GB

## Prompt Templates
Gemma 4 uses chat template:
```
<start_of_turn>user
Your question<end_of_turn>
<start_of_turn>model
```

## Verification Checklist
- [ ] Model file exists and is 3.46GB
- [ ] Basic load test completes
- [ ] Chat mode responds coherently
- [ ] Memory usage stays under 6GB
