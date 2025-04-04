import { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

function App() {
    const [userInput, setUserInput] = useState('');
    const [yodaSpeech, setYodaSpeech] = useState('');

    useEffect(() => {
        async function fetchUsers() {
            const users = await exampleAPIRequest();
            setUserInput(users);
        }
        fetchUsers();
    }, []);

    async function exampleAPIRequest() {
        try {
            const response = await axios.get('http://localhost:8080/api/users');
            return response.data.users;
        } catch (error) {
            console.error('Error fetching data:', error);
            return "Err";
        }
    }

    const handleInputChange = (e) => {
        setUserInput(e.target.value);
    };

    const getYodaSpeech = async (text: string) => {
        // This function could call an API to convert text to Yoda speech
        // For now, let's mock it by appending "Yoda says: " in front of the text
        return `Yoda says: ${text.split('').reverse().join('')}`;
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
        <div className = 'widget-group'>
            <div className="input-container widget">
                <p>Input</p>
                <textarea
                    className="text-field"
                    value={userInput}
                    onChange={handleInputChange}
                    placeholder="Type your sentence here..."
                />
            </div>

            <div className="input-container widget">
                <p>Output</p>
                <textarea
                  className="text-field"
                  value={yodaSpeech}
                  onChange={handleInputChange}
                  readOnly
                  placeholder=""
                />
            </div>
        </div>
      </div>
    );
}

export default App;
