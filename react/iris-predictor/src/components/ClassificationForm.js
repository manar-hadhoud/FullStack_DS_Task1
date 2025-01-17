import React, { useState } from 'react';
import './form.css'; 

function ClassificationForm() {
    //state ti intialize
    const [features, setFeatures] = useState({
        sepal_length: '',
        sepal_width: '',
        petal_length: '',
        petal_width: '',
      });
    // State to store the predicted class from the backend
    const [prediction, setPrediction] = useState('');  

    //on trigger change the stae of features
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFeatures((prevFeatures) => ({
            ...prevFeatures,
            [name]: value === "" ? "" : parseFloat(value),
        }));
    };

    //Handle form submission (send data to FastAPI backend)
    //sending the form data (the features) to the FastAPI backend for prediction, 
    //receiving the response
    //updating the component state accordingly
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate inputs
        for (const key in features) {
            if (!features[key]) {
                console.log(`Missing value for ${key}`);
                setPrediction("All fields are required.");
                return;
            }
        }
        console.log("Features being sent:", features); // Log features

        try {
            //http://127.0.0.1:8000/iris/predict
            const response = await fetch('http://127.0.0.1:8000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(features), // Send feature data in the request body as json
            });

            if (response.ok) {
                const data = await response.json();
                setPrediction(data.predicted_class); // Set predicted class from the response
            } else {
                setPrediction('Prediction failed');
            }
        } catch (error) {
            console.error('Error during prediction request:', error);
            setPrediction('Error during prediction');
        }
    };

  return (
    <div className="model-prediction-container">
      <h2>Classification Prediction</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
            <label>Feature 1:</label>
            <input type="number" name="sepal_length" placeholder="Feature 1" value={features.sepal_length} onChange={handleChange}/>
        </div>
        
        <div className="form-group">
            <label>Feature 2:</label>
            <input type="number" name="sepal_width" placeholder="Feature 2" value={features.sepal_width} onChange={handleChange}/>
        </div>

        <div className="form-group">
            <label>Feature 3:</label>
            <input type="number" name="petal_length" placeholder="Feature 3" value={features.petal_length} onChange={handleChange}/>
        </div>
        
        <div className="form-group">
            <label>Feature 4:</label>
            <input type="number" name="petal_width" placeholder="Feature 4" value={features.petal_width} onChange={handleChange}/>
        </div>
        
        <button type="submit">Classify</button>

        <div className="prediction-box">
          <h3>Predicted Class: {prediction}</h3>
        </div>
      </form>
    </div>
  );
}

export default ClassificationForm;


//reduce redundency
/**const featureNames = [
    { name: 'sepal_length', label: 'Sepal Length' },
    { name: 'sepal_width', label: 'Sepal Width' },
    { name: 'petal_length', label: 'Petal Length' },
    { name: 'petal_width', label: 'Petal Width' },
];
{featureNames.map(({ name, label }, index) => (
                    <div className="form-group" key={index}>
                        <label>{label}:</label>
                        <input
                            type="number"
                            name={name}
                            placeholder={label}
                            value={features[name]}
                            onChange={handleChange}
                        />
                    </div>
                ))}**/   
   
//hardcoding solving
//const API_URL = process.env.REACT_APP_API_URL;
//const response = await fetch(`${API_URL}/predict`, { ... });
//isNaN(features[key]) ensures valid numeric value
