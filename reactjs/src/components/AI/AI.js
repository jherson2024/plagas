import { useState } from "react";
import "./AI.css";
import { analyzeImage } from "../../services/ia";

const AI = () => {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(URL.createObjectURL(file));
      setResult("");
      setLoading(true);

      const resultFromAPI = await analyzeImage(file);
      setResult(resultFromAPI);
      setLoading(false);
    }
  };

  return (
    <div className="ai-container">
      <h1>🔬 Analizador Inteligente de Plagas</h1>
      <p className="subtitle">Sube una imagen de una hoja o planta para detectar posibles enfermedades.</p>

      <input type="file" accept="image/*" onChange={handleImageUpload} className="file-input" />
      {image && <img src={image} alt="Vista previa" className="preview" />}

      <div className={`result ${loading ? "loading" : ""}`}>
        {loading ? "Analizando imagen..." : <pre>{result}</pre>}
      </div>
    </div>
  );
};

export default AI;
