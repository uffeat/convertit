export default async (use, {path}) => {

  console.log('path:', path)


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

  const convert = await use("@@/convert/convert.py");
  const properties = await use("@@/convert/properties.json");
  const { icons } = await use("@@/convert/icons.js");

  // Build page
  const page = component.div(`container.py-3`, { parent: app });
  page.attribute.path = path






  page.innerHTML = html`
   
    <h1 class="mb-3">Unit conversion made <span>simple</span></h1>
  `;

  const form = component.from(await use("@@/convert/form.html"), {
    parent: page,
  });

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
        b.value.value = convert(
          input.current.value,
          a.unit.value,
          b.unit.value,
        );
      } else {
        a.value.value = convert(
          input.current.value,
          b.unit.value,
          a.unit.value,
        );
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
        b.value.value = convert(
          input.current.value,
          a.unit.value,
          b.unit.value,
        );
      } else {
        a.value.value = convert(
          input.current.value,
          b.unit.value,
          a.unit.value,
        );
      }
    },
    { run: true },
  );

  (() => {
    const onchange = (event) => {
      select(event.target, event.target.value);
      if (input.current === a.value) {
        b.value.value = convert(
          input.current.value,
          a.unit.value,
          b.unit.value,
        );
      } else {
        a.value.value = convert(
          input.current.value,
          b.unit.value,
          a.unit.value,
        );
      }
    };
    a.unit.on.change(onchange);
    b.unit.on.change(onchange);
  })();

  (() => {
    const onchange = (event) => {
      input.update(event.target);

      if (input.current === a.value) {
        b.value.value = convert(
          input.current.value,
          a.unit.value,
          b.unit.value,
        );
      } else {
        a.value.value = convert(
          input.current.value,
          b.unit.value,
          a.unit.value,
        );
      }
    };

    a.value.on.change(onchange);
    b.value.on.change(onchange);
  })();

  return page;
};
