import { Link, useLocation } from "react-router-dom";
import { useTheme } from "../contexts/ThemeContext";
import { useLanguage } from "../contexts/LanguageContext";

const SunIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
      d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
  </svg>
);
const MoonIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
      d="M21 12.79A9 9 0 1111.21 3a7 7 0 009.79 9.79z" />
  </svg>
);
const FactoryIcon = () => (
  <svg className="w-7 h-7 text-satisfactory-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
      d="M3 21V11l5-5 5 5 5-5v10a1 1 0 01-1 1H4a1 1 0 01-1-1zM9 21v-4h6v4" />
  </svg>
);

export default function Navbar() {
  const { pathname } = useLocation();
  const { theme, toggle } = useTheme();
  const { t, lang, setLang } = useLanguage();

  const link = (to: string, label: string) => (
    <Link
      to={to}
      className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors duration-150 ${
        pathname === to
          ? "bg-satisfactory-orange text-white"
          : "text-slate-400 hover:text-white"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <nav className="sticky top-0 z-50 bg-satisfactory-surface border-b border-satisfactory-border
                    backdrop-blur-sm">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center gap-4">
        <Link to="/" className="flex items-center gap-2 mr-4">
          <FactoryIcon />
          <span className="font-bold text-satisfactory-orange hidden sm:block">SPC</span>
        </Link>

        <div className="flex items-center gap-1 flex-1">
          {link("/",           t.nav.home)}
          {link("/calculator", t.nav.calculator)}
          {link("/settings",   t.nav.settings)}
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setLang(lang === "en" ? "pt" : "en")}
            className="text-xs text-slate-400 hover:text-white transition-colors px-2 py-1
                       rounded border border-satisfactory-border"
          >
            {lang === "en" ? "PT" : "EN"}
          </button>
          <button
            onClick={toggle}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white transition-colors"
            aria-label="Toggle theme"
          >
            {theme === "dark" ? <SunIcon /> : <MoonIcon />}
          </button>
        </div>
      </div>
    </nav>
  );
}
