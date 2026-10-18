"use strict";
const form = document.getElementById("storage-form");
const output = document.getElementById("storage-result");
function updateStorage(event) {
  if (event) event.preventDefault();
  if (!form.reportValidity()) return;
  const groups = [["photo-count", "photo-mb", "Photos"], ["shot-count", "shot-mb", "Screenshots"], ["video-count", "video-mb", "Videos"]];
  const parts = groups.map(([count, size, label]) => ({label, mb: Number(document.getElementById(count).value) * Number(document.getElementById(size).value)}));
  if (parts.some(part => !Number.isFinite(part.mb) || part.mb < 0)) return;
  const total = parts.reduce((sum, part) => sum + part.mb, 0);
  const format = value => new Intl.NumberFormat(undefined, {maximumFractionDigits: 3}).format(value);
  output.textContent = `${format(total / 1000)} GB of total file bytes (${format(total)} MB). ${parts.map(part => `${part.label}: ${format(part.mb)} MB`).join("; ")}. This is not measured free phone storage.`;
}
if (form && output) form.addEventListener("submit", updateStorage);
