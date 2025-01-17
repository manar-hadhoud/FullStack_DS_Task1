import React, { useState } from 'react';
import './SummerizationForm.css'; 


function SummerizationForm() {

  const [inputPrompt, setprompt] = useState({
    text: '',
  });
  const [generation, setGeneration] = useState(''); 
  const [error, setError] = useState(null);

  // Function to handle input changes
  const handleChange = (e) => {
    setprompt({
      ...inputPrompt,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior

    setError(null);
    setGeneration('');
    try {
      //http://127.0.0.1:8000/summarization/summerize
      // Send a POST request to your FastAPI backend
      const response = await fetch('http://localhost:8080/summerize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(inputPrompt), // Send the user input as JSON
      });

      const data = await response.json();

      if (response.ok) {
        setGeneration(data.generated_text); // Update state with generated text
        setError(null); // Clear any previous errors
      } else {
        const errorMessage = data.error || 'An error occurred while summarizing';

        // Check for specific error types
        if (response.status === 400) {
          setError(`Validation Error: ${errorMessage}`);
        } else if (response.status === 422) {
          setError(`Input Format Error: ${errorMessage}`);
        } else {
          setError(`Server Error: ${errorMessage}`);
        }
        

      }
    } catch (err) {
      setError('Failed to connect to the server');
      
    }
    
  };

  return (
    <div className="text-summerization">
      <h1>Summerization Service</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          name="text"
          rows="20"
          cols="100"
          placeholder="Enter text to summarize"
          value={inputPrompt.text}
          onChange={handleChange}
          className="input-text"
        />
        <button type="submit" className="submit-button">
          Summerize
        </button>
      </form>
      <div className="output-section">
          {/* Conditionally render error message */}
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
        {/* Conditionally render generated summary */}
        {generation && (
          <div>
            <h2>Summarized Text:</h2>
            <p className="generated-text">{generation}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default SummerizationForm;