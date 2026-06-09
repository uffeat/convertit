const { default: use } = await import(`https://rolloh.vercel.app/anvil/use.js`);
const { Reactive, Ref, Sheet, app, capitalize, component, css, html, is } =
  await use("@/rollo/");
const { frame } = await use("@/frame/");
const { Form, Input } = await use("@/form/");
await use(`@/bootstrap/`);

const properties = {
  area: { units: ["cm\u00B2", "m\u00B2", "km\u00B2"] },
  length: { units: ["cm", "m", "km"] },
  mass: { units: ["kg", "g"] },
  speed: { units: ["km/h", "m/s"] },
  time: { units: ["h", "s"] },
  volume: { units: ["m\u00B3", "l"] },
};

const factors = {
  cm: 100 ** -1,
  m: 1,
  km: 1000 ** 1,

  "cm\u00B2": 100 ** -2,
  "m\u00B2": 1,
  "km\u00B2": 1000 ** 2,
};

//console.log(factors["km\u00B2"]); ////

function convert(value, from, to) {
  from = factors[from];
  to = factors[to];
  if (value && from && to) {
    return value * (from / to);
  }
}

const result = convert(1, "m", "cm");
//console.log("result:", result); ////

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
    <select
      name="property"
      class="form-select property"
      title="Property"
    ></select>
    <input name="from_value" type="number" class="form-control" />
    <select
      name="from_unit"
      class="form-select unit from"
      title="Unit"
    ></select>
    <input name="to_value" type="number" class="form-control" />
    <select name="to_unit" class="form-select unit to" title="Unit"></select>
  </form>`,
  { parent: page },
);

// Get elements
//console.dir(form); //
//console.log(form.elements.property); ////
const elements = form.elements;

// Add effects

form.effects.add(
  (change, message) => {
    //console.log("change:", change); ////
    //console.log("message:", message); ////
    if (change._property) {
      console.log("Property is now:", change._property); ////
      elements.from_unit.clear();
      elements.to_unit.clear();
      const units = properties[change._property].units;
      //console.log("units:", units); //
      // Populate unit selects
      for (const value of units) {
        elements.from_unit.append(
          component.option({
            text: value,
            value,
          }),
        );
        elements.to_unit.append(
          component.option({
            text: value,
            value,
          }),
        );
      }
    } else if (change._from_unit) {
      console.log("From unit is now:", change._from_unit); ////
    } else if (change._to_unit) {
      console.log("To unit is now:", change._to_unit); ////
    } else if (change._from_value) {
      console.log("From value is now:", change._from_value); ////
    } else if (change._to_value) {
      console.log("To value is now:", change._to_value); ////
    }



    const value = form.$._from_value
    console.log("value:", value); ////
    const from = form.$._from_unit
    console.log("from:", from); ////
    const to = form.$._to_unit
    console.log("to:", to); ////



    const converted = convert(value, from, to);
    console.log("converted:", converted); ////
  },
  ["_property", "_from_unit", "_from_value", "_to_unit", "_to_value"],
);

// Populate property select
for (const value of Object.keys(properties)) {
  const option = component.option({
    text: capitalize(value),
    value,
    parent: form.elements.property,
  });
}
// Update property state
form.$({ _property: elements.property.value });

/* Event handlers */
form.on.change((event) => {
  //console.log("event:", event); ////
  const target = event.target;
  if (target === elements.property) {
    //console.log("Property changed to: ", target.value); ////
    form.$({ _property: target.value });
  } else if (target === elements.from_unit) {
    console.log("From unit changed to: ", target.value); ////
    form.$({ _from_unit: target.value });
  } else if (target === elements.to_unit) {
    console.log("To unit changed to: ", target.value); ////
    form.$({ _to_unit: target.value });
  } else if (target === elements.from_value) {
    console.log("From value changed to: ", target.value); ////
    form.$({ _from_value: +target.value });
  } 
});
