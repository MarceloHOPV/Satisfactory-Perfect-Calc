export interface Building {
  id: number;
  name: string;
  description: string | null;
}

export interface Item {
  id: number;
  name: string;
  description: string | null;
  category: string | null;
}

export interface RecipeIngredient {
  item_id: number;
  amount_per_min: number;
  item: Item;
}

export interface RecipeProduct {
  item_id: number;
  amount_per_min: number;
  item: Item;
}

export interface Recipe {
  id: number;
  name: string;
  building_id: number;
  is_alternate: boolean;
  building: Building;
  ingredients: RecipeIngredient[];
  products: RecipeProduct[];
}

export interface ProductionNode {
  item_id: number;
  item_name: string;
  rate: number;
  is_raw: boolean;
  recipe_id: number | null;
  recipe_name: string | null;
  building_name: string | null;
  machines: number;
  inputs: ProductionNode[];
}

export interface MachineSummaryItem {
  recipe_id: number;
  recipe_name: string;
  building_name: string;
  machines: number;
}

export interface RawResourceItem {
  item_id: number;
  item_name: string;
  rate: number;
}

export interface CalculateResponse {
  tree: ProductionNode;
  machine_summary: MachineSummaryItem[];
  raw_resources: RawResourceItem[];
  scale_factor: number;
}

export interface SavedProduction {
  id: number;
  name: string;
  description: string | null;
  config: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}
