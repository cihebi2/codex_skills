# Request Format

Use a structured JSON request whenever the user can describe their dataset.

## Preferred fields

- `goal`: Plain-language analysis goal.
- `data_schema.n_tables`: Number of input tables.
- `data_schema.variables[]`: Variables with `name`, `type`, `role`, and optional `description`.
- `data_schema.has_grouping`: Whether grouped comparison is required.
- `data_schema.has_matrix`: Whether the data is matrix-like.
- `data_schema.has_geo`: Whether longitude or latitude is present.
- `data_schema.has_hierarchy`: Whether the data contains flows, links, trees, or nested structure.
- `data_schema.has_replicates`: Whether replicate-level measurements exist.
- `preferences.style[]`: Style hints such as `简洁`, `论文风`, or `高对比`.
- `preferences.need_stats`: Whether significance markers, error bars, or confidence intervals are required.
- `must_have_features[]`: Hard visual requirements such as `散点`, `显著`, `误差线`, `渐变色`.
- `avoid_families[]`: Chart families that must be excluded.
- `notes`: Any domain constraints not captured above.

## Example

```json
{
  "goal": "我有多个处理组的连续数值，想比较分布差异，最好带显著性标注和散点，风格简洁适合论文",
  "data_schema": {
    "n_tables": 1,
    "variables": [
      { "name": "treatment", "type": "categorical", "role": "group" },
      { "name": "feature", "type": "categorical", "role": "category" },
      { "name": "value", "type": "numeric", "role": "measurement" }
    ],
    "has_grouping": true,
    "has_replicates": true
  },
  "preferences": {
    "style": ["简洁", "论文风"],
    "need_stats": true
  },
  "must_have_features": ["散点", "显著"],
  "avoid_families": ["饼图"]
}
```

## Expected output

Return a ranked list with:

- template id and template name
- resolved chart family and source chart family
- short matching reasons
- local code and asset paths
- suggested next step: inspect preview, adapt Python code, or adapt R code
