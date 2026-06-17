import { useLanguage } from "../contexts/LanguageContext";
import { useTheme } from "../contexts/ThemeContext";

export default function Settings() {
  const { t, lang, setLang } = useLanguage();
  const { theme, toggle } = useTheme();

  return (
    <div className="max-w-2xl mx-auto px-4 py-10 space-y-8">
      <h1 className="text-3xl font-bold text-white">{t.settings.title}</h1>

      {/* Language */}
      <div className="card space-y-4">
        <h2 className="text-lg font-semibold text-white">{t.settings.language_label}</h2>
        <div className="flex gap-3">
          {(["en", "pt"] as const).map((l) => (
            <button
              key={l}
              onClick={() => setLang(l)}
              className={`px-6 py-2.5 rounded-lg font-semibold transition-colors ${
                lang === l
                  ? "bg-satisfactory-orange text-white"
                  : "bg-satisfactory-elevated text-slate-400 hover:text-white border border-satisfactory-border"
              }`}
            >
              {l === "en" ? "🇺🇸 English" : "🇧🇷 Português"}
            </button>
          ))}
        </div>
      </div>

      {/* Theme */}
      <div className="card space-y-4">
        <h2 className="text-lg font-semibold text-white">{t.settings.theme_label}</h2>
        <div className="flex gap-3">
          {(["dark", "light"] as const).map((th) => (
            <button
              key={th}
              onClick={() => { if (theme !== th) toggle(); }}
              className={`px-6 py-2.5 rounded-lg font-semibold transition-colors ${
                theme === th
                  ? "bg-satisfactory-orange text-white"
                  : "bg-satisfactory-elevated text-slate-400 hover:text-white border border-satisfactory-border"
              }`}
            >
              {th === "dark" ? `🌙 ${t.settings.dark}` : `☀️ ${t.settings.light}`}
            </button>
          ))}
        </div>
      </div>

      {/* About */}
      <div className="card border-satisfactory-orange/20 space-y-2">
        <h2 className="text-lg font-semibold text-white">Satisfactory Perfect Calc</h2>
        <p className="text-slate-400 text-sm">Version 1.0.0 — INATEL C116 Final Project</p>
        <p className="text-slate-500 text-xs">
          Stack: FastAPI · React 18 · PostgreSQL · Docker Compose
        </p>
        <a
          href="https://github.com/MarceloHOPV/Satisfactory-Perfect-Calc"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block text-satisfactory-orange hover:text-satisfactory-orange-lt
                     text-sm transition-colors"
        >
          GitHub →
        </a>
      </div>
    </div>
  );
}
