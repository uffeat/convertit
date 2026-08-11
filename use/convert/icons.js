export default async (use) => {
  // Build local icons
  const icons = Object.freeze({
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
  });

  return { icons };
};
