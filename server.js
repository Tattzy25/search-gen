import { Groq } from 'groq-sdk';
import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

// Load system prompt from file
const systemPrompt = fs.readFileSync(path.join(__dirname, 'system-prompt.txt'), 'utf-8');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY
});

app.post('/api/generate-searchbar', async (req, res) => {
  try {
    const { description } = req.body;

    if (!description) {
      return res.status(400).json({ error: 'Description is required' });
    }

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: "system",
          content: systemPrompt
        },
        {
          role: "user",
          content: `Create a search bar widget with the following description: ${description}`
        }
      ],
      model: "openai/gpt-oss-120b",
      temperature: 1,
      max_completion_tokens: 65536,
      top_p: 1,
      stream: true,
      reasoning_effort: "medium",
      stop: null,
      tools: [
        {
          type: "browser_search"
        },
        {
          type: "code_interpreter"
        },
        {
          type: "mcp",
          "server_label": "Tavily",
          "server_url": "https://mcp.tavily.com/mcp/?tavilyApiKey=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",
          "headers": {}
        }
      ]
    });

    for await (const chunk of chatCompletion) {
      const content = chunk.choices[0]?.delta?.content || '';
      if (content) {
        res.write(`data: ${JSON.stringify({ content })}\n\n`);
      }
    }

    res.write('data: [DONE]\n\n');
    res.end();

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Failed to generate searchbar' });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
  console.log(`Open http://localhost:${PORT}/index.html in your browser`);
});
