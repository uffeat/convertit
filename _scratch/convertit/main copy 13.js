const { default: use } = await import(`https://rolloh.vercel.app/anvil/use.js`);
const {
  Reactive,
  Ref,
  Sheet,
  app,
  breakpoints,
  capitalize,
  component,
  css,
  html,
  is,
} = await use("@/rollo/");
const { frame } = await use("@/frame/");
const { Form, Input } = await use("@/form/");
await use(`@/bootstrap/`);

const icons = {
  area: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-aspect-ratio" viewBox="0 0 16 16">
  <path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h13A1.5 1.5 0 0 1 16 3.5v9a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 12.5zM1.5 3a.5.5 0 0 0-.5.5v9a.5.5 0 0 0 .5.5h13a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5z"/>
  <path d="M2 4.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1H3v2.5a.5.5 0 0 1-1 0zm12 7a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1 0-1H13V8.5a.5.5 0 0 1 1 0z"/>
</svg>`,
  arrows: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-arrows" viewBox="0 0 16 16">
  <path d="M1.146 8.354a.5.5 0 0 1 0-.708l2-2a.5.5 0 1 1 .708.708L2.707 7.5h10.586l-1.147-1.146a.5.5 0 0 1 .708-.708l2 2a.5.5 0 0 1 0 .708l-2 2a.5.5 0 0 1-.708-.708L13.293 8.5H2.707l1.147 1.146a.5.5 0 0 1-.708.708z"/>
</svg>`,
  beaker: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-beaker" viewBox="0 0 16 16">
  <path d="M9.5 3a.5.5 0 0 0 0 1H13V3zm2 2a.5.5 0 0 0 0 1H13V5zm-2 2a.5.5 0 0 0 0 1H13V7zm2 2a.5.5 0 0 0 0 1H13V9zm-2 2a.5.5 0 0 0 0 1H13v-1zm2 2a.5.5 0 0 0 0 1H13v-1z"/>
  <path d="M.5 0a.5.5 0 0 0-.354.854l.122.12A2.5 2.5 0 0 1 1 2.744V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V2.743a2.5 2.5 0 0 1 .732-1.768l.122-.121A.5.5 0 0 0 15.5 0zM2 2.743A3.5 3.5 0 0 0 1.535 1h12.93A3.5 3.5 0 0 0 14 2.743V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1z"/>
</svg>`,
  copy: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-c-circle" viewBox="0 0 16 16">
  <path d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.146 4.992c-1.212 0-1.927.92-1.927 2.502v1.06c0 1.571.703 2.462 1.927 2.462.979 0 1.641-.586 1.729-1.418h1.295v.093c-.1 1.448-1.354 2.467-3.03 2.467-2.091 0-3.269-1.336-3.269-3.603V7.482c0-2.261 1.201-3.638 3.27-3.638 1.681 0 2.935 1.054 3.029 2.572v.088H9.875c-.088-.879-.768-1.512-1.729-1.512"/>
</svg>`,
  hourglass: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-hourglass" viewBox="0 0 16 16">
  <path d="M2 1.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1-.5-.5m2.5.5v1a3.5 3.5 0 0 0 1.989 3.158c.533.256 1.011.791 1.011 1.491v.702c0 .7-.478 1.235-1.011 1.491A3.5 3.5 0 0 0 4.5 13v1h7v-1a3.5 3.5 0 0 0-1.989-3.158C8.978 9.586 8.5 9.052 8.5 8.351v-.702c0-.7.478-1.235 1.011-1.491A3.5 3.5 0 0 0 11.5 3V2z"/>
</svg>`,
  "minecart-loaded": `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-minecart-loaded" viewBox="0 0 16 16">
  <path d="M4 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2m0 1a2 2 0 1 0 0-4 2 2 0 0 0 0 4m8-1a1 1 0 1 1 0-2 1 1 0 0 1 0 2m0 1a2 2 0 1 0 0-4 2 2 0 0 0 0 4M.115 3.18A.5.5 0 0 1 .5 3h15a.5.5 0 0 1 .491.592l-1.5 8A.5.5 0 0 1 14 12H2a.5.5 0 0 1-.491-.408l-1.5-8a.5.5 0 0 1 .106-.411zm.987.82 1.313 7h11.17l1.313-7z"/>
  <path fill-rule="evenodd" d="M6 1a2.498 2.498 0 0 1 4 0c.818 0 1.545.394 2 1 .67 0 1.552.57 2 1h-2c-.314 0-.611-.15-.8-.4-.274-.365-.71-.6-1.2-.6-.314 0-.611-.15-.8-.4a1.497 1.497 0 0 0-2.4 0c-.189.25-.486.4-.8.4-.507 0-.955.251-1.228.638q-.136.194-.308.362H3c.13-.147.401-.432.562-.545a1.6 1.6 0 0 0 .393-.393A2.5 2.5 0 0 1 6 1"/>
</svg>`,
  ruler: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-rulers" viewBox="0 0 16 16">
  <path d="M1 0a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h5v-1H2v-1h4v-1H4v-1h2v-1H2v-1h4V9H4V8h2V7H2V6h4V2h1v4h1V4h1v2h1V2h1v4h1V4h1v2h1V2h1v4h1V1a1 1 0 0 0-1-1z"/>
</svg>`,
  spedometer: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-speedometer" viewBox="0 0 16 16">
  <path d="M8 2a.5.5 0 0 1 .5.5V4a.5.5 0 0 1-1 0V2.5A.5.5 0 0 1 8 2M3.732 3.732a.5.5 0 0 1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707M2 8a.5.5 0 0 1 .5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 8m9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 1H12a.5.5 0 0 1-.5-.5m.754-4.246a.39.39 0 0 0-.527-.02L7.547 7.31A.91.91 0 1 0 8.85 8.569l3.434-4.297a.39.39 0 0 0-.029-.518z"/>
  <path fill-rule="evenodd" d="M6.664 15.889A8 8 0 1 1 9.336.11a8 8 0 0 1-2.672 15.78zm-4.665-4.283A11.95 11.95 0 0 1 8 10c2.186 0 4.236.585 6.001 1.606a7 7 0 1 0-12.002 0"/>
</svg>`,
  thermometer: `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-thermometer" viewBox="0 0 16 16">
  <path d="M8 14a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3"/>
  <path d="M8 0a2.5 2.5 0 0 0-2.5 2.5v7.55a3.5 3.5 0 1 0 5 0V2.5A2.5 2.5 0 0 0 8 0M6.5 2.5a1.5 1.5 0 1 1 3 0v7.987l.167.15a2.5 2.5 0 1 1-3.333 0l.166-.15z"/>
</svg>`,
  wind: `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-wind" viewBox="0 0 16 16">
  <path d="M12.5 2A2.5 2.5 0 0 0 10 4.5a.5.5 0 0 1-1 0A3.5 3.5 0 1 1 12.5 8H.5a.5.5 0 0 1 0-1h12a2.5 2.5 0 0 0 0-5m-7 1a1 1 0 0 0-1 1 .5.5 0 0 1-1 0 2 2 0 1 1 2 2h-5a.5.5 0 0 1 0-1h5a1 1 0 0 0 0-2M0 9.5A.5.5 0 0 1 .5 9h10.042a3 3 0 1 1-3 3 .5.5 0 0 1 1 0 2 2 0 1 0 2-2H.5a.5.5 0 0 1-.5-.5"/>
</svg>`,
  x: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
  <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
</svg>`,
};

// Create footer
// XXX TODO Move to frame component parcel
(() => {
  css`
    footer > section {
      width: 100%;
      display: flex;
      justify-content: center;
      padding-top: 0.5rem;
    }

    footer > section > p {
      color: var(--bs-gray-600);
      display: flex;
    }

    footer > section > p > span {
      color: var(--bs-white);
      display: flex;
      font-size: 1.125rem;
      padding-left: 0.125rem;
    }
  `.use(frame);

  const footer = frame.shadow.find("footer");
  const section = component.section({
    parent: footer,
  });
  const text = component.p(component.span({ text: "Convertit" }));
  text.insert.afterbegin(icons.copy);
  section.append(text);
})();

const units = {
  // area
  "cm\u00B2": [(v) => v / 100 ** 2, (v) => v * 100 ** 2],
  "m\u00B2": [(v) => v, (v) => v],
  "km\u00B2": [(v) => v * 1_000 ** 2, (v) => v / 1_000 ** 2],
  "inch\u00B2": [(v) => v * 0.0254 ** 2, (v) => v / 0.0254 ** 2],
  "ft\u00B2": [(v) => v * 0.3048 ** 2, (v) => v / 0.3048 ** 2],
  "mile\u00B2": [(v) => v * 1609.344 ** 2, (v) => v / 1609.344 ** 2],
  // length
  cm: [(v) => v / 100, (v) => v * 100],
  m: [(v) => v, (v) => v],
  km: [(v) => v * 1_000, (v) => v / 1_000],
  inch: [(v) => v * 0.0254, (v) => v / 0.0254],
  ft: [(v) => v * 0.3048, (v) => v / 0.3048],
  mile: [(v) => v * 1609.344, (v) => v / 1609.344],
  // mass
  kg: [(v) => v, (v) => v],
  g: [(v) => v / 1000, (v) => v * 1000],
  // speed
  "m/s": [(v) => v, (v) => v],
  "km/h": [(v) => v / 3.6, (v) => v * 3.6],
  "mile/h": [(v) => v * 0.44704, (v) => v / 0.44704],
  // temperature
  "\u00B0C": [(v) => v, (v) => v],
  "\u00B0F": [(v) => (5 / 9) * (v - 32), (v) => v * (9 / 5) + 32],
  K: [(v) => v + 273.15, (v) => v - 273.15],
  // time
  s: [(v) => v, (v) => v],
  h: [(v) => v / 3600, (v) => v + 3600],
  // volume
  "m\u00B3": [(v) => v, (v) => v],
  l: [(v) => v * 1000, (v) => v / 1000],
  "inch\u00B3": [(v) => v * 0.0254 ** 3, (v) => v / 0.0254 ** 3],
  "ft\u00B3": [(v) => v * 0.3048 ** 3, (v) => v / 0.3048 ** 3],
};

const properties = {
  area: {
    base: "m\u00B2",
    icon: "area",
    units: [
      "cm\u00B2",
      "m\u00B2",
      "km\u00B2",
      "inch\u00B2",
      "ft\u00B2",
      "mile\u00B2",
    ],
  },
  length: {
    base: "m",
    icon: "arrows",
    units: ["cm", "m", "km", "inch", "ft", "mile"],
  },
  mass: { base: "kg", icon: "minecart-loaded", units: ["kg", "g"] },
  speed: { base: "m/s", icon: "spedometer", units: ["km/h", "m/s", "mile/h"] },
  temperature: {
    base: "\u00B0C",
    icon: "thermometer",
    units: ["\u00B0C", "\u00B0F", "K"],
  },
  time: { base: "s", icon: "hourglass", units: ["h", "s"] },
  volume: {
    base: "m\u00B3",
    icon: "beaker",
    units: ["m\u00B3", "l", "inch\u00B3", "ft\u00B3"],
  },
};

// Style frame
// XXX TODO Move to router
css`
  #frame {
    nav[slot="top"] {
      display: flex;

      .nav-link {
        color: var(--bs-white);
      }
    }

    nav[slot="side"] {
      display: flex;
      flex-direction: column;
      font-size: 1.125rem;
    }
  }
`.use();

// Build frame
//const base = "http://127.0.0.1:5500/_scratch/convertit/index.html";
const base = "http://127.0.0.1:5500/_scratch/convertit";

let constructed = location.href.split("/");
constructed.pop();
constructed = constructed.join("/");
console.log("constructed:", constructed);

console.dir(location); ////

const foo = (() => {
  let _pathname = location.pathname.split("/");
  _pathname.pop();
  _pathname = _pathname.join("/");
  console.log("_pathname:", _pathname);

  const theme = '_/theme'

  const result = `${location.origin}/${theme}${_pathname}`

  console.log("result:", result);

  if (location.hostname === "127.0.0.1") {
  }
})();

//const src = `${base}/favicon.svg`;
const src = './favicon.svg'

component.img({ src, slot: "home", parent: frame });

component.nav(
  "nav",
  { slot: "top", parent: frame },
  component.a("nav-link", {
    text: "Settings",
    title: "Set number formats and defaults",
  }),
  component.a("nav-link", {
    text: "Go premium",
    title: "Get access to advanced calculations and more",
  }),
);
component.nav(
  "nav",
  { slot: "side", parent: frame },
  component.a("nav-link", { text: "About" }),
  component.a("nav-link", { text: "Units", title: "Learn about units" }),
  component.a("nav-link", {
    text: "Customize",
    title: "Add your own conversions",
  }),
  component.a("nav-link", {
    text: "Newsletter",
    title: "Units digest in your inbox",
  }),
);

// Build page
const page = component.div(`container.py-3`, { parent: frame });
page.innerHTML = html`
  <style>
    [uid="${page.uid}"] {
      h1 {
        text-align: center;

        span {
          color: var(--bs-success);
        }
      }

      form {
        max-width: ${breakpoints.sm}px;
        display: flex;
        flex-direction: column;
        align-items: center;
        row-gap: 1rem;

        margin-left: auto;
        margin-right: auto;

        [icon] {
          width: 4rem;
          display: flex;
          justify-content: center;
        }

        select.unit {
          max-width: 6rem;
        }

        label {
          min-width: 6rem;
        }

        select > option[selected] {
          color: var(--bs-primary-text-emphasis);
        }

        fieldset {
          border: none;
          padding: 0;
          margin: 0;
          /* Fix grid/flexbox overflow quirks in fieldsets */
          min-width: 0;
        }
      }
    }

    #app[state-lg] [uid="${page.uid}"] {
      form {
        max-width: ${breakpoints.sm}px;
      }
    }
  </style>
  <h1 class="mb-3">Unit conversion made <span>simple</span></h1>
`;

const form = component.from(
  html` <!--foo-->
    <form>
      <div class="input-group">
        <label class="input-group-text">Property</label>
        <select
          name="property"
          class="form-select property"
          title="Property"
        ></select>
        <output class="input-group-text" icon name="icon">icon</output>
      </div>

      <fieldset class="input-group" name="a">
        <select name="unit" class="form-select unit" title="Unit"></select>
        <input
          name="value"
          type="number"
          class="form-control"
          placeholder="Number"
          value="1"
          title=" "
        />
        <button
          class="input-group-text"
          type="button"
          name="reset"
          title="Reset to 1"
          icon
        ></button>
      </fieldset>

      <fieldset class="input-group" name="b">
        <select name="unit" class="form-select unit" title="Unit"></select>
        <input
          name="value"
          type="number"
          class="form-control"
          placeholder="Number"
          title=" "
        />
        <button
          class="input-group-text"
          type="button"
          name="reset"
          title="Reset to 1"
          icon
        ></button>
      </fieldset>
    </form>`,
  { parent: page },
);

// Get elements

const a = form.elements.a.elements;
const b = form.elements.b.elements;

a.reset.innerHTML = icons.x;
b.reset.innerHTML = icons.x;

(() => {
  const onclick = (event) => {
    const fieldset = event.target.closest(`fieldset`);
    fieldset.elements.value.value = 1;
    input.update(fieldset.elements.value);

    if (input.current === a.value) {
      b.value.value = convert(input.current.value, a.unit.value, b.unit.value);
    } else {
      a.value.value = convert(input.current.value, b.unit.value, a.unit.value);
    }
  };
  a.reset.on.click(onclick);
  b.reset.on.click(onclick);
})();

const input = new Ref(a.value);

/* Set selected option by value and explicitly adds 'selected' attribute. */
function select(target, value) {
  const previous = target.find(`[selected]`);
  if (previous) {
    previous.attribute.selected = false;
  }
  const current = target.find(`[value="${value}"]`);
  current.attribute.selected = true;
  return target;
}

function convert(value, unit1, unit2) {
  if (value !== "") {
    const toBase = units[unit1][0];
    const fromBase = units[unit2][1];
    return fromBase(toBase(value));
  }
  return null;
}

// Populate property select
for (const value of Object.keys(properties)) {
  const option = component.option({
    text: capitalize(value),
    value,
    parent: form.elements.property,
  });
}

// Add event handlers
form.elements.property.on.change(
  (event) => {
    //console.log("event:", event); ////
    const target = event.target;
    const value = target.value;
    // Unset/set selected option
    select(target, value);
    // Set icon
    form.elements.icon.innerHTML = icons[properties[value].icon];
    // Popuilate unit selects
    a.unit.clear();
    b.unit.clear();
    const units = properties[value].units;
    // Populate unit selects
    for (const unit of units) {
      a.unit.append(
        component.option({
          text: unit,
          value: unit,
          "[value]": unit,
        }),
      );
      b.unit.append(
        component.option({
          text: unit,
          value: unit,
          "[value]": unit,
        }),
      );
    }
    // Set default select value
    const base = properties[value].base;
    select(a.unit, base);
    select(b.unit, base);
    if (input.current === a.value) {
      b.value.value = convert(input.current.value, a.unit.value, b.unit.value);
    } else {
      a.value.value = convert(input.current.value, b.unit.value, a.unit.value);
    }
  },
  { run: true },
);

(() => {
  const onchange = (event) => {
    select(event.target, event.target.value);
    if (input.current === a.value) {
      b.value.value = convert(input.current.value, a.unit.value, b.unit.value);
    } else {
      a.value.value = convert(input.current.value, b.unit.value, a.unit.value);
    }
  };
  a.unit.on.change(onchange);
  b.unit.on.change(onchange);
})();

(() => {
  const onchange = (event) => {
    input.update(event.target);

    if (input.current === a.value) {
      b.value.value = convert(input.current.value, a.unit.value, b.unit.value);
    } else {
      a.value.value = convert(input.current.value, b.unit.value, a.unit.value);
    }
  };

  a.value.on.change(onchange);
  b.value.on.change(onchange);
})();
