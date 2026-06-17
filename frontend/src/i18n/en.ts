export interface Translations {
  nav: {
    home: string;
    calculator: string;
    settings: string;
  };
  home: {
    hero_title: string;
    hero_subtitle: string;
    hero_cta: string;
    feature_tree_title: string;
    feature_tree_desc: string;
    feature_machines_title: string;
    feature_machines_desc: string;
    feature_lcm_title: string;
    feature_lcm_desc: string;
    about_title: string;
    about_desc: string;
  };
  calculator: {
    title: string;
    item_label: string;
    item_placeholder: string;
    rate_label: string;
    scale_label: string;
    calc_button: string;
    calculating: string;
    save_button: string;
    save_name_label: string;
    save_confirm: string;
    results_title: string;
    machines_title: string;
    raw_title: string;
    tree_title: string;
    scale_info: string;
    no_recipe: string;
    error_item: string;
    error_rate: string;
  };
  settings: {
    title: string;
    language_label: string;
    theme_label: string;
    dark: string;
    light: string;
    saved_title: string;
    no_saved: string;
    delete: string;
  };
  common: {
    min: string;
    machines: string;
    alternate: string;
    loading: string;
    error: string;
  };
}

const en: Translations = {
  nav: {
    home:       "Home",
    calculator: "Calculator",
    settings:   "Settings",
  },
  home: {
    hero_title:    "Satisfactory Perfect Calc",
    hero_subtitle: "Plan your factory. Maximize efficiency.",
    hero_cta:      "Open Calculator",
    feature_tree_title: "Dependency Tree",
    feature_tree_desc:  "Visualize the full production chain from raw ore to finished part.",
    feature_machines_title: "Machine Counter",
    feature_machines_desc:  "Get the exact number of machines needed at any production rate.",
    feature_lcm_title: "Optimal Scaling",
    feature_lcm_desc:  "Use LCM scaling to find the minimum all-integer production line.",
    about_title: "About the project",
    about_desc:  "Built for the INATEL C116 final project. Marcelo H. O. Pina Vieira — 2026.",
  },
  calculator: {
    title:           "Production Calculator",
    item_label:      "Target item",
    item_placeholder:"Search item…",
    rate_label:      "Target rate (units/min)",
    scale_label:     "Scale to integer machines (LCM)",
    calc_button:     "Calculate",
    calculating:     "Calculating…",
    save_button:     "Save production",
    save_name_label: "Production name",
    save_confirm:    "Saved!",
    results_title:   "Results",
    machines_title:  "Machines needed",
    raw_title:       "Raw resources",
    tree_title:      "Production tree",
    scale_info:      "Scaled ×{{n}} to get integer machine counts",
    no_recipe:       "No recipe found — this is a raw resource.",
    error_item:      "Please select a target item.",
    error_rate:      "Rate must be greater than zero.",
  },
  settings: {
    title:          "Settings",
    language_label: "Language",
    theme_label:    "Theme",
    dark:           "Dark",
    light:          "Light",
    saved_title:    "Saved productions",
    no_saved:       "No saved productions yet.",
    delete:         "Delete",
  },
  common: {
    min:       "/min",
    machines:  "machines",
    alternate: "Alternate",
    loading:   "Loading…",
    error:     "An error occurred.",
  },
};

export default en;
