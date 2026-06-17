import React, { createContext, useContext, useState } from "react";
import en, { type Translations } from "../i18n/en";
import pt from "../i18n/pt";

type Lang = "en" | "pt";

interface LanguageContextValue {
  lang: Lang;
  t: Translations;
  setLang: (l: Lang) => void;
}

const TRANSLATIONS: Record<Lang, Translations> = { en, pt };

const LanguageContext = createContext<LanguageContextValue>({
  lang: "en",
  t: en,
  setLang: () => {},
});

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [lang, setLangState] = useState<Lang>(
    () => (localStorage.getItem("lang") as Lang) ?? "en"
  );

  const setLang = (l: Lang) => {
    localStorage.setItem("lang", l);
    setLangState(l);
  };

  return (
    <LanguageContext.Provider value={{ lang, t: TRANSLATIONS[lang], setLang }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
