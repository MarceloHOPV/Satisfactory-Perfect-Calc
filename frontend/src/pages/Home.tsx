import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useLanguage } from "../contexts/LanguageContext";
import * as api from "../api/client";
import type { SavedProduction } from "../api/types";

const features = (t: ReturnType<typeof useLanguage>["t"]) => [
  { icon: "🌲", title: t.home.feature_tree_title, desc: t.home.feature_tree_desc },
  { icon: "⚙️", title: t.home.feature_machines_title, desc: t.home.feature_machines_desc },
  { icon: "📐", title: t.home.feature_lcm_title, desc: t.home.feature_lcm_desc },
];

export default function Home() {
  const { t } = useLanguage();
  const navigate = useNavigate();

  const [saved, setSaved] = useState<SavedProduction[]>([]);

  useEffect(() => {
    api.getSavedProductions().then(setSaved).catch(() => {});
  }, []);

  const handleLoad = (sp: SavedProduction) => {
    navigate("/calculator", { state: { savedProduction: sp } });
  };

  const handleDelete = async (id: number) => {
    await api.deleteSavedProduction(id);
    setSaved((prev) => prev.filter((s) => s.id !== id));
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12 space-y-16">
      {/* Hero */}
      <section className="text-center space-y-6">
        <div className="inline-flex items-center gap-3 bg-satisfactory-surface border
                        border-satisfactory-orange/30 rounded-full px-5 py-2 text-satisfactory-orange
                        text-sm font-medium">
          <span>🏭</span>
          Satisfactory Update 8
        </div>
        <h1 className="text-4xl sm:text-6xl font-bold tracking-tight">
          <span className="text-satisfactory-orange">Satisfactory</span>
          <br />
          <span className="text-white">Perfect Calc</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-xl mx-auto">{t.home.hero_subtitle}</p>
        <Link
          to="/calculator"
          className="inline-block btn-primary text-base px-8 py-3 shadow-lg
                     shadow-satisfactory-orange/20"
        >
          {t.home.hero_cta} →
        </Link>
      </section>

      {/* Saved productions — shown only when there is at least one */}
      {saved.length > 0 && (
        <section className="card space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white">
              📋 {t.settings.saved_title}
            </h2>
            <span className="text-xs text-slate-500">{saved.length} saved</span>
          </div>
          <ul className="space-y-2">
            {saved.map((sp) => (
              <li
                key={sp.id}
                className="flex items-center justify-between gap-3 p-3 bg-satisfactory-elevated
                           rounded-lg border border-satisfactory-border"
              >
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-semibold text-white truncate">{sp.name}</p>
                  {Boolean(sp.config?.target_item_name) && (
                    <p className="text-xs text-satisfactory-orange mt-0.5">
                      {String(sp.config.target_item_name)} — {String(sp.config.target_rate)}/min
                    </p>
                  )}
                  <p className="text-xs text-slate-600 mt-0.5">
                    {new Date(sp.updated_at).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex gap-2 shrink-0">
                  <button
                    onClick={() => handleLoad(sp)}
                    className="btn-primary text-xs px-4 py-1.5"
                  >
                    Load
                  </button>
                  <button
                    onClick={() => handleDelete(sp.id)}
                    className="text-red-500 hover:text-red-400 text-xs font-medium px-3 py-1.5
                               rounded border border-red-800 hover:border-red-600 transition-colors"
                  >
                    {t.settings.delete}
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Features */}
      <section>
        <div className="grid sm:grid-cols-3 gap-6">
          {features(t).map((f) => (
            <div key={f.title} className="card hover:border-satisfactory-orange/50 transition-colors">
              <div className="text-4xl mb-4">{f.icon}</div>
              <h3 className="font-semibold text-white mb-2">{f.title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="card space-y-6">
        <h2 className="text-2xl font-bold text-white">How it works</h2>
        <div className="space-y-4 text-slate-300 text-sm leading-relaxed">
          <p>
            Select any item in the game, enter your desired output rate per minute, and the
            calculator walks the entire dependency chain — recursively finding every ingredient,
            counting how many machines are needed at each step, and listing raw-resource demands.
          </p>
          <p>
            Enable <span className="text-satisfactory-orange font-semibold">LCM scaling</span> to
            automatically multiply the whole production line by the least common multiple of all
            machine-count denominators, giving you the smallest all-integer factory blueprint.
          </p>
          <p>
            All game data (recipes, buildings, items) is stored in PostgreSQL and fully editable
            through the REST API — add alternate recipes, adjust rates, or extend the database as
            the game updates.
          </p>
        </div>
      </section>

      {/* About */}
      <section className="card border-satisfactory-orange/20">
        <h2 className="text-xl font-bold text-white mb-3">{t.home.about_title}</h2>
        <p className="text-slate-400 text-sm">{t.home.about_desc}</p>
        <div className="mt-4 flex flex-wrap gap-3 text-xs">
          {["FastAPI", "React", "PostgreSQL", "Docker Compose", "SQLAlchemy", "Tailwind CSS"].map(
            (tech) => (
              <span
                key={tech}
                className="badge bg-satisfactory-elevated text-slate-300 border border-satisfactory-border"
              >
                {tech}
              </span>
            )
          )}
        </div>
      </section>
    </div>
  );
}
