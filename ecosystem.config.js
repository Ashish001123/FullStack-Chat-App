module.exports = {
  apps: [
    {
      name: "backend",
      script: "src/index.js",
      cwd: "./backend",
    },
    {
      name: "ai-service",
      script: "uvicorn",
      args: "main:app --host 0.0.0.0 --port 8000",
      cwd: "./ai-agent",
      interpreter: "none"
    },
    {
      name: "frontend",
      script: "npm",
      args: "run dev",
      cwd: "./frontend",
    }
  ]
}