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
## Item deep links

Each item may carry an optional `href`, such as
`generated/ajo/2026/10/loyalty/hub.html#autosave-challenge-drafts`. It must
point to the same hub as `action.href`, plus the `#` id of the matching item in
that hub (the validator checks that the id exists in the hub).

When a user selects an item, the component opens the release-notes modal with
that `href` (hash included) as the iframe address instead of `action.href`. The
hub reads the hash on load: it opens the tab that holds the item, scrolls to it
and highlights it. When an item has no `href`, or the component does not
support it yet, the card falls back to `action.href` and the hub opens on its
first tab. The component must not strip the `#` fragment.

## Dismissal

Closing the card (the X or the `dismiss` action) must keep it hidden until the
next update. The component stores the dismissed entry `id` (for example in
`localStorage`, keyed by surface) and renders nothing while the stored `id`
equals the registry `id`. A new release gets a new `id`, so the card shows
again. The data contract has no field for this behavior.
