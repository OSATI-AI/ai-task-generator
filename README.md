# Task Generation Experiment
This reposity contains experiments with AI-supported task generation by the Open and Scalable AI Tutoring Initiative (OSATI). A demo version is deployed at [here](https://osati-tasks.fly.dev).

### Usage
The interace is implemented in NiceGUI. To experiment with the task generator, clone the repository and run

```bash
python main.py
```

and don't forget to set the respective API keys as environmental variables (see below).

### Deployment

The repo is ready for direct deployment at [fly.io](https://fly.io) following the suggestions from [NiceGUI](https://github.com/zauberzeug/nicegui/wiki/fly.io-Deployment). In short, deploy as follows:

1. Install flyctl, the command line interface (CLI) to administer your fly.io deployment.
2. Create an account with the terminal command `fly auth signup` or login with `fly auth login`.
3. Run `fly launch` from inside your project source directory. It will ask for a unique app name and some other information to create, configure, and deploy your new application.
4. To work properly, you need to set the required API keys as secrets
```bash
  fly secrets set GROQ_API_KEY={your_groq_API_key}
  fly secrets set OPENROUTER_API_KEY={your_openrouter_API_key}
```
5. Run `fly deploy` from inside your project source directory.
