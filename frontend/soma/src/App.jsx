import { useState } from 'react';

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleFileChange = (event) => {
    setPdfFile(event.target.files[0]);
  };

  const handleQuestionChange = (event) => {
    setQuestion(event.target.value);
  };

  const handleProcessPdf = async () => {
    const formData = new FormData();
    formData.append('pdf', pdfFile);
    formData.append('question', question);

    try {
      const response = await fetch('/api/process_pdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setResponse(result.response);
      } else {
        console.error('Error processing PDF:', response.statusText);
      }
    } catch (error) {
      console.error('Error processing PDF:', error);
    }
  };

  return (
    <div>
      <h1>Ask Your PDF</h1>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <input
        type="text"
        placeholder="Ask your Question about your PDF"
        value={question}
        onChange={handleQuestionChange}
      />
      <button onClick={handleProcessPdf}>Process PDF</button>
      {response && <div>{response}</div>}
    </div>
  );
}

export default App;
