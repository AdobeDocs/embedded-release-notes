# Toast component contract

`toast.json` is the source consumed by the in-product web component. Transport
and deployment are deliberately separate from this versioned data contract.

## Selection and rendering

The component uses its `surface` attribute as a direct lookup key:

```html
<releasenote surface="ajo"></releasenote>
```

```js
const toast = registry.surfaces[element.getAttribute("surface")];
```

The component renders `title`, the two `items`, `action`, and `dismiss`.
`action.href` opens the full release note generated before the JSON entry.
Upserting a new release for an occupied surface replaces the previous entry.

## Example

```json
{
  "schema_version": 1,
  "surfaces": {
    "ajo": {
      "id": "ajo-2026-06-general",
      "surface": "ajo",
      "release": {
        "year": 2026,
        "month": 6,
        "slug": "general",
        "label": "June '26 release"
      },
      "title": "What's new for Journey Optimizer",
      "items": [
        {
          "icon": {
            "name": "journey",
            "foreground": "#4B3CB7",
            "background": "#8174E8"
          },
          "title": "Journey Simulation",
          "description": "Validate journey logic with simulated profiles."
        },
        {
          "icon": {
            "name": "optimize",
            "foreground": "#8D153A",
            "background": "#ED4776"
          },
          "title": "Optimized paths",
          "description": "Route audiences with targeting rules in Optimize."
        }
      ],
      "action": {
        "label": "See what's new",
        "href": "generated/ajo/2026/09/general/hub.html"
      },
      "dismiss": {
        "label": "Dismiss"
      },
      "source_request": "requests/ajo/2026/09/general.json"
    }
  }
}
```

Consumers must treat unknown fields as forward-compatible and must render
nothing when no surface matches.