import { useEffect, useRef, useState } from "react";
import { useLocation } from "react-router-dom";
import { useLanguage } from "../contexts/LanguageContext";
import * as api from "../api/client";
import type { Item, CalculateResponse, SavedProduction } from "../api/types";
import ProductionTree from "../components/ProductionTree";
import MachineCard from "../components/MachineCard";

const fmt = (n: number) =>
  Number.isInteger(n) || Math.abs(n - Math.round(n)) < 0.001
    ? Math.round(n).toString()
    : n.toFixed(2);

export default function Calculator() {
  const { t } = useLanguage();
  const location = useLocation();

  const [items, setItems] = useState<Item[]>([]);
  const [search, setSearch] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);
  const [targetItem, setTargetItem] = useState<Item | null>(null);
  const [rate, setRate] = useState<string>("60");
  const [scaleIntegers, setScaleIntegers] = useState(false);
  const [result, setResult] = useState<CalculateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Save production
  const [saveName, setSaveName] = useState("");
  const [saveStatus, setSaveStatus] = useState<"idle" | "saved">("idle");

  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api.getItems().then((fetched) => {
      setItems(fetched);

      // Pre-load a saved production passed via router state (from Settings page)
      const sp = (location.state as { savedProduction?: SavedProduction } | null)
        ?.savedProduction;
      if (!sp?.config) return;

      const cfg = sp.config as {
        target_item_id?: number;
        target_item_name?: string;
        target_rate?: number;
        scale_to_integers?: boolean;
        result?: CalculateResponse;
      };

      if (cfg.target_item_id) {
        const found = fetched.find((i) => i.id === cfg.target_item_id) ?? null;
        setTargetItem(found);
        setSearch(cfg.target_item_name ?? found?.name ?? "");
      }
      if (cfg.target_rate) setRate(String(cfg.target_rate));
      if (cfg.scale_to_integers !== undefined) setScaleIntegers(cfg.scale_to_integers);
      if (cfg.result) setResult(cfg.result);
    }).catch(() => setError(t.common.error));
  }, []);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node))
        setShowDropdown(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const filtered = items.filter((i) =>
    i.name.toLowerCase().includes(search.toLowerCase())
  );

  const selectItem = (item: Item) => {
    setTargetItem(item);
    setSearch(item.name);
    setShowDropdown(false);
    setResult(null);
  };

  const handleCalculate = async () => {
    if (!targetItem) { setError(t.calculator.error_item); return; }
    const rateNum = parseFloat(rate);
    if (!rateNum || rateNum <= 0) { setError(t.calculator.error_rate); return; }
    setError(null);
    setLoading(true);
    try {
      const res = await api.calculate({
        target_item_id: targetItem.id,
        target_rate: rateNum,
        scale_to_integers: scaleIntegers,
      });
      setResult(res);
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })
        .response?.data?.detail ?? t.common.error;
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!result || !saveName.trim()) return;
    await api.createSavedProduction({
      name: saveName.trim(),
      config: {
        target_item_id: targetItem?.id,
        target_item_name: targetItem?.name,
        target_rate: parseFloat(rate),
        scale_to_integers: scaleIntegers,
        result,
      },
    });
    setSaveStatus("saved");
    setTimeout(() => setSaveStatus("idle"), 2000);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-10 space-y-8">
      <h1 className="text-3xl font-bold text-white">{t.calculator.title}</h1>

      {/* Input card */}
      <div className="card space-y-5">
        <div className="grid sm:grid-cols-3 gap-4 items-end">
          {/* Item search */}
          <div className="sm:col-span-2 relative" ref={dropdownRef}>
            <label className="label">{t.calculator.item_label}</label>
            <input
              className="input"
              placeholder={t.calculator.item_placeholder}
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setShowDropdown(true);
                if (!e.target.value) setTargetItem(null);
              }}
              onFocus={() => setShowDropdown(true)}
            />
            {showDropdown && filtered.length > 0 && (
              <ul className="absolute z-20 mt-1 w-full bg-satisfactory-elevated border
                             border-satisfactory-border rounded-lg shadow-xl max-h-60 overflow-y-auto">
                {filtered.map((item) => (
                  <li
                    key={item.id}
                    onMouseDown={() => selectItem(item)}
                    className="px-4 py-2.5 cursor-pointer hover:bg-satisfactory-surface
                               text-sm text-slate-200 flex items-center justify-between"
                  >
                    <span>{item.name}</span>
                    {item.category && (
                      <span className="text-xs text-slate-500">{item.category}</span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Rate */}
          <div>
            <label className="label">{t.calculator.rate_label}</label>
            <input
              className="input"
              type="number"
              min={0.1}
              step={0.1}
              value={rate}
              onChange={(e) => setRate(e.target.value)}
            />
          </div>
        </div>

        {/* LCM toggle */}
        <label className="flex items-center gap-3 cursor-pointer select-none w-fit">
          <div
            onClick={() => setScaleIntegers((v) => !v)}
            className={`relative w-11 h-6 rounded-full transition-colors duration-200 ${
              scaleIntegers ? "bg-satisfactory-orange" : "bg-satisfactory-border"
            }`}
          >
            <span
              className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow
                          transition-transform duration-200 ${scaleIntegers ? "translate-x-5" : ""}`}
            />
          </div>
          <span className="text-sm text-slate-300">{t.calculator.scale_label}</span>
        </label>

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button
          onClick={handleCalculate}
          disabled={loading}
          className="btn-primary w-full sm:w-auto"
        >
          {loading ? t.calculator.calculating : t.calculator.calc_button}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {scaleIntegers && result.scale_factor > 1 && (
            <div className="bg-amber-900/30 border border-amber-700/50 rounded-lg px-4 py-3
                            text-amber-300 text-sm">
              {t.calculator.scale_info.replace("{{n}}", String(result.scale_factor))}
            </div>
          )}

          <div className="grid sm:grid-cols-2 gap-6">
            {/* Machines */}
            <div className="card space-y-3">
              <h2 className="text-lg font-semibold text-white">{t.calculator.machines_title}</h2>
              {result.machine_summary.map((m) => (
                <MachineCard key={m.recipe_id} {...m} />
              ))}
            </div>

            {/* Raw resources */}
            <div className="card space-y-3">
              <h2 className="text-lg font-semibold text-white">{t.calculator.raw_title}</h2>
              {result.raw_resources.map((r) => (
                <div
                  key={r.item_id}
                  className="flex items-center justify-between p-3 bg-satisfactory-elevated
                             rounded-lg border border-emerald-900/50"
                >
                  <div className="flex items-center gap-2">
                    <span>⛏️</span>
                    <span className="text-sm text-white">{r.item_name}</span>
                  </div>
                  <span className="font-mono text-emerald-400 font-semibold">
                    {fmt(r.rate)}/min
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Production tree */}
          <div className="card">
            <h2 className="text-lg font-semibold text-white mb-4">{t.calculator.tree_title}</h2>
            <div className="overflow-x-auto">
              <ProductionTree node={result.tree} />
            </div>
          </div>

          {/* Save production */}
          <div className="card">
            <h2 className="text-lg font-semibold text-white mb-4">{t.calculator.save_button}</h2>
            <div className="flex gap-3">
              <input
                className="input"
                placeholder={t.calculator.save_name_label}
                value={saveName}
                onChange={(e) => setSaveName(e.target.value)}
              />
              <button
                onClick={handleSave}
                className={`btn-secondary shrink-0 ${saveStatus === "saved" ? "text-green-400" : ""}`}
              >
                {saveStatus === "saved" ? `✓ ${t.calculator.save_confirm}` : t.calculator.save_button}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
