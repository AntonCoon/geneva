## Assignment: Gene-Disease Analysis Service
### Overview
Build a web application that analyzes potential correlations between genes and diseases using public life sciences data and LLM capabilities. The service should accept gene and disease names as input, retrieve relevant scientific data, use an LLM to analyze the correlation, and return both immediate results and stored analysis history.
### Core Requirements
#### 1. Frontend Interface
Implement a simple web interface that:
- Allows users to input their username and LLM API key (OpenAI or Anthropic)
- Provides a form to submit gene and disease names for analysis
- Displays analysis results in real-time
- Shows a history of previous analyses for the user
- The frontend should be functional and user-friendly (design aesthetics are not the focus)
#### 2. Backend API
Design and implement a RESTful API that:
- Handles user sessions and API key management
- Processes gene-disease analysis requests
- Stores and retrieves analysis history
- You have full freedom to design the API structure as you see fit
#### 3. Data Integration
- Integrate with at least one public life sciences API (e.g. OpenTargets)
- Retrieve relevant gene and disease information via relevant endpoints
- No authentication should be required for the data source you choose
#### 4. LLM Integration
- Support any or both: OpenAI and Anthropic APIs
- Implement proper prompt engineering to analyze gene-disease correlations
- Handle rate limiting and API errors gracefully
#### 5. Concurrency
- The service must handle multiple concurrent requests efficiently
#### 6. Data Persistence
- Store all analyses in a database (SQLite is sufficient)
- Include any relevant data
#### 7. Docker Configuration
- Provide a docker-compose.yml that runs the entire application
- Application should be fully functional after running `docker-compose up`
### Technical Expectations
#### Documentation
- README with clear setup and running instructions
- Document any design decisions or trade-offs
#### Development Practices
- Use virtual environment (venv, poetry, or similar)
- Include requirements.txt or pyproject.toml
- Provide clear git commit history showing your development process
#### Running the Application
Your application should be runnable with a single command: bash docker-compose up After running this command, the application should be fully accessible at http://localhost (or another port of your choice).
### Bonus Points (Optional)
- If you want to go above and beyond think of missing functinality and go for it
### Submission Guidelines
1. Create a GitHub repository with your solution
2. Include all required artefacts there
3. Make sure the git history shows your development process
4. Send us the repository link when complete
### Time Expectation
This assignment is designed to take 6-8 hours to complete with the help of AI coding assistants. You're encouraged to use LLMs to help write code, but ensure you understand and can explain every part of your solution.
### Notes
- You may use any frameworks
- Choose libraries that demonstrate your understanding of the Python ecosystem
- Focus on demonstrating senior-level decision-making and implementation skills
- Remember: we value quality over quantity - a well-implemented core solution is better than a
feature-rich but poorly structured application
### Example User Scenarios
Login
1. User enters their username and OpenAI/Anthropic API key Search
2. User submits a gene name (e.g., "TP53") and disease name (e.g., "lung cancer")
3. System retrieves relevant data from scientific databases
4. System uses LLM to analyze the correlation
5. Results are displayed to the user with correlation score and analysis
Overview
6. User can view their history of previous analyses
Good luck! We look forward to discussing your implementation choices during the technical interview.
