import "./App.css";
import LandingPage from "./LandingPage";
import WeatherForcast from "./Weather Forecast/WeatherForcast";
import { Routes, Route, BrowserRouter as Router } from "react-router-dom";
import ChatBot from "./chatbot/ChatBot";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/weatherforecast" element={<WeatherForcast />} />
      <Route path="/chatbot" element={<ChatBot/>}/>
      </Routes>
    </Router>
  );
}

export default App;
