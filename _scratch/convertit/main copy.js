const { default: use } = await import(`https://rolloh.vercel.app/anvil/use.js`);
const { Reactive, Ref, Sheet, app, capitalize, component, css, html, is } =
  await use("@/rollo/");
const { frame } = await use("@/frame/");
const { Form, Input } = await use("@/form/");

await use(`@/bootstrap/`);

const sheet = css`
  form {
    border: 1px solid pink;
  }

  button.dimension {
    min-width: 8rem;
  }

  nav.dimension > a[active] {
    background-color: var(--bs-secondary);
  }
`.use();

const form = Form(`container py-3`, { parent: frame });

const control = component.from(
  html`<div class="input-group">
    <button
      class="btn btn-outline-secondary dropdown-toggle dimension"
      type="button"
      data-bs-toggle="dropdown"
      aria-expanded="false"
    >
      Dimension
    </button>
    <nav class="dropdown-menu dimension">
      <a class="dropdown-item" value="area">Area</a>
      <a class="dropdown-item" value="length">Length</a>
      <a class="dropdown-item" value="mass">Mass</a>
      <a class="dropdown-item" value="speed">Speed</a>
      <a class="dropdown-item" value="time">Time</a>
      <a class="dropdown-item" value="volume">Volume</a>
    </nav>
    <input
      name="from"
      type="number"
      class="form-control"
      aria-label="Text input with dropdown button"
    />
    <select class="form-select" aria-label="Default select example">
      <option selected>Open this select menu</option>
      <option value="1">One</option>
      <option value="2">Two</option>
      <option value="3">Three</option>
    </select>
  </div>`,
  { parent: form },
);

const dimensionButton = control.find(`button.dimension`);
//console.log("dimensionButton:", dimensionButton);//
const dimensionNav = control.find(`nav.dimension`);

const dimensionState = new Ref("area");

dimensionState.effects.add((current) => {
  //console.log("current:", current);//
  dimensionButton.text = capitalize(current);
  let active = dimensionNav.find(`a[active]`);
  if (active) {
    active.attribute.active = null;
  }
  active = dimensionNav.find(`a[value="${current}"]`);
  if (active) {
    active.attribute.active = true;
  }
});

dimensionNav.on.click((event) => {
  //console.log("event:", event); //

  if (event.target.tagName === "A") {
    //console.log("event.target:", event.target); //
    //console.log("value:", event.target.attribute.value); //
    dimensionState.update(event.target.attribute.value);
  }
});
