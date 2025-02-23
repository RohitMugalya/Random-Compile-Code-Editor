const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');
const cors = require('cors');
const path = require('path');

const app = express();
const port = 3000;

app.use(cors());
app.use(bodyParser.json());

// Serve static files (like index.html) from the current directory
app.use(express.static(__dirname));

// Home Route - Serve `index.html`
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Route to execute user-submitted code
app.post('/run-code', (req, res) => {
  const { language, code } = req.body;
  
  if (!language || !code) {
    return res.status(400).send({ error: 'Language and code are required' });
  }

  let fileExtension = '';
  let fileName = '';
  let command = '';

  switch (language) {
    case 'python':
      fileExtension = 'py';
      fileName = 'script.py';
      command = `python3 ${fileName}`;
      break;
    case 'c':
      fileExtension = 'c';
      fileName = 'script.c';
      command = `gcc ${fileName} -o output && ./output`;
      break;
    case 'cpp':
      fileExtension = 'cpp';
      fileName = 'script.cpp';
      command = `g++ ${fileName} -o output && ./output`;
      break;
    case 'java':
      fileExtension = 'java';
      fileName = 'Script.java';
      command = `javac ${fileName} && java Script`;
      break;
    default:
      return res.status(400).send({ error: 'Unsupported language' });
  }

  fs.writeFile(fileName, code, (err) => {
    if (err) {
      return res.status(500).send({ error: 'Failed to write file' });
    }

    exec(command, (error, stdout, stderr) => {
      fs.unlinkSync(fileName);
      if (language === 'c' || language === 'cpp') fs.unlinkSync('output');
      if (language === 'java') fs.unlinkSync('Script.class');

      if (error) {
        return res.status(500).send({ error: stderr });
      }
      res.send({ output: stdout });
    });
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
