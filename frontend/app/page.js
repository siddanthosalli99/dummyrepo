"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [formData, setFormData] = useState({
    age: "",
    sex: "male",
    bmi: "",
    children: "",
    smoker: "no",
    region: "southwest",
  });

  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          age: Number(formData.age),
          sex: formData.sex,
          bmi: Number(formData.bmi),
          children: Number(formData.children),
          smoker: formData.smoker,
          region: formData.region,
        }),
      });

      if (!response.ok) {
        throw new Error("Prediction request failed");
      }

      const data = await response.json();

      setPrediction(data);

      setHistory((previous) => [
        {
          id: Date.now(),
          ...formData,
          result: data,
        },
        ...previous,
      ]);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to connect to the DummyPro API. Make sure your FastAPI backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setFormData({
      age: "",
      sex: "male",
      bmi: "",
      children: "",
      smoker: "no",
      region: "southwest",
    });

    setPrediction(null);
    setError("");
  }

  function getPredictionValue(result) {
    return (
      result.predicted_charges ??
      result.prediction ??
      result.charges ??
      result.predicted_cost ??
      null
    );
  }

  return (
    <main className="page">
      <header className="header">
        <div>
          <p className="eyebrow">ML Prediction System</p>
          <h1>DummyPro</h1>
          <p className="subtitle">
            Predict individual medical insurance charges using machine
            learning.
          </p>
        </div>

        <div className="api-status">
          <span className="status-dot"></span>
          FastAPI
        </div>
      </header>

      <section className="content-grid">
        <div className="card">
          <div className="card-header">
            <div>
              <h2>Insurance Predictor</h2>
              <p>Enter the customer's information.</p>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="age">Age</label>

                <input
                  id="age"
                  name="age"
                  type="number"
                  min="1"
                  max="120"
                  placeholder="35"
                  value={formData.age}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="sex">Sex</label>

                <select
                  id="sex"
                  name="sex"
                  value={formData.sex}
                  onChange={handleChange}
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="bmi">BMI</label>

                <input
                  id="bmi"
                  name="bmi"
                  type="number"
                  step="0.1"
                  min="1"
                  max="100"
                  placeholder="27.5"
                  value={formData.bmi}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="children">Children</label>

                <input
                  id="children"
                  name="children"
                  type="number"
                  min="0"
                  max="20"
                  placeholder="2"
                  value={formData.children}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="smoker">Smoker</label>

                <select
                  id="smoker"
                  name="smoker"
                  value={formData.smoker}
                  onChange={handleChange}
                >
                  <option value="no">No</option>
                  <option value="yes">Yes</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="region">Region</label>

                <select
                  id="region"
                  name="region"
                  value={formData.region}
                  onChange={handleChange}
                >
                  <option value="southwest">Southwest</option>
                  <option value="southeast">Southeast</option>
                  <option value="northwest">Northwest</option>
                  <option value="northeast">Northeast</option>
                </select>
              </div>
            </div>

            <div className="form-actions">
              <button
                type="submit"
                className="predict-button"
                disabled={loading}
              >
                {loading ? "Predicting..." : "Predict Insurance Cost"}
              </button>

              <button
                type="button"
                className="reset-button"
                onClick={handleReset}
              >
                Reset
              </button>
            </div>
          </form>

          {error && <div className="error-box">{error}</div>}
        </div>

        <div className="card result-card">
          <p className="eyebrow">Prediction Result</p>

          {prediction ? (
            <>
              <h2>Estimated Charges</h2>

              <div className="prediction-value">
                {getPredictionValue(prediction) !== null
                  ? `$${Number(getPredictionValue(prediction)).toLocaleString(
                      "en-US",
                      {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      }
                    )}`
                  : "Prediction received"}
              </div>

              <p className="result-description">
                This prediction was generated by the DummyPro machine
                learning model.
              </p>

              <div className="result-details">
                <div>
                  <span>Age</span>
                  <strong>{formData.age}</strong>
                </div>

                <div>
                  <span>BMI</span>
                  <strong>{formData.bmi}</strong>
                </div>

                <div>
                  <span>Smoker</span>
                  <strong>{formData.smoker}</strong>
                </div>

                <div>
                  <span>Region</span>
                  <strong>{formData.region}</strong>
                </div>
              </div>
            </>
          ) : (
            <div className="empty-result">
              <div className="empty-icon">ML</div>

              <h2>No prediction yet</h2>

              <p>
                Fill in the customer information and click the prediction
                button.
              </p>
            </div>
          )}
        </div>
      </section>

      <section className="card history-card">
        <div className="card-header">
          <div>
            <h2>Prediction History</h2>
            <p>Predictions made during this session.</p>
          </div>

          <span className="history-count">{history.length}</span>
        </div>

        {history.length === 0 ? (
          <div className="empty-history">
            No predictions have been made yet.
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Age</th>
                  <th>Sex</th>
                  <th>BMI</th>
                  <th>Children</th>
                  <th>Smoker</th>
                  <th>Region</th>
                  <th>Charges</th>
                </tr>
              </thead>

              <tbody>
                {history.map((item) => {
                  const value = getPredictionValue(item.result);

                  return (
                    <tr key={item.id}>
                      <td>{item.age}</td>
                      <td>{item.sex}</td>
                      <td>{item.bmi}</td>
                      <td>{item.children}</td>
                      <td>{item.smoker}</td>
                      <td>{item.region}</td>
                      <td>
                        {value !== null
                          ? `$${Number(value).toLocaleString("en-US", {
                              minimumFractionDigits: 2,
                              maximumFractionDigits: 2,
                            })}`
                          : "N/A"}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <footer>
        <p>DummyPro · Machine Learning Prediction API</p>
      </footer>
    </main>
  );
}