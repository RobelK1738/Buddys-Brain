# Buddy's Brain

Buddy's Brain is an intelligent, AI-powered educational assistant designed to help students quickly and effectively find relevant educational resources. It leverages advanced vector-based semantic search and OpenAI's GPT models to provide clear, concise summaries and explanations. Buddy's Brain also supports voice interactions through text-to-speech (TTS) and speech-to-text (STT), allowing users to engage naturally with the assistant. Users can interact through a friendly React-based frontend, currently deployed at:

[buddys-brain-alpha.vercel.app](https://buddys-brain-alpha.vercel.app/)

## Features

- **Semantic Vector Search**: Quickly retrieves educational resources relevant to the student's query.
- **AI-Generated Summaries**: Uses GPT-4o to provide concise, clear, five-sentence summaries or explanations.
- **Fallback Summaries**: Provides brief, AI-generated summaries from internet knowledge when internal resources aren't available.
- **Voice Interaction**: Supports natural voice-based interactions using TTS and STT technologies.
- **Media Uploads**: Allows users to upload different media types such as images, videos, links, and documents to assist future students.

## Tech Stack

- **Frontend**: React
- **Backend**: FastAPI, MongoDB (with vector search capabilities)
- **AI Model**: OpenAI GPT-4o
- **Deployment**: Deployed via Vercel (frontend) and Railway (backend), Docker-friendly and cloud-compatible

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB with vector search indexes
- OpenAI API key

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/buddys-brain.git
cd buddys-brain
pip install -r requirements.txt
cd app/utils/summarization 
```

Create a `.env` file and add your OpenAI API key :

```
OPENAI_API_KEY=your_openai_api_key
```

### Starting the Server

Run the provided bash script to start the FastAPI server locally:

```bash
cd ../../../
./runApp.sh
```

## API Endpoint

**POST** `/search`

**Request Example:**

```json
{
  "query": "Explain the concept of limits in calculus"
}
```

**Response Example:**

```json
{
  "summary": "A limit in calculus describes the value a function approaches as its input approaches some point. Limits form the foundational basis for defining continuity, derivatives, and integrals. They help mathematicians understand function behavior near specific points, even if the function isn't explicitly defined there. Limits are essential in evaluating instantaneous rates of change and the area under curves. Understanding limits is crucial for applications in physics, engineering, economics, and many other fields.",
  "results": [
    {
      "title": "Limits and Continuity",
      "summary": "Detailed explanation of calculus concepts like limits and continuity.",
      "media_link": "https://example.com/limits",
      "media_type": "video",
      "course": "CALC101",
      "score": 0.93
    }
  ]
}
```

## Contributing

Contributions are welcome! Please submit pull requests or open issues for improvements.

## Contributors

This project was developed during the Bison Bytes 2025 hackathon hosted at Howard University by:

- [Robel Kebede](https://github.com/RobelK1738)
- [Abdulmujeeb Lawal](https://github.com/lawal-mj)
- [Valentine Ezikeoha](https://github.com/HuVddme)
- [Kyle Nwosu](https://github.com/KyleNwosu)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
