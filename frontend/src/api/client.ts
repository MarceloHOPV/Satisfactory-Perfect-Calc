import axios from "axios";
import type { Item, Recipe, Building, CalculateResponse, SavedProduction } from "./types";

const api = axios.create({ baseURL: "/api/v1" });

// ── Items ──────────────────────────────────────────────────────────────────────
export const getItems = (search?: string) =>
  api.get<Item[]>("/items/", { params: { search } }).then((r) => r.data);

export const createItem = (payload: Partial<Item>) =>
  api.post<Item>("/items/", payload).then((r) => r.data);

export const updateItem = (id: number, payload: Partial<Item>) =>
  api.put<Item>(`/items/${id}`, payload).then((r) => r.data);

export const deleteItem = (id: number) =>
  api.delete(`/items/${id}`);

// ── Recipes ────────────────────────────────────────────────────────────────────
export const getRecipes = (params?: { item_id?: number; include_alternates?: boolean }) =>
  api.get<Recipe[]>("/recipes/", { params }).then((r) => r.data);

export const getRecipe = (id: number) =>
  api.get<Recipe>(`/recipes/${id}`).then((r) => r.data);

export const createRecipe = (payload: unknown) =>
  api.post<Recipe>("/recipes/", payload).then((r) => r.data);

export const updateRecipe = (id: number, payload: unknown) =>
  api.put<Recipe>(`/recipes/${id}`, payload).then((r) => r.data);

export const deleteRecipe = (id: number) =>
  api.delete(`/recipes/${id}`);

// ── Buildings ──────────────────────────────────────────────────────────────────
export const getBuildings = () =>
  api.get<Building[]>("/buildings/").then((r) => r.data);

// ── Calculator ─────────────────────────────────────────────────────────────────
export const calculate = (payload: {
  target_item_id: number;
  target_rate: number;
  recipe_overrides?: Record<number, number>;
  scale_to_integers?: boolean;
}) => api.post<CalculateResponse>("/calculate/", payload).then((r) => r.data);

// ── Saved productions ──────────────────────────────────────────────────────────
export const getSavedProductions = () =>
  api.get<SavedProduction[]>("/saved-productions/").then((r) => r.data);

export const createSavedProduction = (payload: { name: string; description?: string; config: unknown }) =>
  api.post<SavedProduction>("/saved-productions/", payload).then((r) => r.data);

export const updateSavedProduction = (
  id: number,
  payload: { name?: string; description?: string; config?: unknown }
) => api.put<SavedProduction>(`/saved-productions/${id}`, payload).then((r) => r.data);

export const deleteSavedProduction = (id: number) =>
  api.delete(`/saved-productions/${id}`);
