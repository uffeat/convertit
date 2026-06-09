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
//console.log(form.elements.property); //
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
    }else if (change._to_unit) {
      console.log("To unit is now:", change._to_unit); ////
    }
  },
  ["_property", "_from_unit", "from_value", "_to_unit", "to_value"],
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
  }
});


