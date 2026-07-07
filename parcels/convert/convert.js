export default async (use) => {
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

  const { Form, Input } = await use("@/form/");
  await use(`@/bootstrap/`);

  //const { convert, properties } = await use("@@/convert/convert.py");
  const { convert } = await use("@@/convert/convert.py");
  const properties = await use("@@/convert/properties.json");
  console.log("properties:", properties); //

  // Build local icons
  const icons = {
    arrows: await use("@@/icons/arrows.svg"),
    aspect_ratio: await use("@@/icons/aspect_ratio.svg"),
    beaker: await use("@@/icons/beaker.svg"),

    c_circle: await use("@@/icons/c_circle.svg"),
    hourglass_split: await use("@@/icons/hourglass_split.svg"),
    minecart_loaded: await use("@@/icons/minecart_loaded.svg"),
    rulers: await use("@@/icons/rulers.svg"),
    speedometer: await use("@@/icons/speedometer.svg"),
    thermometer: await use("@@/icons/thermometer.svg"),





    x: await use("@@/icons/x.svg"),
  };
  //console.log("icons:", icons); //

  // Build page
  const page = component.div(`container.py-3`, { parent: app });
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
    // Poppulate unit selects
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

  return { page };
};
