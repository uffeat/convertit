const { default: use } = await import(`https://rolloh.vercel.app/anvil/use.js`);
const { Reactive, Ref, Sheet, app, capitalize, component, css, html, is } =
  await use("@/rollo/");
const { frame } = await use("@/frame/");
const { Form, Input } = await use("@/form/");
await use(`@/bootstrap/`);

const properties = {
  area: { units: ["km^2", "m^2"] },
  length: { unit: "m", units: ["km", "m"] },
  mass: { unit: "kg", units: ["kg", "g"] },
  speed: { units: ["km/h", "m/s"] },
  time: { units: ["h", "s"] },
  volume: { units: ["m^2", "l"] },
};

const sheet = css`

  form {
    display: flex;
  }
  

  select.property {
    //max-width: 8rem;
    background-color: var(--bs-secondary);
  }

  select.property > option {
    background-color: var(--bs-body-bg);
  }

  select.unit {
    max-width: 8rem;
  }
`.use();

const page = component.div(`container py-3`, { parent: frame });

const form = component.from(
  html`<form class="input-group">
    <select name="property" class="form-select property" title="Property"></select>
    <input name="from_value" type="number" class="form-control" />
    <select name="from_unit" class="form-select unit from" title="Unit"></select>
    <input name="to_value" type="number" class="form-control" />
    <select name="to_unit" class="form-select unit to" title="Unit"></select>
  </form>`,
  { parent: page },
);

// Get elements

const propertySelect = form.find(`select.property`);
const fromUnitSelect = form.find(`select.from`);
const fromValueInput = form.find(`input[name="from_value"]`);

// Create states
const propertyState = new Ref();
const fromUnitState = new Ref();
const fromValueState = new Ref();

// Populate property select
for (const value of Object.keys(properties)) {
  const option = component.option({
    text: capitalize(value),
    value,
    parent: propertySelect,
  });
}
// Update property state
propertyState.update(propertySelect.value);

/* Effects */

propertyState.effects.add((current) => {
  console.log("property state:", current); //
  fromUnitSelect.clear();
  const units = properties[current].units;
  //console.log("units:", units); //
  // Populate property select
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
  console.log("from unit state:", current); //
});

fromValueState.effects.add((current) => {
  console.log("from value state:", current); //

  //console.log("typeof current:", typeof current); //
});

/* Event handlers */

propertySelect.on.Xchange((event) => {
  //console.log("value:", event.target.value); //
  // Update dimension state
  propertyState.update(event.target.value);
});

fromUnitSelect.on.Xchange((event) => {
  //console.log("value:", event.target.value); //
  // Update from unit state
  fromUnitState.update(event.target.value);
});

fromValueInput.on.Xchange((event) => {
  //console.log("value:", event.target.value); //
  // Update from unit state
  fromValueState.update(+event.target.value);
});




form.on.change((event) => {
  console.log("event:", event); //
 
 
});