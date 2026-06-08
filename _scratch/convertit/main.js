const { default: use } = await import(`https://rolloh.vercel.app/anvil/use.js`);
const { Reactive, Ref, Sheet, app, capitalize, component, css, html, is } =
  await use("@/rollo/");
const { frame } = await use("@/frame/");
const { Form, Input } = await use("@/form/");
await use(`@/bootstrap/`);

const dimensions = {
  area: { unit: "m", power: 2, units: ["km^2", "m^2"] },
  length: { unit: "m", units: ["km", "m"] },
  mass: { unit: "kg", units: ["kg", "g"] },
  speed: { computed: (length, time) => length / time, units: ["km/h", "m/s"] },
  time: { unit: "s", units: ["h", "s"] },
  volume: { unit: "m", power: 3, units: ["m^2", "l"] },
};

const sheet = css`
  form {
    border: 1px solid pink;
  }

  select.dimension {
    max-width: 8rem;
  }

  select.from {
    max-width: 8rem;
  }

  nav.dimension > a[active] {
    background-color: var(--bs-secondary);
  }
`.use();

const form = Form(`container py-3`, { parent: frame });

const control = component.from(
  html`<div class="input-group">
    <select class="form-select dimension"></select>
    <input
      name="from"
      type="number"
      class="form-control"
      aria-label="Text input with dropdown button"
    />
    <select class="form-select from"></select>
  </div>`,
  { parent: form },
);

// Get elements
const dimensionSelect = control.find(`select.dimension`);
const fromUnitSelect = control.find(`select.from`);
const fromValueInput = control.find(`input[name="from]`);

// Create states
const dimensionState = new Ref();
const fromUnitState = new Ref();

// Populate dimension select
for (const value of Object.keys(dimensions)) {
  const option = component.option({
    text: capitalize(value),
    value,
    parent: dimensionSelect,
  });
  
}
// Update dimension state
dimensionState.update(dimensionSelect.value);

dimensionState.effects.add((current) => {
  //console.log("dimension:", current); //
  fromUnitSelect.clear();
  const units = dimensions[current].units;
  console.log("units:", units); //
  // Populate dimension select
  for (const value of units) {
    const option = component.option({
      text: value,
      value,
      parent: fromUnitSelect,
    });
  }
  // Update from unit state
  fromUnitState.update(fromUnitSelect.value);
});

fromUnitState.effects.add((current) => {
  console.log("from unit:", current); //
  
});

dimensionSelect.on.change((event) => {
  //console.log("value:", event.target.value); //
  // Update dimension state
  dimensionState.update(event.target.value);
});

fromUnitSelect.on.change((event) => {
  //console.log("value:", event.target.value); //
  // Update from unit state
  fromUnitState.update(event.target.value);
});
