const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const app = express();
const cors = require('cors');
const port = 3000;

app.use(cors());

// Middleware
app.use(bodyParser.json());

// Route to handle code execution
app.post('/run-code', (req, res) => {
  const { language, code } = req.body;

  let command = '';
  let fileExtension = '';
  let fileName = '';

  // Determine the correct compiler based on the language
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
    case 'clike':
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

  // Write the code to a file and execute it
  const fs = require('fs');
  fs.writeFileSync(fileName, code);

  // Execute the command
  exec(command, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).send({ error: stderr });
    }
    res.send({ output: stdout });
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
