interface Props {
  building_name: string;
  recipe_name: string;
  machines: number;
}

const BUILDING_EMOJI: Record<string, string> = {
  Smelter:             "🔥",
  Constructor:         "⚙️",
  Assembler:           "🔧",
  Foundry:             "🏭",
  Manufacturer:        "🏗️",
  "Oil Refinery":      "🛢️",
  Blender:             "🌀",
  Packager:            "📦",
};

const fmt = (n: number) =>
  Number.isInteger(n) || Math.abs(n - Math.round(n)) < 0.0001
    ? Math.round(n).toString()
    : n.toFixed(3);

export default function MachineCard({ building_name, recipe_name, machines }: Props) {
  const emoji = BUILDING_EMOJI[building_name] ?? "🏭";
  const isInteger = Number.isInteger(machines) || Math.abs(machines - Math.round(machines)) < 0.001;

  return (
    <div className="flex items-center gap-3 p-3 bg-satisfactory-elevated rounded-lg
                    border border-satisfactory-border">
      <span className="text-2xl">{emoji}</span>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-white truncate">{recipe_name}</p>
        <p className="text-xs text-slate-400">{building_name}</p>
      </div>
      <div className="text-right shrink-0">
        <span
          className={`text-lg font-bold font-mono ${
            isInteger ? "text-satisfactory-orange" : "text-amber-400"
          }`}
        >
          {fmt(machines)}
        </span>
        {!isInteger && (
          <p className="text-xs text-slate-500">
            ~{Math.ceil(machines)} @ {((machines / Math.ceil(machines)) * 100).toFixed(0)}%
          </p>
        )}
      </div>
    </div>
  );
}
