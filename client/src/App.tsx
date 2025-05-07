import { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
    const [userInput, setUserInput] = useState('');
    const [yodaSpeech, setYodaSpeech] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
    };

    const handleSubmit = async () => {
        if (!userInput.trim()) return;

        setIsLoading(true);
        try {
            const response = await axios.post('http://localhost:8080/api/yoda-chat', {
                text: userInput
            });
            setYodaSpeech(response.data.response);
        } catch (error) {
            console.error('Error getting Yoda speech:', error);
            setYodaSpeech('Error, there was. Try again, you must.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
      <div className="App">
          <div className="title-container widget">
              <img
                className="yoda-image"
                src="../public/yoda_header.png"
                alt="Yoda"
              />
              <div className="header">
                  <h1>Yoda Speech Converter</h1>
                  <p>Transform your text into speech that sounds like Yoda!</p>
              </div>
          </div>
          <div className="widget-group">
              <div className="input-container widget">
                  <p>Input</p>
                  <textarea
                    className="convert-button"
                    value={userInput}
                    onChange={handleInputChange}
                    placeholder="Type your sentence here..."
                  />
                  <button
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className="submit-button"
                  >
                      {isLoading ? 'Processing...' : 'Convert to Yoda Speech'}
                  </button>
              </div>

              <div className="input-container widget">
                  <p>Output</p>
                  <textarea
                    value={yodaSpeech}
                    readOnly
                    placeholder="Yoda's wisdom will appear here..."
                  />
              </div>
          </div>
      </div>
    );
}

export default App;

