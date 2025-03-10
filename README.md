# NeuroPrompt

NeuroPrompt is the world's best open-source AI prompt generator, built using CrewAI. It generates highly effective, contextually rich, and structurally optimized prompts by integrating multiple prompt engineering frameworks, reinforcement learning, and adaptive context amplification.

## Features

- **Document-Driven Prompt Engineering**: Stores and utilizes prompt engineering frameworks and research
- **AI Optimization Pipeline**: Performs real-time analysis of user input using semantic parsing
- **Continuous Learning & Feedback**: Uses reinforcement learning to improve prompt quality
- **CrewAI Architecture**: Specialized agents work together for optimal results
- **Resource Efficient**: Designed to run locally on a laptop with minimal computational overhead

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/NeuroPrompt.git
cd NeuroPrompt
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the template:
```bash
cp .env.template .env
```

4. Add your OpenRouter API key to the `.env` file:
```
OPENROUTER_API_KEY=your-api-key-here
```

## Usage

Run the application:
```bash
python run.py "Your prompt request here"
```

Example:
```bash
python run.py "Create a prompt for a creative writing assistant that specializes in science fiction"
```

## Project Structure

```
NeuroPrompt/
│── agents/              # Specialized CrewAI agents
│── core/                # Core system functionality
│── data/                # Knowledge base and data storage
│── documents/           # Prompt engineering frameworks and research
│── logs/                # System logs
│── tests/               # Unit tests
│── .env                 # Environment variables
│── README.md            # Project documentation
│── requirements.txt     # Python dependencies
│── run.py               # Main entry point
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.