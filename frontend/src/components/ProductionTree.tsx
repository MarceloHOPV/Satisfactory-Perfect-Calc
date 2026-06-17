import type { ProductionNode } from "../api/types";

interface Props {
  node: ProductionNode;
  depth?: number;
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

const fmt = (n: number) => {
  if (Number.isInteger(n) || Math.abs(n - Math.round(n)) < 0.0001) return Math.round(n).toString();
  return n.toFixed(2);
};

export default function ProductionTree({ node, depth = 0 }: Props) {
  const isRoot = depth === 0;

  const borderColor = node.is_raw
    ? "border-emerald-600"
    : isRoot
    ? "border-satisfactory-orange"
    : "border-satisfactory-border";

  const emoji = node.building_name ? (BUILDING_EMOJI[node.building_name] ?? "🏭") : "⛏️";

  return (
    <div className={`relative ${depth > 0 ? "ml-6 mt-2" : ""}`}>
      {depth > 0 && (
        <span className="absolute -left-4 top-4 h-px w-4 bg-satisfactory-border" />
      )}

      <div
        className={`card border-l-2 ${borderColor} py-3 px-4 flex flex-col gap-1`}
      >
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-lg">{emoji}</span>
          <span className="font-semibold text-sm text-white">{node.item_name}</span>
          <span className="text-satisfactory-orange text-sm font-mono">
            {fmt(node.rate)}/min
          </span>
          {!node.is_raw && (
            <span className="text-slate-400 text-xs">
              {fmt(node.machines)} × {node.building_name}
            </span>
          )}
          {node.is_raw && (
            <span className="badge bg-emerald-900 text-emerald-300">raw</span>
          )}
        </div>
        {node.recipe_name && (
          <span className="text-xs text-slate-500 ml-7">{node.recipe_name}</span>
        )}
      </div>

      {node.inputs.length > 0 && (
        <div className="relative border-l border-satisfactory-border ml-3 pl-1">
          {node.inputs.map((child, i) => (
            <ProductionTree key={i} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}
