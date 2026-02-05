# vLLM Service Dockerfile
FROM vllm/vllm-openai:latest

# Set environment variables
ENV VLLM_HOST=0.0.0.0
ENV VLLM_PORT=8000

# Expose port
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["--host", "0.0.0.0", "--port", "8000"]
