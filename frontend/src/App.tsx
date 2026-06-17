import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ThemeProvider } from "./contexts/ThemeContext";
import { LanguageProvider } from "./contexts/LanguageContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Calculator from "./pages/Calculator";
import Settings from "./pages/Settings";

export default function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <BrowserRouter>
          <div className="min-h-screen flex flex-col">
            <Navbar />
            <main className="flex-1">
              <Routes>
                <Route path="/"            element={<Home />} />
                <Route path="/calculator"  element={<Calculator />} />
                <Route path="/settings"    element={<Settings />} />
              </Routes>
            </main>
          </div>
        </BrowserRouter>
      </LanguageProvider>
    </ThemeProvider>
  );
}
