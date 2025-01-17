import './App.css';
import React from 'react';
import ClassificationForm from './components/ClassificationForm';
import SummerizationForm from './components/SummerizationForm';


function App() {
  return (
    <div className="App">
      <h1>AI Services</h1>
      <ClassificationForm />
      <SummerizationForm />
    </div>
  );
}

export default App;
